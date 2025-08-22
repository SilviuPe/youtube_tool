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

STANDARD_PROMPT_TITLE = """
Generate a catchy YouTube Shorts video title.
Rules:
- Maximum 8 words.
- Must be directly based on the script provided.
- Should be intriguing, clickable, and relevant.
- Avoid clickbait, all caps, or excessive punctuation.
- Write the title exactly as it should be written in the title textarea.

Script:
\"\"\"{script}\"\"\"
"""

STANDARD_PROMPT_DESCRIPTION = """
Generate a YouTube Shorts video description.
Rules:
- Maximum 2 sentences (under 40 words).
- Summarize the main idea of the script clearly.
- Keep the tone friendly and engaging.
- Can include a call-to-action or a curious question.
- No hashtags, emojis, or unnecessary fluff.
- Write the description exactly as it should be written in the description textarea.

Script:
\"\"\"{script}\"\"\"
"""
