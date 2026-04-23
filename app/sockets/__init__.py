from .game_events import init_sockets

def init_app(socketio):
    """
    初始化所有 socket 模組
    """
    init_sockets(socketio)
