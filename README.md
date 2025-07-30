# TikToker

TikToker is an AI Agent powered by CrewAI that analyzes short-form video content
for viral potential.

## Example

Here's a sample output from TikToker:

> **HOOK SCORE (1-10): 7**
> - Evidence: The hook occurs within the first 3 seconds, starting with the question about 
> the high-tech toilet, which piques curiosity. The close-up of the toilet bowl and clear 
> labeling immediately draws viewers in, making them want to learn more about this unique 
> product.
>
> **PACING SCORE (1-10): 6**
> - Evidence: The pacing is relatively consistent, maintaining a steady flow between 
> segments. However, there are moments, particularly around 8000ms, where the focus on the 
> control panel could lead to a drop-off if viewers find the information less engaging. 
> The transitions could be smoother to maintain viewer interest throughout.
>
> **VIRAL SCORE (1-10): 8**
> - Evidence: The video contains high entertainment value due to the humorous mishap with 
> the bidet at 12199ms and the unique setting of a high-tech bathroom. Emotional 
> engagement is fostered by the presenter's enthusiastic demeanor, and the potential for 
> sharing is high given the lighthearted approach to a relatable experience.
>
> **STRENGTHS:**
> - **Engaging Hook (0-3s):** The direct question about the toilet captures attention 
> quickly and sets the expectation for an interesting reveal.
> - **Humor and Relatability (12199ms):** The unexpected mishap of trying to operate the 
> toilet without sitting down adds a humorous element, making the content more shareable 
> and relatable.
> - **Clear Focus on Unique Features (4000ms - 10000ms):** Close-ups of the bidet control 
> panel highlight its innovative features, appealing to viewers interested in home 
> technology.
>
> **IMPROVEMENTS:**
> - **Add Variety in Visuals (Drawing Attention):** Between 6000ms and 8000ms, incorporate 
> a wider variety of bathroom shots or user reactions to break the monotony of control 
> panel footage and keep viewers engaged.
> - **Enhance Closure (Final Seconds)**: At 15039ms and 16000ms, consider adding a concise 
> commentary or a funny closing remark that ties back to the introduction for a memorable 
> end, increasing the likelihood of shares and viewer retention.

## Implementation

TikToker leverages CrewAI Flows to orchestrate a video analysis pipeline. 

1. The process begins by extracting and transcribing the audio from the video.
2. After that, it samples video frames and uses an LLM to generate detailed descriptions
   of each still frame.
3. These audio transcriptions and visual descriptions are then combined into a timeline,
   which is analyzed by a specialized CrewAI agent. The agent evaluates the video's
   viral potential and provides actionable insights for improvement.

## Dependencies
- **[CrewAI](https://github.com/crewaiinc/crewai)** - Multi-agent AI framework for
  orchestrating the analysis workflow
- **[Python](https://www.python.org/)** - Programming language used for the core
  implementation
- **[ffmpeg](https://ffmpeg.org/)** - Library for handling video/audio processing and
  frame extraction
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Tool for downloading videos from
  various platforms

## Contributing

We welcome contributions to TikToker! Feel free to fork it and submit your pull requests.