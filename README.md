# 專案簡介

本專案是一個基於 Flask 的簡易專案/競標管理系統，主要結構與細節如下：

---

## 1. 專案結構

```
main.py                  # 啟動點，載入 Flask app
app/
    __init__.py          # 建立 Flask app、註冊 blueprint、初始化資料庫
    config.py            # 設定檔（資料庫、密鑰、管理者帳密等）
    extensions.py        # 初始化 db、login_manager 等擴充
    models.py            # 資料庫模型（User, Project, Bid）
    routes/
        __init__.py      # 匯入 blueprint
        auth.py          # 登入/註冊/登出等認證路由
        dashboard.py     # 儀表板頁面
        proposal_routes.py # 專案列表、提交、競標等功能
    templates/           # Jinja2 HTML 模板
    static/              # 靜態檔案（CSS等）
requirements.txt         # 依賴套件
render.yaml              # Render 部署設定
README.md                # 專案說明
```

---

## 2. 主要元件說明

- **models.py**
  - User：使用者帳號，含帳號、密碼雜湊、是否管理員。
  - Project：專案（可被競標），有標題、描述、建立時間。
  - Bid：競標紀錄，紀錄誰、何時對哪個專案競標。

- **routes**
  - auth.py：處理登入、登出、註冊等。
  - dashboard.py：登入後首頁，顯示專案數、用戶數、最新專案。
  - proposal_routes.py：
    - /proposal/list：專案列表。
    - /proposal/submit：提交新專案。
    - /proposal/projects/<project_id>/bid：對專案競標（僅限登入）。

- **app/__init__.py**
  - 建立 Flask app，載入設定，初始化資料庫、登入管理，註冊所有 blueprint。
  - 啟動時自動建立管理員帳號（根據環境變數）。

- **config.py**
  - 設定 Flask 祕鑰、資料庫連線、管理員帳密（可用環境變數覆蓋）。

- **templates/**
  - 各頁面 HTML 模板，配合 Jinja2 動態渲染。

---

## 3. 運作流程

1. 使用者註冊/登入（auth.py）。
2. 登入後可瀏覽 dashboard（dashboard.py）。
3. 可提交新專案（proposal_routes.py）。
4. 其他登入者可對專案競標（proposal_routes.py）。
5. 管理員帳號於啟動時自動建立（models.py/init_admin_account）。

---

## 4. 部署

- 依 requirements.txt 安裝依賴。
- 依 render.yaml 設定 Render 部署。
- 管理員帳密可用環境變數 ADMIN_USERNAME、ADMIN_PASSWORD 設定。

---

如需更細節的檔案或程式碼說明，請指定檔案或功能！
