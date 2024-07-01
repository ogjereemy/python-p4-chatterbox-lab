from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages = [message.to_dict() for message in Message.query.all()]

    response = make_response(messages, 200)

    return response

@app.route('/messages', methods=['POST'])
def create_message():
    body = request.json.get('body')
    username = request.json.get('username')

    if not body or not username:
        return make_response({'error': 'Missing body or username'}, 400)

    message = Message(body=body, username=username)
    db.session.add(message)
    db.session.commit()

    return make_response(message.to_dict(), 201)
    

@app.route('/messages/<int:id>', methods=['PATCH'])
def messages_by_id(id):
    message = db.session.get(Message, id)

    if not message:
        return make_response({'error': 'Message not found'}, 404)

    body = request.json.get('body')
    username = request.json.get('username')

    if body:
        message.body = body

    if username:
        message.username = username

    db.session.commit()

    return make_response(message.to_dict(), 200)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)

    if not message:
        return make_response({'error': 'Message not found'}, 404)

    db.session.delete(message)
    db.session.commit()

    return make_response('', 204)
    

if __name__ == '__main__':
    app.run(port=5555)
