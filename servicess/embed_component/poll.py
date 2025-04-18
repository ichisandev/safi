import pydantic
from pydantic_ai import Agent
# import discord
import traceback

from ..chatbot import memory
from utils import config


class PollChoice(pydantic.BaseModel):
    choice: str
    choice_emoji: str = pydantic.Field(description="hanya satu karakter emoji")


class PollRequest(pydantic.BaseModel):
    poll_question: str = pydantic.Field(description="buat pertanyaan kurang dari 250 karakter")
    poll_choice: list[PollChoice] = pydantic.Field(description="minimal 2 pilihan, maksimal 10 pilihan")


agent = Agent(
    model=config.GENAI_MODEL,
    result_type=PollRequest,
    system_prompt=config.SYSTEM_INSTRUCTION + "buat poll dari permintaan terakhir",
)


def parse_poll(response):
    title = "📊 " + response.data.poll_question
    description = "\n".join(f"{choice.choice_emoji} {choice.choice}" for choice in response.data.poll_choice)
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    return embed


async def main(message):
    prompt = memory.get_chat_history(str(message.channel.id))
    response = await agent.run(prompt)
    embed = parse_poll(response)
    poll_message = await message.channel.send(embed=embed)
    for choice in response.data.poll_choice:
        await poll_message.add_reaction(choice.choice_emoji)
    return
