from flask import Flask
from flask_socketio import SocketIO,emit
import flask_cors
app = Flask(__name__)
cors = flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'secret!'
# socketio=SocketIO(app,cors_allowed_origins='*',supports_credentials=True)
socketio = SocketIO(app,cors_allowed_origins='*')

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'},namespace='/test')

@socketio.on('old_person', namespace='/test')
def test_disconnect(massage):
    print(massage)
    print(massage["id"])
    print(massage["name"])
    print(massage["type"])


if __name__ == '__main__':
    socketio.run(app,debug=True,host="0.0.0.0")