from flask import Flask, request, render_template_string, redirect, url_for
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets 認證設定
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
service_account_info = json.loads(os.environ['GCP_CREDENTIALS'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
sheet = client.open("基層報修案件").sheet1

# HTML 表單模板
form_html = """
<!DOCTYPE html>
<html>
<head><title>選民服務表單</title></head>
<body>
  <h2>選民需求回報</h2>
  <form method="POST" action="/submit">
    <label>姓名：</label><br>
    <input type="text" name="name" required><br><br>
    
    <label>電話：</label><br>
    <input type="text" name="phone" required><br><br>
    
    <label>需求說明：</label><br>
    <textarea name="description" rows="4" cols="40" required></textarea><br><br>
    
    <button type="submit">送出</button>
  </form>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(form_html)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    phone = request.form.get("phone")
    description = request.form.get("description")
    
    # 寫入 Google Sheets（加一列）
    sheet.append_row([name, phone, description])
    
    return "<h3>感謝您的回報！我們會盡快處理。</h3>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

'''
| 欄位名稱                            | 說明                                                               | 如何取得                     |
| ------------------------------- | ---------------------------------------------------------------- | ------------------------ |
| `"type"`                        | 固定為 `"service_account"`                                          | 系統自動填入                   |
| `"project_id"`                  | 你的 Google Cloud 專案 ID（例如：`my-gcp-project-123`）                   | GCP 控制台首頁 / 左上方導航列       |
| `"private_key_id"`              | Google 產生的憑證 ID，用來辨識私鑰                                           | 建立憑證時自動產生                |
| `"private_key"`                 | 你的私密金鑰（PEM 格式，會以多行 `-----BEGIN PRIVATE KEY-----` 開頭）             | 建立憑證時自動產生                |
| `"client_email"`                | 服務帳戶的 Email（例如：`mvp-bot@my-gcp-project.iam.gserviceaccount.com`） | 在 IAM → 服務帳戶 → 點服務帳戶即可看到 |
| `"client_id"`                   | GCP 系統分配的帳戶 ID                                                   | 同上，會出現在 JSON 檔           |
| `"auth_uri"`                    | 固定為 `https://accounts.google.com/o/oauth2/auth`                  | 標準 Google 認證網址           |
| `"token_uri"`                   | 固定為 `https://oauth2.googleapis.com/token`                        | 標準 Google token API      |
| `"auth_provider_x509_cert_url"` | 固定為 Google 的憑證 URL                                               | 標準值                      |
| `"client_x509_cert_url"`        | 對應該服務帳戶的公開憑證 URL                                                 | 自動生成，通常不需修改              |


📥 如何下載 JSON 憑證
登入 Google Cloud Console
選擇你要的專案
點左側「IAM 與管理」>「服務帳戶」
建立新的服務帳戶，或點進現有服務帳戶
點「金鑰」頁籤 → 點「新增金鑰」
選擇「JSON」格式並下載
✅ 這時你就會拿到含上述所有欄位的 .json 檔案！
'''
