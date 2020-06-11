# Cài 22 module cần thiết: Flask và flask-socketio
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Khuc nay cau hinh theo ducument
# Static folder là để browser truy cập trực tiếp vào
# Tempplates folder chứa các page: login, info, 404
app = Flask(__name__, static_folder='./templates', template_folder='./templates')

app.config[ 'SECRET_KEY' ] = 'chonayrandomstring:lalalalalalalalala';
socketio = SocketIO(app, cors_allowed_origins="*"); # cors_allowed_origins="*" là do latest version của flask-socketio yêu cầu

# Cac route chính
@app.route('/login')
def index_login():
  return render_template('/login/index.html')

@app.route('/info')
def index_info():
  return render_template('/members/index.html')

@app.errorhandler(404)
def page_not_found(e):
  socketio.emit('error', '404')
  return render_template('/404/index.html'), 404

# Khi co user connect toi Server
@socketio.on('conn')
def handle_login(json):
  print('Client: ' + str(json))

# Khi user send form login
@socketio.on('login')
def handle_login(data):
  user_name = data['data']['user_name']
  password = data['data']['password']

  # Neu dung email va password
  if user_name == "admin" and password == "admin":
    socketio.emit('redirect', 'info')
  else:
    socketio.emit('redirect', 'login')

# Start server: python server.py
if __name__ == '__main__':
    socketio.run(app)