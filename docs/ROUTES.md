# 路由設計文件 (ROUTES)

本文件基於前面的設計文件，定義「線上撲克牌桌遊網站」的 HTTP 路由與 WebSocket 事件規劃，供前後端開發與串接參考。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **大廳首頁** | `GET` | `/` | `main/index.html` | 顯示輸入暱稱表單以及「建立房間」、「加入特定房間」、「快速配對」的操作按鈕。 |
| **建立房間** | `POST` | `/room/create` | — | 接收玩家暱稱，在 DB 建立 User 與 Room，成功後重導向至房間頁面。 |
| **加入特定房間** | `POST` | `/room/join` | — | 接收暱稱與特定的 6 碼房號，將玩家設為 guest 後重導向至房間頁面。 |
| **快速配對** | `POST` | `/room/quick_match` | — | 接收暱稱，由系統隨機尋找 `status='waiting'` 且有空位的房間，並重導向過去。 |
| **遊戲房間頁** | `GET` | `/room/<room_code>` | `room/game.html` | 顯示遊戲對戰桌布，並在此頁面載入 Socket.IO 的 JS 腳本建立連線。 |

### WebSocket 事件清單 (補充)

由於專案核心對戰依賴 SocketIO，以下為對應的事件規劃：

| 功能 | 類型 (Emit/Broadcast) | Event 名稱 | 說明 |
| :--- | :--- | :--- | :--- |
| **加入房間** | `Client -> Server` | `join_room` | 前端載入畫面後，傳送 `room_code` 與 `user_id` 加入 WebSocket 房間。 |
| **遊戲開始** | `Server -> Client` | `game_start` | 人數到齊後，伺服器洗牌並廣播手牌給對應玩家。 |
| **玩家出牌** | `Client -> Server` | `play_card` | 玩家在自己的回合出牌時觸發，傳送卡牌資訊。 |
| **狀態更新** | `Server -> Client` | `update_state` | 伺服器驗證出牌後，廣播最新的桌面狀態（誰的回合、出了什麼牌）。 |
| **遊戲結算** | `Server -> Client` | `game_over` | 滿足勝利條件時，廣播勝負結果。 |

---

## 2. 每個路由的詳細說明

### `GET /`
- **輸入**：無。
- **處理邏輯**：單純渲染首頁畫面，不需讀取資料庫。
- **輸出**：渲染 `main/index.html`。

### `POST /room/create`
- **輸入**：表單欄位 `nickname` (玩家暱稱)。
- **處理邏輯**：
  1. 呼叫 `User.create(nickname)`。
  2. 產生一組隨機 6 碼字串作為 `room_code`。
  3. 呼叫 `Room.create(room_code, host_id)`。
  4. 將 `user_id` 存入 Flask Session 中。
- **輸出**：重導向至 `/room/<room_code>`。
- **錯誤處理**：如果暱稱空白，回傳 400 錯誤或 flash 訊息並重導向回 `/`。

### `POST /room/join`
- **輸入**：表單欄位 `nickname`、`room_code`。
- **處理邏輯**：
  1. 尋找該 `room_code` 的房間。
  2. 確保房間狀態為 `waiting` 且 `guest_id` 為空。
  3. 建立 `User` 並將 `user_id` 存入 Session。
  4. 呼叫 `Room.join_room()` 更新房間資訊。
- **輸出**：重導向至 `/room/<room_code>`。
- **錯誤處理**：若房間不存在或已滿，flash 錯誤訊息並重導向回 `/`。

### `POST /room/quick_match`
- **輸入**：表單欄位 `nickname`。
- **處理邏輯**：
  1. 查詢 DB 中第一個 `status == 'waiting'` 的房間。
  2. 建立 `User` 並存入 Session。
  3. 若找不到房間，則自動幫玩家轉為呼叫 `/room/create` 邏輯。
  4. 否則呼叫 `Room.join_room()` 加入該空房間。
- **輸出**：重導向至 `/room/<room_code>`。

### `GET /room/<room_code>`
- **輸入**：URL 參數 `room_code`，以及 Session 中的 `user_id`。
- **處理邏輯**：
  1. 驗證該房間是否存在。
  2. 驗證當前 `user_id` 是否為該房間的 `host_id` 或 `guest_id`（防偷窺）。
- **輸出**：渲染 `room/game.html` 並將 `room_code`, `user_id` 注入模板。
- **錯誤處理**：無權限或房間不存在則回傳 403 / 404 錯誤頁面。

---

## 3. Jinja2 模板清單

所有的模板都放在 `app/templates/` 目錄中：

1. **`base.html`**
   - 包含基礎的 HTML5 骨架、載入 Bootstrap CSS/JS 以及 SocketIO 用戶端腳本。
   - 提供 `{% block content %}{% endblock %}` 供子模板繼承。
2. **`main/index.html`**
   - 繼承自 `base.html`。
   - 畫面中央有簡單的 Logo 與三組表單按鈕對應 POST 路由。
3. **`room/game.html`**
   - 繼承自 `base.html`。
   - 對戰桌面，分為對手區域（上方）、共用牌桌（中央）、玩家手牌（下方）。
   - 包含處理 SocketIO 事件的前端 JavaScript 區塊。
