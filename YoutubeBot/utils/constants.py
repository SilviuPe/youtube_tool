STANDARD_PROMPT = """
Generate a short script for a YouTube Shorts video.
Rules:
- Tone: friendly, energetic, and engaging.
- Length: maximum 50 words (around 20 seconds spoken).
- Structure:
  1. Start with a strong hook to grab attention instantly.
  2. Deliver the main idea about the category: "{category}" in a concise, impactful way.
  3. End with a quick conclusion or a curious question.

IMPORTANT:
- Write the script exactly as it should be spoken in the video, like a natural voiceover.
- Do not add explanations, titles, or labels, only the spoken script.
"""

STANDARD_MODEL = "gpt-4o-mini"