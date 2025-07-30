from crewai.flow import Flow, start, listen
from crewai.agent import Agent
from tiktoker.media import still_frames_from_video, extract_audio_from_video, ensure_ffmpeg
from tiktoker.ai import describe_image, transcribe
from tiktoker.models import Timeline

class TiktokerFlow(Flow):
    @start()
    def initialize_state(self):
        ensure_ffmpeg()

        if self.state.get("frame_sampling_interval_seconds") is None:
            self.state["frame_sampling_interval_seconds"] = 2.0

    @listen(initialize_state)
    def transcribe(self):
        audio_path = extract_audio_from_video(self.state["video_path"])
        self.state["transcription"] = transcribe(audio_path)

    @listen(transcribe)
    def describe(self):
        frames = still_frames_from_video(self.state["video_path"], interval_seconds=self.state["frame_sampling_interval_seconds"])
        frame_descriptions = []
        for i, frame in enumerate(frames):
            description = describe_image(frame, int(i * self.state["frame_sampling_interval_seconds"] * 1000))
            frame_descriptions.append(description)

        self.state["frame_descriptions"] = frame_descriptions

    @listen(describe)
    def build_timeline(self):
        self.state["timeline"] = Timeline(items=[*self.state["transcription"], *self.state["frame_descriptions"]])
        print(self.state["timeline"])
    
    @listen(build_timeline)
    async def critique(self):
        total_duration = max(item.milliseconds_from_start for item in self.state["timeline"].items)
        
        analyst = Agent(
            role="Viral Video Analyst",
            goal="Analyze social media video content for viral potential using established frameworks and data-driven insights.",
            backstory="""You are an expert viral video analyst with deep knowledge of:
            - Social media algorithms (TikTok, Instagram, YouTube Shorts)
            - Viral content patterns and psychological triggers
            - Attention retention strategies and hook effectiveness
            - Visual-audio synchronization and pacing analysis
            - Engagement optimization techniques
            
            You provide evidence-based analysis using only the provided timeline data.""",
            verbose=True,
            model="openai/gpt-4o"
        )

        query = f"""
        Analyze this {total_duration:.1f}-second video for viral potential on social media. Focus on:

        1. Hook (0-3s): Attention grab, value prop, audio-visual impact
        2. Pacing: Flow, sync, potential drop-offs
        3. Viral elements: Emotional triggers, shareability, entertainment value
        4. Technical: Audio clarity, visual quality, timing

        Format your response as:

        HOOK SCORE (1-10): [score + evidence]
        PACING SCORE (1-10): [score + evidence] 
        VIRAL SCORE (1-10): [score + evidence]

        STRENGTHS:
        - [2-3 key strengths with timestamps]

        IMPROVEMENTS:
        - [2-3 specific suggestions with timestamps]

        Base all analysis only on the provided timeline data. Reference specific timestamps.

        ## VIDEO TRANSCRIPTION
        {self.state["timeline"]}
        """

        result = await analyst.kickoff_async(query)
        print(result.raw)
        return result

def kickoff():
    flow = TiktokerFlow()
    flow.kickoff(inputs={"video_path": "/Users/replaceme/video.mp4"})


def plot():
    flow = TiktokerFlow()
    flow.plot()


if __name__ == "__main__":
    kickoff()
