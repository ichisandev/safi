from . import message_router


async def route(update, context):
    if update.message:
        await message_router.route(update, context)
