from flask import render_template, request, redirect, url_for, flash, session, abort
from . import main_bp

@main_bp.route('/')
def index():
    """
    預設進入點，依照使用者的登入狀態。
    - 若已登入，重導向至大廳 (`/lobby`)。
    - 若未登入，重導向至登入頁面 (`auth.login`)。
    """
    pass

@main_bp.route('/lobby')
def lobby():
    """
    遊戲大廳首頁。
    取得目前的公開空房間並渲染給前端，附帶個人資訊以及房間一覽表。
    """
    pass

@main_bp.route('/api/room/create', methods=['POST'])
def create_room():
    """
    處理建立房間的要求。
    接收房間名稱與公開/私人屬性，在 DB 註冊 Room 再跳轉入內。
    """
    pass

@main_bp.route('/room/<int:room_id>')
def room(room_id):
    """
    進行桌遊的虛擬房間。
    檢查權限並調用資料庫確認房間可用性，渲染遊戲對抗用的視窗。
    會將 room_id 傳給前端，以利後續的 WebSocket SocketIO 連線綁定該頻道。
    """
    pass

@main_bp.route('/leaderboard')
def leaderboard():
    """
    列出伺服器整體的積分排行榜(如全服 top 10)，
    並且取得該使用者過往所有的對戰成績作表格顯示。
    """
    pass
