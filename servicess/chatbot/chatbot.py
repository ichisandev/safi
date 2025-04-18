import re
import textwrap
import google.generativeai as genai

from servicess.embed_component import generate_bounding_box

from . import memory, gemini, content_fetcher
from ..agents import link_reader


async def get_image_prompt(photo, text, context):
    image_base_64 = await content_fetcher.get_image_base64(photo, context)
    prompt = [
        {"mime_type": "image/jpeg", "data": image_base_64},
        text
    ]
    return prompt


def get_link_prompt(message):
    links = re.findall(r"https://[^\s\"'>]+", str(update.message.text))
    images = [link_reader.get_link_ss(link) for link in links]
    prompt = [{"mime_type": "image/jpeg", "data": image} for image in images]
    prompt.append(message.content)
    return prompt


async def main(update, context):
    if update.message.photo:
        prompt = await get_image_prompt(update.message.photo[-1], update.message.caption, context)
    elif update.message.reply_to_message:
        try:
            prompt = await get_image_prompt(update.message.reply_to_message.photo[-1], update.message.text, context)
        except:
            pass
    #     if "tandain" in str(update.message.caption).lower():
    #         await generate_bounding_box.send_bounding_box(update.message)
    #         return
    #     else:
    # # elif "https" in str(message.content):
    # #     prompt = get_link_prompt(message)
    else:
        prompt = memory.get_chat_history(str(update.message.chat.id))

    result = gemini.model.generate_content(
        prompt
    )
    result_filtered = result.text.replace("jarfish: ", "").replace("jarfish-bot: ", "").replace("JarfishBot: ", "")
    for response_part in textwrap.wrap(result_filtered, 1999, expand_tabs=False, replace_whitespace=False, drop_whitespace=False,):
        memory.store_message(chatroom_id=str(update.message.chat.id), message=f"jarfish: {response_part}")
        await context.bot.send_message(chat_id=update.message.chat.id, text=response_part)
    return
