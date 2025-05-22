from PIL import Image, ImageDraw
from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import requests
import io

class BoundingBox(BaseModel):
    label: str
    xmin: float
    ymin: float
    xmax: float
    ymax: float

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

config={
        'response_mime_type': 'application/json',
        'response_schema': list[BoundingBox],
    }

def normalize_bbox(width, height, bbox):
    return [bbox[0]*width/1000, bbox[1]*height/1000, bbox[2]*width/1000, bbox[3]*height/1000]

async def send_bounding_box(message):
    image = Image.open(requests.get(message.attachments[0], stream=True).raw)
    width, height = image.size
    while width>1000 and height>1000:
        width = int(width/2)
        height = int(height/2)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    response = client.models.generate_content(
      model="gemini-1.5-pro",
      contents=[image, str(message.content)],
      config=config
    )
    for object_box in response.parsed:
        label = object_box.label
        bbox = [object_box.xmin, object_box.ymin, object_box.xmax, object_box.ymax]
        normalized_bbox = normalize_bbox(width, height, bbox)
        draw.rectangle(normalized_bbox, outline="red", width=5)
        draw.text((normalized_bbox[0], normalized_bbox[1]), label, fill= "yellow")
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    with io.BytesIO(img_byte_arr) as file:
        await message.channel.send(file=discord.File(file, "generated_bounding_box.png"))
    return

