from io import BytesIO
import base64
from PIL import Image

async def get_image_base64(photo, context):
    file = await context.bot.get_file(photo.file_id)
    byte_stream = BytesIO()
    await file.download_to_memory(out=byte_stream)
    byte_stream.seek(0)
    image_data = base64.b64encode(byte_stream.read()).decode("utf-8")
    return image_data

async def get_image_pillow(photo, context):
    file = await context.bot.get_file(photo.file_id)
    byte_stream = BytesIO()
    await file.download_to_memory(out=byte_stream)
    byte_stream.seek(0)
    image_data = Image.open(byte_stream)
    return image_data
