from flask import render_template
from . import main_bp

@main_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁大廳。
    
    渲染 main/index.html，包含輸入暱稱、建立房間、加入房間與快速配對的表單。
    """
    pass
