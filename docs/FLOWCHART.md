# 系統流程圖與使用者流程 (FLOWCHART)

本文件基於 `docs/PRD.md` 的需求與 `docs/ARCHITECTURE.md` 的技術架構，定義出「線上撲克牌桌遊網站」的使用者操作路徑與系統資料流。

---

## 1. 使用者流程圖 (User Flow)

這張圖描述了玩家從進入網站到完成一局遊戲的完整操作路徑。

```mermaid
flowchart TD
    A([玩家進入網站]) --> B[大廳首頁]
    B --> C{選擇操作}
    
    C -->|輸入暱稱| D[建立新房間]
    C -->|輸入暱稱與房號| E[加入特定房間]
    C -->|點擊快速配對| F[系統尋找空房間加入]
    
    D --> G[進入遊戲房間]
    E --> G
    F --> G
    
    G --> H{房間人數是否到齊？}
    H -->|否| I[顯示等待對手畫面]
    I --> H
    H -->|是| J[遊戲開始：系統自動洗牌發牌]
    
    J --> K[玩家回合輪替：操作與出牌]
    K --> L{滿足結束條件？}
    L -->|否| K
    L -->|是| M[顯示結算畫面與勝負]
    
    M --> N{選擇下一步}
    N -->|再來一局| G
    N -->|離開房間| B
```

---

## 2. 系統序列圖 (Sequence Diagram)

這張圖描述了「玩家建立/加入房間」到「系統發牌與即時對戰」背後的技術實作流程，包含傳統 HTTP 請求與 WebSocket 的交替使用。

```mermaid
sequenceDiagram
    actor User as 玩家
    participant Browser as 瀏覽器 (前端)
    participant Flask as Flask (HTTP Controller)
    participant Socket as Flask-SocketIO (WebSocket)
    participant DB as SQLite (Model)

    %% 房間建立與進入
    User->>Browser: 填寫暱稱點擊「建立房間」
    Browser->>Flask: POST /room/create (表單資料)
    Flask->>DB: INSERT 新增玩家與房間資料
    DB-->>Flask: 回傳房間 ID
    Flask-->>Browser: HTTP 302 重新導向 /room/{room_id}
    
    %% WebSocket 連線建立
    User->>Browser: 進入房間畫面
    Browser->>Socket: 建立 WebSocket 連線
    Browser->>Socket: emit('join_room', {room_id, user_id})
    Socket->>Socket: 將連線加入對應的 Socket 房間
    Socket-->>Browser: 廣播 emit('player_joined')，更新畫面人數
    
    %% 遊戲開始
    Note over User, DB: 當對手加入，房間人數滿 2 人
    Socket->>Socket: 後端觸發洗牌與分配手牌邏輯
    Socket-->>Browser: emit('game_start', {玩家專屬手牌資料})
    Browser-->>User: 渲染卡牌，顯示「你的回合」
    
    %% 對戰互動
    User->>Browser: 點擊卡牌出牌
    Browser->>Socket: emit('play_card', {card_id})
    Socket->>Socket: 驗證合法性並更新遊戲狀態
    Socket-->>Browser: 廣播 emit('update_state', {桌面最新狀態})
    Browser-->>User: 畫面同步顯示雙方最新卡牌
```

---

## 3. 功能清單對照表

此表列出了主要功能所對應的 URL 路徑、通訊協定與方法：

| 功能名稱 | URL 路徑 / Event 名稱 | 協定與方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **進入首頁大廳** | `/` | HTTP `GET` | 顯示輸入暱稱與選擇操作的介面。 |
| **建立房間** | `/room/create` | HTTP `POST` | 接收暱稱，在資料庫建立房間後重新導向至房間頁面。 |
| **加入房間** | `/room/<room_id>` | HTTP `GET` | 進入特定的遊戲房間畫面並載入基本前端資源。 |
| **加入即時連線** | `join_room` | WS `emit` | 前端建立連線後，主動告知後端將自己加入該 Socket 房間。 |
| **開始遊戲與發牌** | `game_start` | WS `broadcast` | 當人數到齊，後端自動洗牌並推播各自的手牌給對應玩家。 |
| **玩家出牌** | `play_card` | WS `emit` | 玩家進行遊戲操作時，傳送出牌動作給後端。 |
| **更新遊戲狀態** | `update_state` | WS `broadcast` | 後端驗證出牌後，將最新牌桌資訊與當前輪替玩家推播給所有人。 |
| **遊戲結算** | `game_over` | WS `broadcast` | 達成勝利條件時推播結果，前端渲染勝負結算畫面。 |
