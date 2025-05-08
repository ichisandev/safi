import pydantic
import os
import json
import gspread
import pytz

from datetime import datetime
from pydantic_ai import Agent
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from ..chatbot import memory
from utils import config

trigger_words = ["catatan utang", "catat utang", "catatan hutang", "catat hutang", "catatkan utang", "catatkan hutang"]

class Entry(pydantic.BaseModel):
    nama_pengutang: str
    barang: str
    harga: str
    keterangan: str

class EntryRequest(pydantic.BaseModel):
    nama_pembayar: str
    entry: list[Entry] 

agent = Agent(
    model=config.GENAI_MODEL,
    result_type=EntryRequest,
    system_prompt="selidikilah riwayat chat berikut! buatlah pencatatan utang dari permintaan terakhir",
)

def parse_response(response):
    now = datetime.now(pytz.timezone('Asia/Jakarta'))
    formatted_date = now.strftime("%d-%m-%Y")
    data = []
    for entry in response.data.entry:
        data.append([
            formatted_date,
            entry.barang,
            entry.harga,
            entry.keterangan,
            response.data.nama_pembayar,
            entry.nama_pengutang,
            "Belum diterima",
            "Belum dibayar"
        ])
    return data

DB_FILE = "database.json"

def read_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"rooms": []}

def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_room(room_id, sheet_id):
    db = read_db()
    db["rooms"].append({"room_id": room_id, "sheet_id": sheet_id})
    write_db(db)

def get_room_id(room_id):
    db = read_db()
    room = next((room for room in db["rooms"] if room["room_id"] == room_id), None)
    return room["sheet_id"]

async def create_new_sheet(update, credentials):
    NOTE_TEMPLATE_SHEET_ID = os.environ.get("NOTE_TEMPLATE_SHEET_ID")
    drive_service = build('drive', 'v3', credentials=credentials)
    try:
        room_name = str(update.message.chat.title)
    except:
        room_name = str(update.message.chat.first_name)
    file_metadata = {
        'name': f'Catatan Utang {room_name}',
        'parents': ['root']
    }
    response = await drive_service.files().copy(
        fileId=NOTE_TEMPLATE_SHEET_ID,
        body=file_metadata
    ).execute()
    new_sheet_id = response.get('id')
    permission = {
        'type': 'anyone',
        'role': 'writer'
    }
    await drive_service.permissions().create(
        fileId=new_sheet_id,
        body=permission
    ).execute()
    add_room(str(update.message.chat.id), new_sheet_id)
    return new_sheet_id


async def main(update, context):
    load_dotenv()
    SERVICE_ACCOUNT_FILE = 'gapi-credentials.json'
    SCOPES = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    try:
        sheet_id = get_room_id(str(update.message.chat.id))
    except:
        sheet_id = await create_new_sheet(update, credentials)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(sheet_id)
    sheet_name = spreadsheet.title
    worksheet = spreadsheet.sheet1
    first_empty_row = len(list(filter(None, worksheet.col_values(1)))) + 1
    prompt = memory.get_chat_history(str(update.message.chat.id))
    response = await agent.run(prompt)
    parsed_data = parse_response(response)
    for data in parsed_data:
        worksheet.insert_row(data, first_empty_row)
    message = f"Catatan utang berhasil diupdate!! silakan periksa link berikut: https://docs.google.com/spreadsheets/d/{sheet_id}/edit !"
    await context.bot.send_message(chat_id=update.message.chat.id, text=message)
    memory.store_message(chatroom_id=str(update.message.chat.id), message=f"safi: {message}")
    return
