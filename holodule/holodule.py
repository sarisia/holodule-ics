import asyncio
from logging import getLogger
from math import ceil
from typing import Dict, Sequence, Set

from aiohttp import ClientSession, ClientTimeout
from lxml.html import document_fromstring

from holodule.errors import HTTPStatusError
from holodule.schedule import Schedule

CHUNK_SIZE = 50
YOUTUBE_API = "https://www.googleapis.com/youtube/v3/videos"
log = getLogger(__name__)

class Holodule():
    def __init__(self, holodule_page:str, youtube_key:str, save_dir:str) -> None:
        self.page_url = holodule_page
        self.yt_key = youtube_key
        self.save_dir = save_dir
        
        self.session = None
        self.videos = {}

    async def run(self) -> int:
        # ClientSession.__aenter__ does nothing
        # but ClientSession.__aexit__ closes this sessoin, so we have to do that.
        # https://github.com/aio-libs/aiohttp/blob/fe647a08d1acb53404b703b46b37409602ab18b4/aiohttp/client.py#L986
        self.session = ClientSession(
            timeout=ClientTimeout(total=30),
            headers={ "User-Agent": "Holodule-ICS" }
        )

        status = 0
        try:
            await self.do_run()
        except:
            log.error("Failed: ", exc_info=True)
            status = 1
        finally:
            await self.session.close()

        return status

    async def do_run(self) -> None:
        index_html = await self.get_page()
        index = document_fromstring(index_html)

        # TODO: make this selectable from command args
        target = ["all", "hololive", "holostars", "innk"]
        schedules: Dict[str, Schedule] = {}
        for t in target:
            elem = index.xpath(f'//*[@id="{t}"]')
            if elem:
                log.info(f"Found target: {t}")
                schedules[t] = Schedule(t, elem[0])

        # currently 'all' has all video ids so fetch this
        video_ids = schedules['all'].video_ids
        await self.get_videos(video_ids)

        for s in schedules.values():
            s.assign_youtube(self.videos)
            log.info(f"Dump {s.name}...")
            try:
                s.dump(self.save_dir)
            except:
                log.error(f"Failed to dump {s.name}: ", exc_info=True)

        log.info("Done!")

    async def get_page(self) -> str:
        log.info("Getting page...")
        async with self.session.get(self.page_url) as resp:
            if resp.status != 200:
                raise HTTPStatusError(resp.status)
                
            return await resp.text()

    async def get_videos(self, video_ids:Set[str]) -> None:
        # divide to chunks each contains 50 videos
        videos = list(video_ids)
        tasks = []
        for i in range( ceil( len(videos)/CHUNK_SIZE ) ):
            tasks.append(self.do_get_videos(videos[i*CHUNK_SIZE:min(len(videos), (i+1)*CHUNK_SIZE)]))

        results = await asyncio.gather(*tasks)
        for resp in results:
            for item in resp["items"]:
                self.videos[item["id"]] = item

    async def do_get_videos(self, video_ids:Sequence[str]) -> dict:
        async with self.session.get(
            YOUTUBE_API,
            params={
                "key": self.yt_key,
                "part": "id,snippet,liveStreamingDetails",
                "id": ",".join(video_ids)
            }
        ) as resp:
            if resp.status != 200:
                raise HTTPStatusError(resp.status)

            return await resp.json()
