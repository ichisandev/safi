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
generate_image_prompt = f"""
Kamu adalah gadis yang sangat bersahabat dan loyal bernama {config.BOT_NAME}.
Kamu adalah pembuat image prompt.
Responlah hanya image prompt yang singkat dan jelas dalam bahasa inggris.
Fokuskan image prompt pada permintaan terakhir.
"""

agent = Agent(
    model=config.GENAI_MODEL,
    system_prompt=generate_image_prompt,
)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

async def main(update, context):
    if "gambarkan" in str(update.message.text).lower():
        image_prompt = str(update.message.text).lower().replace("safi", "").replace("saf", "").replace("fi","")
    else:
        prompt = memory.get_chat_history(str(update.message.chat.id))
        agent_response = await agent.run(prompt)
        image_prompt = agent_response.data.lower().replace("safi", "").replace("saf", "").replace("fi","")
        await context.bot.send_message(chat_id=update.message.chat.id, text=image_prompt)
    response = client.models.generate_content(
        model="models/gemini-2.0-flash-exp",
        contents=image_prompt,
        config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
    )
    try:
        for part in response.candidates[0].content.parts:
          if part.text is not None:
            caption = part.text
          else:
            caption = "berikut request gambarmu!😊"
          if part.inline_data is not None:
            with io.BytesIO(part.inline_data.data) as file:
                await context.bot.send_photo(
                    chat_id=update.message.chat.id,
                    photo=file,
                    caption=caption
                )
            memory.store_message(chatroom_id=str(update.message.chat_id), message=f"{config.BOT_NAME}: {caption}")
    except:
        warning_message = "Waduh maaf, nggak bisa generete gambar kamu nih😔"
        await context.bot.send_message(chat_id=update.message.chat.id, text=warning_message)
        memory.store_message(chatroom_id=str(update.message.chat_id), message=f"{config.BOT_NAME}: {warning_message}")
    return

