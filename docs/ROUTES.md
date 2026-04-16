# 路由與頁面設計文件 (ROUTES)

本文件依據 `docs/PRD.md`、`docs/FLOWCHART.md` 與 `docs/DB_DESIGN.md` 定義系統所有的 Flask HTTP 路由、對應的處理邏輯與 Jinja2 模板清單，作為後端邏輯與前端介面整合的標準文件。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁重導向 | GET | `/` | — | 將造訪者重新導向至 `/lobby` 或登入頁 |
| 註冊首頁 | GET | `/auth/register` | `templates/auth/register.html` | 顯示使用者註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 接收帳號密碼，建立 User，完成後導向登入頁 |
| 登入首頁 | GET | `/auth/login` | `templates/auth/login.html` | 顯示使用者登入表單 |
| 處理登入 | POST | `/auth/login` | — | 驗證密碼，成功後建立 Session 並導向 `/lobby` |
| 使用者登出 | GET | `/auth/logout` | — | 清除 Session 改為未登入狀態，導向 `/auth/login` |
| 遊戲大廳 | GET | `/lobby` | `templates/game/lobby.html` | 取得等待中公開房間，顯示列表與新增按鈕 |
| 建立房間 | POST | `/api/room/create` | — | 於 DB 建立新 Room 記錄並導向 `/room/<room_id>` |
| 遊戲桌面 | GET | `/room/<room_id>` | `templates/game/room.html` | 該場對戰桌面，連線 WebSocket，開始遊戲 |
| 戰績與排行 | GET | `/leaderboard` | `templates/game/leaderboard.html`| 查詢積分排名與該名玩家的歷史成績紀錄 |

## 2. 每個路由的詳細說明

### 2.1 首頁與大廳
- **GET `/`**
  - **處理邏輯**：檢查 session 是否已登入。
  - **輸出**：有登入重導向 `/lobby`，未登入重導向 `/auth/login`。
- **GET `/lobby`**
  - **處理邏輯**：檢查登入狀態。調用 `Room.get_all_waiting_public()` 取得所有等待中房間。
  - **輸出**：渲染 `templates/game/lobby.html`，傳遞 `rooms` 與 目前使用者資料給前端。

### 2.2 帳號與身份驗證 (Auth)
- **GET `/auth/register`**
  - **輸出**：渲染 `register.html` 註冊表單頁面。
- **POST `/auth/register`**
  - **輸入**：表單欄位 `username`, `password`。
  - **處理邏輯**：將密碼以 bcrypt 加密，呼叫 `User.create()`。若帳號已存在則產生 flash error。
  - **輸出**：重導向 `/auth/login`。
- **GET `/auth/login`**
  - **輸出**：渲染 `login.html` 進入系統。
- **POST `/auth/login`**
  - **輸入**：表單欄位 `username`, `password`。
  - **處理邏輯**：找尋 User、查核密碼是否正確，設定 session。
  - **輸出**：成功導向 `/lobby`，失敗則返回 `login.html` 並快顯錯誤。
- **GET `/auth/logout`**
  - **處理邏輯**：將使用者的 session (`user_id`) 清除。

### 2.3 房間與遊戲對戰 (Game & Room)
- **POST `/api/room/create`**
  - **輸入**：透過表單或按鈕提交房間名稱 `name` 與 `is_private`。
  - **處理邏輯**：驗證是否登入。呼叫 `Room.create()`，設定房主。
  - **輸出**：重導向至 `GET /room/<新增的room_id>`。
- **GET `/room/<room_id>`**
  - **輸入**：路徑參數 `room_id`。
  - **處理邏輯**：擷取 Room 狀態，確認使用者是否為兩名參與者之一或房間尚未滿員。
  - **輸出**：渲染 `templates/game/room.html`，並向前端暴露該房間 ID 供 WebSocket 腳本連線使用。若房間不存在或無權加入則顯示 404/錯誤，重導回 lobby。
- **GET `/leaderboard`**
  - **處理邏輯**：從 DB 透過 sqlalchemy 排序出全服最高分玩家 (limit 10)，以及取得目前登入者的所有 `MatchRecord`。
  - **輸出**：渲染 `templates/game/leaderboard.html`，並帶入參數排行榜、歷史場次。

## 3. Jinja2 模板清單

所有的模板將繼承共用的佈局框架，確保外觀一致以及全站都能載入 Bootstrap 或共通 CSS。

1. **`templates/base.html`**：主頁面框架，包含導覽列、Flash message 與區塊 `{% block content %}`。所有檔案皆繼承自此。
2. **`templates/auth/login.html`**：使用者登入表單。
3. **`templates/auth/register.html`**：使用者註冊表單。
4. **`templates/game/lobby.html`**：大廳畫面，包含「可加入的房間區塊」、「創建房間按鈕/Modal」。
5. **`templates/game/room.html`**：綠色的桌遊桌面，會有卡牌展示區、對手出牌區以及右下方的實時聊天對話視窗。
6. **`templates/game/leaderboard.html`**：含有成績列表與排行榜表格的綜合統計資訊頁。

## 4. 路由骨架程式碼
骨架程式碼已在 `app/routes/` 下自動產生對應的 `auth.py` 與 `main.py` 內容（依循 Flask Blueprint 架構設計）。
