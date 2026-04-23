# 雖然 api-design 主要是設計 HTTP Route，
# 但為配合 ARCHITECTURE.md 提及的防作弊即時對戰機制，這裡建立 SocketIO 骨架

def init_sockets(socketio):
    """
    註冊所有的 WebSocket 事件
    """
    
    @socketio.on('join_room')
    def handle_join_room(data):
        """
        處理玩家進入對戰房間的連線。
        讀取 room_code 將連線放入專屬的 Socket Room。
        當人數到達 2 人時，觸發洗牌與 game_start 廣播。
        """
        pass

    @socketio.on('play_card')
    def handle_play_card(data):
        """
        處理玩家出牌邏輯。
        驗證合法性後，將結果透過 'update_state' 廣播給同房玩家。
        如果達成勝利條件，則發出 'game_over' 廣播。
        """
        pass
