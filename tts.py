import edge_tts
import asyncio

async def text_to_speech():
    # Read the story text
    with open("story.txt", "r", encoding="utf-8") as file:
        story_text = file.read()

    # Set the output file name
    output_audio = "audio.mp3"

    # Choose a soothing male English voice
    voice = "en-US-BrianMultilingualNeural"  # A calm, natural-sounding male voice

    # Initialize Edge TTS
    tts = edge_tts.Communicate(story_text, voice)

    # Generate and save the TTS output
    await tts.save(output_audio)

    print(f"TTS conversion complete! The audio file is saved as {output_audio}")

# Run the async function
asyncio.run(text_to_speech())
