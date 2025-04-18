import re
import textwrap
import google.generativeai as genai

from servicess.embed_component import generate_bounding_box

from . import memory, gemini, content_fetcher
from ..agents import link_reader


def get_image_prompt(update):
    prompt = [
        {"mime_type": "image/jpeg", "data": content_fetcher.get_image_base64(attachment.url)}
        for attachment in message.attachments
    ]
    prompt.append(update)
    return prompt


def get_link_prompt(message):
    links = re.findall(r"https://[^\s\"'>]+", str(update.message.text))
    images = [link_reader.get_link_ss(link) for link in links]
    prompt = [{"mime_type": "image/jpeg", "data": image} for image in images]
    prompt.append(message.content)
    return prompt


async def main(update, context):
    # if update.context.photo:
    #     if "tandain" in str(update.message.caption).lower():
    #         await generate_bounding_box.send_bounding_box(update.message)
    #         return
    #     else:
    #         prompt = get_image_prompt(update)
    # # elif "https" in str(message.content):
    # #     prompt = get_link_prompt(message)
    # else:
    prompt = memory.get_chat_history(str(update.message.chat.id))

    result = gemini.model.generate_content(
        prompt
    )
    result_filtered = result.text.replace("jarfish: ", "").replace("jarfish-bot: ", "").replace("JarfishBot: ", "")
    for response_part in textwrap.wrap(result_filtered, 1999, expand_tabs=False, replace_whitespace=False, drop_whitespace=False,):
        memory.store_message(chatroom_id=str(update.message.chat.id), message=f"jarfish: {response_part}")
        await context.bot.send_message(chat_id=update.message.chat.id, text=response_part)
    return
