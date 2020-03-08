from logging import getLogger
from pathlib import Path
from typing import Set

from ics import Calendar
from ics.parse import ContentLine

from holodule.event import LiveEvent

log = getLogger(__name__)

class Schedule():
    def __init__(self, name:str, tree) -> None:
        self.name = name
        self.tree = tree

        self.events = []
        self.parse_events()

    @property
    def video_ids(self) -> Set[str]:
        return { e.video_id for e in self.events }

    @property
    def ical_calendar(self) -> Calendar:
        cal = Calendar(events=[e.ical_event for e in self.events], creator="holodule-ical")
        cal.extra.append(ContentLine("X-WR-CALNAME", value=f"Holodule - {self.name}"))
        cal.extra.append(ContentLine("X-WR-TIMEZONE", value="Asia/Tokyo"))
        return cal

    def parse_events(self) -> None:
        for i in self.tree.xpath('.//a'):
            log.debug(f"processing: {i.text}")
            # ホロライブ公式チャンネルでの配信はアイコンがない 虚無だ…
            _, name, *rest = i.text.split()
            icon = rest[0] if rest else ""
            url = i.get("href")
            self.events.append(LiveEvent(f"{icon}{name}", url))

        log.info(f"parsed {len(self.events)} events: {self.name}")

    def assign_youtube(self, yt_meta:dict) -> None:
        # is there any case that stream is registered to Holodule but not to YouTube?
        # if so, we need to include these events.
        self.events = [e for e in self.events if e.assign(yt_meta.get(e.video_id))]

    def dump(self, save_dir:str) -> None:
        path = Path(save_dir)
        path.mkdir(parents=True, exist_ok=True)
        with (path/f"holodule-{self.name}.ics").open('w', encoding="utf-8") as f:
            f.writelines(self.ical_calendar)
