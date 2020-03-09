from logging import getLogger

import arrow
from ics import Event

log = getLogger(__name__)

class LiveEvent():
    def __init__(self, name:str, url:str) -> None:
        self.name = name
        self.url = url
        
        self.title = None
        self.begin = None

    @property
    def video_id(self) -> str:
        # hope holodule do not change url rule...
        return self.url.split('=')[1]

    @property
    def ical_event(self) -> Event:
        return Event(
            name=f"{self.name}: {self.title}",
            begin=self.begin,
            duration={"hours": 2},
            description=f"{self.title}\n{self.url}",
            # use video_id as uid will make order of events static
            # (because uid is used in Event.__hash__)
            uid=self.video_id # TODO: コラボで同じ動画が複数ホロジュールに登録される可能性？
        )

    def assign(self, meta:dict) -> bool:
        try:
            self.title = meta['snippet']['title'] if 'snippet' in meta else None
            if not self.title:
                log.error(f"Failed to get title: video_id {self.video_id}")
                return False

            begin = None
            lsd = meta.get('liveStreamingDetails')
            if lsd:
                # when live is not scheduled, get actualStartTime instead
                begin = lsd.get('scheduledStartTime') or lsd.get('actualStartTime')
            else:
                # sometime it's not a stream, just a video.
                # so get published time
                # TODO: is this correct?
                begin = meta['snippet']['publishedAt']
            
            if not begin:
                log.error(f"Failed to get begin time: video_id {self.video_id}")
                return False
            self.begin = arrow.get(begin)
        except:
            log.error("Something odd has happened: ", exc_info=True)
            return False

        return True
