import os
import sys
import socket
import threading
import time
import OpenSSL       # 确保 PyInstaller 能检测到 adhoc SSL 的依赖
import cryptography

from flask import Flask, send_from_directory, jsonify
from flask_socketio import SocketIO, emit

from platforms import get_platform

# 兼容 PyInstaller 的资源路径定位机制
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# 常量
VERSION = "v0.0.3"

# 平台检测
platform = get_platform()

# WebView2 环境变量（仅 Windows 需要）
for k, v in platform.get_webview_env().items():
    os.environ[k] = v

# ==========================================
# 1. Flask & SocketIO 初始化
# ==========================================
WEBUI_DIR = os.path.join(base_path, 'webui')
app = Flask(__name__, static_folder=WEBUI_DIR, static_url_path='')
app.config['SECRET_KEY'] = 'webmic-super-secret-key'

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')


def get_lan_ip():
    """获取本机在局域网内的 IPv4 地址"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# ==========================================
# 2. 路由配置
# ==========================================
@app.route('/')
def index():
    return send_from_directory(WEBUI_DIR, 'index.html')


@app.route('/desktop')
def desktop():
    return send_from_directory(WEBUI_DIR, 'desktop.html')


@app.route('/api/info')
def api_info():
    return jsonify({
        "ip": get_lan_ip(),
        "port": 5000,
        "version": VERSION
    })


@app.route('/api/platform_info')
def api_platform_info():
    return jsonify({
        "os": sys.platform,
        "driver_display_name": platform.driver_display_name,
        "driver_match_keyword": platform.driver_match_keyword,
        "post_install_warning": platform.get_post_install_warning(),
    })


@app.route('/api/check_driver', methods=['GET'])
def api_check_driver():
    return jsonify({"installed": platform.is_driver_installed()})


@app.route('/api/install_driver', methods=['POST'])
def api_install_driver():
    success, msg = platform.install_driver()
    return jsonify({"success": success, "msg": msg})


@app.route('/api/uninstall_driver', methods=['POST'])
def api_uninstall_driver():
    success, msg = platform.uninstall_driver()
    return jsonify({"success": success, "msg": msg})


@app.route('/api/exit', methods=['POST'])
def api_exit():
    def kill_me():
        time.sleep(1)
        os._exit(0)
    threading.Thread(target=kill_me).start()
    return jsonify({"success": True})


# ==========================================
# 3. WebRTC 信令服务器 (Socket.IO)
# ==========================================
@socketio.on('join')
def on_join(data):
    role = data.get('role', 'unknown')
    print(f"[{role}] 已连接到信令服务器")
    emit('ready', {'role': role}, broadcast=True, include_self=False)


@socketio.on('offer')
def on_offer(data):
    emit('offer', data, broadcast=True, include_self=False)


@socketio.on('answer')
def on_answer(data):
    emit('answer', data, broadcast=True, include_self=False)


@socketio.on('ice_candidate')
def on_ice_candidate(data):
    emit('ice_candidate', data, broadcast=True, include_self=False)


# ==========================================
# 4. 启动入口
# ==========================================
def start_flask():
    lan_ip = get_lan_ip()
    print(f"\n=========================================")
    print(f"ZeroMic 服务端已启动！")
    print(f"手机请访问: https://{lan_ip}:5000")
    print(f"=========================================\n")

    socketio.run(app, host='0.0.0.0', port=5000, ssl_context='adhoc', debug=False, use_reloader=False, allow_unsafe_werkzeug=True)


if __name__ == '__main__':
    # 启动 Flask 线程
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # 给 Flask 一点时间启动
    time.sleep(1.5)

    desktop_url = 'https://127.0.0.1:5000/desktop'

    if platform.use_system_browser:
        import webbrowser
        print(f"[ZeroMic] 桌面页面已用系统浏览器打开: {desktop_url}")
        webbrowser.open(desktop_url)
        # 主线程保持存活
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        import webview
        icon_ext = 'ico' if sys.platform == 'win32' else 'png'
        icon_path = os.path.join(os.path.dirname(__file__), f'icon.{icon_ext}')
        if not os.path.exists(icon_path):
            icon_path = ''

        webview.create_window(
            title='ZeroMic Desktop',
            url=desktop_url,
            width=380,
            height=740,
            resizable=False,
            frameless=False,
            easy_drag=False,
            background_color='#121212'
        )
        webview.start(
            gui=platform.gui_backend,
            debug=False,
            icon=icon_path
        )
