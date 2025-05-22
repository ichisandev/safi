import random

from . import memory
from utils import config

def gacha(message):
    chance = list(range(memory.chat_histories[str(message.channel.id)]["counter"]))
    rate = config.AUTOCHAT_SURE_RATE
    rng = random.randint(1, rate)
    if rng in chance:
        return True
    else:
        return False

