from together import Together

# Initialize Together API client
client = Together(api_key="b4ab017442d0ecebf62fe5ed409a6ea1d70b48e16e8a6efab6e7ea9b986a22cc")  # Replace with your API key

# Story prompt
# Story prompt for a long, immersive bedtime story
prompt = (
    "You are a masterful storyteller, a weaver of dreams and gentle tales, known far and wide for crafting **immersive bedtime stories** "
    "MINIMUM 1000+ WORDS SHOULD BE PRESENT IN YOUR OUTPUT PLEASE"
    "that bring comfort and serenity to those who need it most. Your stories are a sanctuary for weary minds, a soft refuge for those struggling with **insomnia, anxiety, or stress.** "
    "They flow like a gentle river, soothing and rhythmic, designed to ease listeners into a deep, restful sleep.\n\n"

    "**Tonight, you have been called upon to tell another tale...**\n\n"

    "Take a deep breath, settle into the warmth of the storytelling chamber, and let the magic of words unfold. "
    "Speak softly and with care, crafting a bedtime story that stretches across at least **3000+ words**, "
    "allowing the listener to sink deeper into relaxation with each passing moment. "
    "Every word should be wrapped in tranquility, every sentence flowing seamlessly into the next, creating a dreamlike experience that drifts between reality and fantasy.\n\n"

    "**Your story must include:**\n"
    "- A **mystical and soothing setting**\n"
    "- **Rich, immersive descriptions** of soft sounds, gentle breezes, shimmering light, and delicate textures to deepen the sense of peace and wonder.\n"
    "- **A slow, flowing, comforting narrative** that unfolds like a lullaby, without tension, danger, or urgency—only quiet discovery, peaceful moments, and dreamlike wonder.\n"
    "- **A character (or multiple)** who embarks on a magical journey of rest and renewal, guided by the soft whispers of nature, the stars, or an unseen, benevolent presence.\n"
    "- **Minimal dialogue**—allow the world to speak through its ambiance and the gentle rhythm of the narrative.\n\n"
    "- ** Something new every time, sometimes you follow a journey sometimes you make a character, sometimes space while sometimes a castl, sometimes the moon while sometimes the mountains, and sometimes the forests"
    "**Your storytelling should be timeless and free of modern distractions, as if whispered by an ancient storyteller beneath a sky full of stars.**\n\n"

    "**Example Themes:**\n"
    "- A wanderer finds a hidden village where time moves slower, allowing them to heal and rediscover peace.\n"
    "- A gentle wind spirit leads a lost soul through a valley of glowing flowers, where memories bloom like petals.\n"
    "- A floating library where books whisper bedtime stories to those who seek solace in their pages.\n"
    "- A peaceful voyage across an endless, starlit ocean where the waves hum ancient lullabies.\n"
    "- A secret garden where the trees hum songs of old, and every step leads deeper into serenity.\n\n"

    "Your writing should **flow like a soft breeze**, carrying the listener effortlessly toward relaxation with every word. "
    "The final paragraphs should feel like **a delicate lullaby**, guiding the listener into a dream-filled slumber. "
    "Use **subtle repetition, soft transitions, and calming rhythms** to enhance the effect.\n\n"

    "**Narration Style:**\n"
    "- Whenever you need to pause in your storytelling, add **a series of periods ('.')** proportional to the length of the pause, "
    "helping create a natural, rhythmic storytelling flow.\n"
    "- Ensure a **consistent, slow, and poetic tone**, never rushing through the descriptions or transitions.\n"
    "- Do not introduce any **abrupt events, conflict, or intense emotions**—this story should be **purely peaceful and meditative**.\n\n"

    "**Final Requirement:**\n"
    "THIS IS A MUST AND SHOULD BE DONE At the very end of your story, **on a new line**, append a unique title for the story. "
    "This title must begin with:\n"
    "'Soothing Sleep Story & Cozy Music for Deep Relaxation | ' followed by a short, creative phrase that reflects the essence of the narrative.\n\n"

    "**Output:**\n"
    " YOU MUST Start the story saying : Welcome to the sleep zone, let's unwind and get ready for a cozy night"
    "DO NOT ADD ANY NOTES AT ALL NOTHING BELOW THE FINAL TITLE LINE"
    "- A **fully written, structured bedtime story** in plain text.\n"
    "- No introductions, explanations, or formatting—only the story itself.\n"
    "- A total length of at least **1000+ words** (ensure it is complete and immersive)."
)





# API request
response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[
        {"role": "system", "content": "You are a masterful storyteller who writes immersive, relaxing bedtime stories."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=5000,
    temperature=0.8,  # More creative but not too random
    top_p=0.9,  # Allows more diverse responses
    repetition_penalty=1.08,  # Helps prevent loops
    stream=True  # Streaming is fine
)


# Open file to save output
with open("story.txt", "w", encoding="utf-8") as file:
    for token in response:
        if hasattr(token, "choices"):
            content = token.choices[0].delta.content
            # print(content, end="", flush=True)  # Print to console
            file.write(content)  # Write to file

print("\nStory saved to 'story.txt'!")
