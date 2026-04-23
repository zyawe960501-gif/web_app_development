from flask import request, redirect, url_for, render_template, session, flash
from . import room_bp

@room_bp.route('/create', methods=['POST'])
def create_room():
    """
    接收玩家暱稱，建立 User 與 Room。
    成功後將 user_id 存入 session，重導向至 /room/<room_code>。
    """
    pass

@room_bp.route('/join', methods=['POST'])
def join_room():
    """
    接收玩家暱稱與指定房號，檢查房間狀態。
    若合法則建立 User，將其設為 guest_id，並重導向至 /room/<room_code>。
    """
    pass

@room_bp.route('/quick_match', methods=['POST'])
def quick_match():
    """
    尋找 status 為 'waiting' 的空房間。
    若找到則加入；若無則自動建立新房間。
    """
    pass

@room_bp.route('/<room_code>', methods=['GET'])
def game_room(room_code):
    """
    顯示遊戲房間對戰畫面。
    驗證 session 中的 user_id 是否擁有進入該房間的權限。
    若通過驗證，渲染 room/game.html。
    """
    pass
