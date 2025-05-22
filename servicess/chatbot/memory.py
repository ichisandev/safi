from collections import deque
import sched, time, asyncio

from utils import config

# Dictionary to store chat histories per chatroom
chat_histories = {}
last_chat_history = {}
args_histories = {}


def store_message(chatroom_id, message):
    # If chatroom doesn't exist, initialize it with a deque
    if chatroom_id not in chat_histories:
        chat_histories[chatroom_id] = {}
        chat_histories[chatroom_id]["message"] = deque(maxlen=config.MAX_MESSAGES)
        chat_histories[chatroom_id]["counter"] = 0

    # Append the message to the chatroom's history
    chat_histories[chatroom_id]["message"].append(message)
    
    # Add counter
    chat_histories[chatroom_id]["counter"] += 1

def get_chat_history(chatroom_id):
    return "".join(f"{chat}\n" for chat in chat_histories[chatroom_id]["message"])


def store_args(args):
    args_histories[args.chatroom_id] = args


def get_args(chatroom_id):
    return args_histories[chatroom_id]

def clear_counter(scheduler):
    scheduler.enter(config.AUTOCHAT_PERIOD, 1, clear_counter, (scheduler,))
    print("clearing counter")
    for key in chat_histories.keys():
        chat_histories[key]["counter"]=0

clear_counter_scheduler = sched.scheduler(time.time, time.sleep)

async def run_cc_scheduler():
    while True:
        clear_counter_scheduler.run(blocking=False)
        await asyncio.sleep(1)
