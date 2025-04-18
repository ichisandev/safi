from os import wait
import re
import traceback

from utils import logger, config
from servicess.chatbot import memory, chatbot, regex, autochat
from servicess.embed_component import poll, generate_image


async def route(update, context):
    auto_chatbot = False
    username = str(update.message.from_user.first_name)
    if str(update.message.from_user.last_name).lower() != "none":
        username += " " + str(update.message.from_user.last_name)
    user_message = str(update.message.text)
    # if str(message.reply["content"]) != user_message:
        # print("replied")
        # user_message += f" (mereply ke [{str(message.reply.author)}: {str(message.reply.content)}])"
    if update.message.photo:
        user_message += " *mengirim attachment*"
    # if message.reply.attachments:
        # message.attachments.append(message.reply.attachments)
    memory.store_message(chatroom_id=str(update.message.chat.id), message=f"{username}: {user_message}")
    logger.message_print(update.message)

    # if message.author.id in config.ADMIN_IDS:
    #     if str(message.text).startswith("exec"):
    #         command = str(message.content).replace("exec ", "")
    #         try:
    #             if command.startswith("print"):
    #                 command = command.replace("print ", "")
    #                 await message.channel.send(eval(command))
    #             else:
    #                 exec(command)
    #                 await message.channel.send("exec success")
    #             return
    #         except Exception as e:
    #             traceback.print_exc()
    #             result = get_serializable_dict(e.__dict__)
    #             await message.channel.send("exec failed")
    #             await message.channel.send(result)
    #             return

    engage_chatbot = re.search(regex.get_regex(), user_message.lower())
    if update.message.text == "jarfish reset":
        del memory.chat_histories[str(update.message.chat.id)]
        return
    try:
        if str(update.message.title).lower() in config.AUTOCHAT_CHANNEL:
            if memory.chat_histories[str(update.message.chat.id)]["counter"]>=config.AUTOCHAT_START_RATE:
                auto_chatbot = autochat.gacha(update.message)
    except:
        pass
    if engage_chatbot or auto_chatbot:
        memory.chat_histories[str(update.message.chat.id)]["counter"] = 0
        try:
            if "poll" in str(update.message.text).lower():
                await poll.main(update, context)
            elif any(word in str(update.message.text).lower() for word in generate_image.trigger_words):
                await generate_image.main(update, context)
            else:
                await chatbot.main(update, context)
        except Exception as e:
            traceback.print_exc()
            result = get_serializable_dict(e.__dict__)
            await context.bot.send_message(chat_id=update.message.chat.id, text=str(result))
            return


def get_serializable_dict(json_obj):
    import json

    serializable_dict = {}
    for key, value in json_obj.items():
        try:
            json.dumps(value)
            serializable_dict[key] = value
        except Exception:
            pass
    return serializable_dict
