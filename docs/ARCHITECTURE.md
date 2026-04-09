# 系統架構設計文件 (ARCHITECTURE) - 線上桌遊系統

這份文件基於 `docs/PRD.md` 的功能需求，規劃線上桌遊系統的技術細節、架構與資料夾結構。

---

## 1. 技術架構說明

本專案採用的核心技術棧如下：
- **後端框架**：**Python + Flask**，負責處理商業邏輯、使用者驗證與整體頁面路由。
- **模板引擎**：**Jinja2**，用於處理伺服器端 HTML 頁面渲染（Server-Side Rendering），因此不採用完全前後端分離，以求快速實現介面。
- **即時通訊**：**Flask-SocketIO** (WebSocket)，負責處理遊戲對戰連線、發牌、動作同步與即時聊天。
- **前端呈現**：**HTML5 / 原生 CSS / JavaScript**，處理視覺排版、動態發牌特效，以及建立與後端的 WebSocket 端點。
- **資料庫**：**SQLite (建議透過 SQLAlchemy ORM 作操作)**，存放結構化資料（如使用者資訊、歷史積分、房間紀錄等）。

### MVC 架構模式說明
整個應用程式將基於經典的 MVC（Model-View-Controller）模式變體來設計：
- **Model (模型)**：由 SQLAlchemy 定義對應 SQLite 的表格實體（Entity），例如 `User`, `Room`, `MatchRecord`。主要負責處理資料操作與儲存。
- **View (視圖)**：由 Jinja2 模板結合前端 CSS/JS 呈現給使用者的介面層，例如註冊表單大廳清單以及對戰用的桌布畫面。
- **Controller (控制器)**：包含傳統的 Flask Route (`@app.route`) 與連線用的 Socket events (`@socketio.on`)。負責接收使用者請求、進行安全與防作弊驗證、實施遊戲核心邏輯（如洗牌機制），決定呼叫哪個 Model 修改資料，最終調用 View 渲染結果。

---

## 2. 專案資料夾結構

建議採用以下的資料夾結構，以達到模組化及易於維護的目的：

```text
online-board-game/
├── app/                        ← 應用程式核心目錄
│   ├── __init__.py             ← 載入設定、初始化 Flask App、DB 等
│   ├── config.py               ← 全域配置變數 (Database URL, Secret Keys)
│   ├── models/                 ← [Model] 資料庫實體定義
│   │   ├── __init__.py
│   │   ├── user.py             ← 使用者帳號與基本屬性
│   │   └── game.py             ← 遊戲積分歸檔、房間等資料表
│   ├── routes/                 ← [Controller] Flask 路由 (HTTP 請求)
│   │   ├── __init__.py
│   │   ├── auth.py             ← 處理註冊、登入與登出流程
│   │   └── main.py             ← 處理大廳、個人戰績排行榜等首頁邏輯
│   ├── sockets/                ← [Controller] 即時連線邏輯 (WebSocket 請求)
│   │   ├── __init__.py
│   │   └── events.py           ← 負責發牌、玩家行動同步、聊天廣播等事件
│   ├── templates/              ← [View] Jinja2 網頁模板
│   │   ├── base.html           ← 共用的網頁主版 Layout
│   │   ├── auth/               ← 登入、註冊表單畫面
│   │   └── game/               ← 遊戲大廳、對戰專屬房間桌面
│   └── static/                 ← 靜態資源檔案
│       ├── css/                ← 視覺樣式與動態效果 (含卡牌翻轉動畫)
│       ├── js/                 ← 前端互動腳本與 Socket.IO 用戶端邏輯
│       └── images/             ← 頭像、卡牌圖示、UI 素材
├── instance/                   ← 運作時產生的自動建立檔案與敏感資料
│   └── database.db             ← SQLite 資料庫本體
├── docs/                       ← 專案設計文件 (PRD, ARCHITECTURE 等)
├── requirements.txt            ← Python 環境套件清單
└── run.py                      ← 系統進入點 (Python Entry Point)
```

---

## 3. 元件關係圖

以下展示了「連線操作與資料」如何在客戶端與後端之間流動的形式：

```mermaid
flowchart TD
    Browser[瀏覽器 - 玩家介面]
    
    %% Flask Routes
    RouteMain[Flask HTTP 路由\n(Controller)]
    RouteSockets[WebSocket 事件\n(SocketIO Controller)]
    
    %% Backend internal
    JinjaView[Jinja2 模板與靜態檔案\n(View)]
    SQLModel[SQLAlchemy ORM\n(Model)]
    SQLite[(SQLite 資料庫)]
    
    %% 一般操作
    Browser -- "HTTP GET/POST 獲取畫面與登入" --> RouteMain
    RouteMain -- "獲取與核對資料" --> SQLModel
    SQLModel <--> SQLite
    RouteMain -- "將上下文傳遞給模板" --> JinjaView
    JinjaView -- "渲染回傳 HTML" --> Browser
    
    %% 遊戲內操作
    Browser <== "雙向連線 ( Socket 事件處理 )" ==> RouteSockets
    RouteSockets -- "驗證出牌、發送聊天廣播" --> Browser
    RouteSockets -- "結算分數與寫入勝敗紀錄" --> SQLModel
```

---

## 4. 關鍵設計決策

1. **傳統 HTTP 與 WebSocket (SocketIO) 雙管齊下：**
   - **原因：** 使用者查看排行榜、登入帳號等操作並不講求極度即時，這部分保留傳統 HTTP 請求可以節省常駐連線資源；真正的核心操作：「進入房間」與「對手進行發牌對戰」，因需要「對手動作立刻顯示在我螢幕上」的雙向推播，於是交由 WebSockets 處理，確保極低的傳輸延遲與順暢度。

2. **維持 Jinja2 渲染而不採前端框架（如 React / Vue）：**
   - **原因：** MVP 時期講求能夠快速開發、展示出基礎功能並降低複雜度。不採取前後端分離，可省去大量的 API 規格設計以及跨網域請求 (CORS) 設定等阻礙，讓專案能直接以 Python 後端緊扣畫面渲染，團隊也能減少技術學習與開發的成本。

3. **遊戲核心防作弊與安全性設計：**
   - **原因：** 如果所有邏輯都寫在 JavaScript (瀏覽器端) 會使得玩家能輕易「偷看牌」或「決定發牌結果」。因此洗牌的隨機亂數演算法、抽牌動作驗證，以及遊戲結算邏輯全都放置於 `app/sockets/events.py` (Controller) 中實作以確保遊戲公平。

4. **採用 SQLite 結合 SQLAlchemy ORM：**
   - **原因：** 本專案為概念開發與小型驗證用途，不須一開始就耗費時間建立像 MySQL 這樣的大規模伺服器。SQLite 不需要額外的伺服器執行環境即可將其放在 `instance/` 分區，結合 SQLAlchemy ORM 使用後，如果後續系統長大需要切換至進階資料庫，僅需修改 `config.py` 連線字串即可，極大程度保障未來可擴充性。
