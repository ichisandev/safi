import os
import io
from pydantic_ai import Agent
from google import genai
from google.genai import types
from dotenv import load_dotenv

from utils import config
from servicess.chatbot import memory

load_dotenv()

trigger_words = ["gambarkan", "gambarin"]
generate_image_prompt = """
Kamu adalah gadis yang sangat bersahabat dan loyal bernama unmei-chan.
Kamu adalah pembuat image prompt.
Responlah hanya image prompt yang singkat dan jelas dalam bahasa inggris.
Fokuskan image prompt pada permintaan terakhir.
"""

agent = Agent(
    model=config.GENAI_MODEL,
    system_prompt=generate_image_prompt,
)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

async def main(message):
    if "gambarkan" in str(message.content).lower():
        image_prompt = str(message.content).lower().replace("unmei-chan", "").replace("mei", "")
    else:
        prompt = memory.get_chat_history(str(message.channel.id))
        agent_response = await agent.run(prompt)
        image_prompt = agent_response.data.lower().replace("unmei-chan", "").replace("mei", "")
        await message.channel.send(image_prompt)
    response = client.models.generate_content(
        model="models/gemini-2.0-flash-exp",
        contents=image_prompt,
        config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
    )
    try:
        for part in response.candidates[0].content.parts:
          if part.text is not None:
            await message.channel.send(part.text)
          if part.inline_data is not None:
            with io.BytesIO(part.inline_data.data) as file:
                await message.channel.send(file=discord.File(file, "generated_image.png"))
    except:
        await message.channel.send("Image generation error, your request might be inappropriate")
    return

