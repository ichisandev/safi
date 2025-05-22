import os
import google.generativeai as genai
from dotenv import load_dotenv

from utils import config

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name=config.GENAI_MODEL,
    system_instruction=config.SYSTEM_INSTRUCTION,
)
