import base64
from litellm import completion, transcription
from typing import List
from tiktoker.models import TimelineItem

VISION_MODEL = "openai/gpt-4o-mini"
AUDIO_MODEL = "openai/whisper-1"

def describe_image(image_path: str, milliseconds_from_start: int) -> TimelineItem:
    with open(image_path, "rb") as f:
        image_in_base64 = base64.b64encode(f.read()).decode("utf-8")

    response = completion(
        model=VISION_MODEL,
        messages=[{"role": "user", "content": [{"type": "text", "text": "Briefly describe what is shown in this video frame. No opinions or analysis."}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_in_base64}"}}]}],
        max_tokens=300
    )
    return TimelineItem(
        milliseconds_from_start=milliseconds_from_start,
        kind="frame_description",
        content=response["choices"][0]["message"]["content"]
    )

def transcribe(audio_path: str) -> List[TimelineItem]:
    with open(audio_path, "rb") as file:
        response = transcription(
            model=AUDIO_MODEL,
            file=file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

    return [
        TimelineItem(
            milliseconds_from_start=int(float(segment.get("start", 0)) * 1000),
            kind="audio_transcript",
            content=segment.get("text", "").strip()
        )
        for segment in response.segments
    ]