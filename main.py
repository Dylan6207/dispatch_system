import gspread
from oauth2client.service_account import ServiceAccountCredentials
from linebot import LineBotApi
from linebot.models import TextSendMessage

# ========= 1) Google Sheets 認證 =========
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials/your_service_account.json', scope)
client = gspread.authorize(creds)

# 打開你的 Sheet
sheet = client.open("基層報修案件").sheet1

# 讀最新一筆
data = sheet.get_all_records()
latest = data[-1]

案件內容 = f"""
📌 新進案件通知
案件類型：{latest['案件類型']}
地點：{latest['地點']}
描述：{latest['描述']}
聯絡人：{latest['聯絡人']} {latest['電話']}
"""

# ========= 2) LINE OA 發送訊息 =========
line_bot_api = LineBotApi('YOUR_LINE_CHANNEL_ACCESS_TOKEN')

# 助理或群組的 User ID
line_bot_api.push_message(
    'YOUR_USER_ID',
    TextSendMessage(text=案件內容)
)

print("✅ 已發送 LINE 通知！")
