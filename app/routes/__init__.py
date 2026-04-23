from flask import Blueprint

# 使用 Blueprint 模組化路由
main_bp = Blueprint('main', __name__)
room_bp = Blueprint('room', __name__, url_prefix='/room')

# 匯入各個路由模組以註冊
from . import main, room

def init_app(app):
    """
    註冊所有的 Blueprint 到 Flask app
    """
    app.register_blueprint(main_bp)
    app.register_blueprint(room_bp)
