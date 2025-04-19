import pydantic
from pydantic_ai import Agent

from ..chatbot import memory
from utils import config


class PollRequest(pydantic.BaseModel):
    poll_question: str = pydantic.Field(description="buat pertanyaan kurang dari 250 karakter")
    poll_choice: list[str] = pydantic.Field(description="minimal 2 pilihan, maksimal 10 pilihan")


agent = Agent(
    model=config.GENAI_MODEL,
    result_type=PollRequest,
    system_prompt=config.SYSTEM_INSTRUCTION + "\nbuat poll dari permintaan terakhir",
)

async def main(update, context):
    prompt = memory.get_chat_history(str(update.message.chat.id))
    response = await agent.run(prompt)
    await context.bot.send_poll(
        chat_id=update.message.chat.id,
        question=response.data.poll_question,
        options=response.data.poll_choice,
        is_anonymous=False
    )
    memory.store_message(chatroom_id=str(update.message.chat.id), message=f"{config.BOT_NAME}: *sending poll, question={response.data.poll_question}, options={response.data.poll_choice}")
    return
