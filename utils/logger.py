from servicess.chatbot import memory
from utils import config

# print message info in terminal
def message_print(message):
    print(message)
    # print(message.author)
    print(memory.get_chat_history(str(message.chat.id)))
    # print(message.referenced_message)
