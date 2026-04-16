from flask import render_template, request, redirect, url_for, flash, session
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊請求。
    - GET: 渲染並顯示註冊表單
    - POST: 接收與驗證使用者名與密碼，建立系統帳號，然後重導至登入
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入驗證。
    - GET: 顯示登入表單
    - POST: 根據輸入資料驗證密碼，設定使用者的登入 Session
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    清除 session 中現有的登入權杖，並把使用者退回未登入首頁。
    """
    pass
