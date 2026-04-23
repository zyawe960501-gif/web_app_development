# 系統架構設計文件 (ARCHITECTURE)

本文件基於 `docs/PRD.md` 中「線上撲克牌桌遊網站」的功能需求，規劃專案的技術架構、資料夾結構與元件職責。

---

## 1. 技術架構說明

本專案將不採用完全前後端分離的架構，而是由後端直接渲染頁面，以利快速打造 MVP 產品。以下是核心技術選型與其原因：

- **後端框架**：**Python + Flask**
  - **原因**：輕量且靈活，適合快速開發 MVP，並且有豐富的套件生態。
- **模板引擎**：**Jinja2**
  - **原因**：Flask 內建支援，能直接將後端資料注入 HTML，負責頁面的伺服器端渲染（SSR）。
- **即時通訊**：**Flask-SocketIO (WebSocket)**
  - **原因**：撲克牌對戰需要雙方「即時」看到發牌與對手出牌，傳統 HTTP 輪詢效率太差，WebSocket 是最佳解。
- **資料庫**：**SQLite (透過 SQLAlchemy ORM)**
  - **原因**：零配置、輕量化，適合小型專案與開發階段測試，ORM 則讓資料庫操作更直覺且易於未來擴充。

### Flask MVC 模式說明
整個應用程式採用類似 MVC (Model-View-Controller) 的設計模式來規劃職責：
- **Model (模型)**：負責定義資料庫表格（如 `User`、`Room` 等實體），並處理所有寫入、查詢等資料庫操作。
- **View (視圖)**：負責呈現給使用者的介面，這裡指的是 `templates/` 資料夾下的 HTML 與 Jinja2 檔案，以及前端 CSS/JS。
- **Controller (控制器)**：負責接收使用者請求、執行商業邏輯（如判斷勝負、執行洗牌演算法）並決定呼叫哪個 Model 或渲染哪個 View。在 Flask 中，Controller 就是定義在 `@app.route` 裡的邏輯，以及 `@socketio.on` 裡的 WebSocket 事件處理。

---

## 2. 專案資料夾結構

為了讓程式碼好維護，我們將各個元件分門別類，結構如下：

```text
online-poker-app/
├── app/                        ← 專案的核心應用程式目錄
│   ├── __init__.py             ← 初始化 Flask App, 資料庫與 SocketIO
│   ├── config.py               ← 全域設定檔 (如資料庫路徑、密鑰等)
│   ├── models/                 ← [Model] 資料表定義與操作
│   │   └── schemas.py          ← 使用者、房間等實體定義
│   ├── routes/                 ← [Controller] HTTP 請求路由
│   │   ├── main.py             ← 首頁大廳、建立房間等路由
│   │   └── room.py             ← 遊戲房間相關的路由
│   ├── sockets/                ← [Controller] WebSocket 即時連線事件
│   │   └── game_events.py      ← 發牌、出牌、狀態更新等事件處理
│   ├── templates/              ← [View] Jinja2 HTML 模板
│   │   ├── base.html           ← 共用排版 Layout
│   │   ├── index.html          ← 大廳首頁
│   │   └── room.html           ← 遊戲對戰桌面
│   └── static/                 ← 靜態資源檔案
│       ├── css/                ← 視覺設計與撲克牌樣式
│       ├── js/                 ← SocketIO 客戶端邏輯與動態效果
│       └── images/             ← 撲克牌圖檔與素材
├── instance/                   
│   └── database.db             ← SQLite 本機資料庫檔案 (自動產生)
├── docs/                       ← 專案設計文件 (PRD, ARCHITECTURE 等)
├── requirements.txt            ← 依賴套件清單 (Flask, Flask-SocketIO 等)
└── run.py                      ← 啟動伺服器的入口檔案
```

---

## 3. 元件關係圖

以下展示玩家透過瀏覽器操作時，系統各元件是如何互相溝通的：

```mermaid
flowchart TD
    User[玩家瀏覽器]
    
    subgraph Controller
        HTTP[Flask Routes\n(HTTP 請求)]
        WS[Flask-SocketIO\n(WebSocket 事件)]
    end
    
    subgraph Model
        DB_Model[SQLAlchemy 模型]
    end
    
    subgraph View
        Jinja[Jinja2 模板與靜態資源]
    end
    
    Database[(SQLite 資料庫)]
    
    %% HTTP Flow
    User -- "1. GET / 或 POST 建立房間" --> HTTP
    HTTP -- "2. 查詢/寫入資料" --> DB_Model
    DB_Model <--> Database
    HTTP -- "3. 傳遞變數並渲染" --> Jinja
    Jinja -- "4. 回傳完整 HTML 頁面" --> User
    
    %% WebSocket Flow
    User <== "雙向即時連線 (發牌/出牌)" ==> WS
    WS -- "驗證邏輯與更新狀態" --> DB_Model
    WS -- "廣播最新牌桌狀態" --> User
```

---

## 4. 關鍵設計決策

1. **混搭 HTTP 與 WebSocket：**
   - **原因**：大廳瀏覽、建立房間等低頻率操作使用傳統 HTTP 請求，可利用 Jinja2 快速開發介面並降低伺服器常駐連線負擔；進入遊戲後的「發牌」與「出牌」則改用 WebSocket，以滿足低延遲的遊戲對戰體驗。

2. **撲克牌核心邏輯放在後端 (Server-Authoritative)：**
   - **原因**：為了防止作弊，洗牌、發牌結果以及判斷勝負的邏輯都寫在後端的 Controller (`app/sockets/game_events.py`)。前端只負責「顯示」後端傳來的牌面資料，絕對不能在瀏覽器端使用 JavaScript 自行產生牌組。

3. **採用輕量級的 SQLite：**
   - **原因**：此專案 MVP 著重於功能驗證與快速上線，不需要複雜的關聯式資料庫設定。SQLite 足以應付目前儲存使用者暱稱與房間資訊的需求，且資料庫檔案 (`database.db`) 隨附於專案中，開發非常方便。

4. **使用 Bootstrap 或 Tailwind CSS 加速開發：**
   - **原因**：專案並非完全前後端分離，利用現成的 CSS 框架可以讓我們在 Jinja2 模板中快速刻出美觀的大廳與遊戲桌面，把主力放在 Flask 與 WebSocket 的連線開發上。
