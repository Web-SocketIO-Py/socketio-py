from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Khuc nay cau hinh theo ducument
app = Flask(__name__, static_folder='./templates', template_folder='./templates')

app.config[ 'SECRET_KEY' ] = 'chonayrandomstring:lalalalalalalalala';
socketio = SocketIO(app);

# Cac route chinh
@app.route('/login')
def index_login():
  return render_template( '/login/index.html' )

@app.route('/info')
def index_info():
  return render_template( '/members/index.html' )

@app.route('/404')
def index_404():
  return render_template( '/404/index.html' )

# Khi co user connect toi Server
@socketio.on('conn')
def handle_login(json):
    print('Received: ' + str(json))

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

# Start server
if __name__ == '__main__':
    socketio.run(app)