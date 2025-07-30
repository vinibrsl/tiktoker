from pydantic import BaseModel
from typing import Literal

class TimelineItem(BaseModel):
    milliseconds_from_start: int
    kind: Literal["audio_transcript", "frame_description"]
    content: str

    def __str__(self) -> str:
        return f"[timestamp={self.milliseconds_from_start}ms][type={self.kind}] {self.content}"

class Timeline(BaseModel):
    items: list[TimelineItem]

    def __str__(self) -> str:
        return "\n".join(str(item) for item in sorted(self.items, key=lambda item: item.milliseconds_from_start))