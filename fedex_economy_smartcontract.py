from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send
import ast

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")


users = []
orders = {}

# initialize the fedex user
fedex = {'id': "fedex", 'tokens': 1000000, 'profile': ''}
users.append(fedex)


# TODO: remove this
@socketio.on('message')
def handle_message(msg):
    print('Message ' + msg)
    send(msg, broadcast=True)


@app.route('/')
def home():
    return "Fedex economy smart contract is running"


@app.route('/register_user')
def register_user():
    # TODO: reject addition if user already exists
    user_id = request.args['user_id']
    user = {'id': user_id, 'tokens': 0, 'profile': ''}
    users.append(user)

    return user_id + ' is registered'


@app.route('/update_profile')
def update_profile():
    print('entered the update profile')
    user_id = request.args['user_id']
    profile_string = request.args['profile']

    profile_dict = ast.literal_eval(profile_string)

    status_message = "profile not found"
    for user in users:
        if user['id'] == user_id:
            user['profile'] = profile_dict
            print('updating profile')
            socketio.send(str(user), namespace='/profile', broadcast=True)
            status_message = "profile updated"

    return status_message


@app.route('/user_profile')
def user_profile():
    user_id = request.args['user_id']

    profile = ""
    for user in users:
        if user['id'] == user_id:
            profile = user['profile']

    return profile


@app.route('/list_users')
def list_users():
    return str(users)


@app.route('/user_balance')
def user_balance():
    user_id = request.args['user_id']

    balance = 0
    for user in users:
        if user['id'] == user_id:
            balance = user['tokens']

    return str(balance)


@app.route('/update_order')
def update_order():
    order = ast.literal_eval(request.args['order'])
    orders[order['order_id']] = order

    socketio.send(str(order), namespace='/order', broadcast=True)

    return "order updated"


@app.route('/list_orders')
def list_orders():
    order_list = []
    for order_id in orders:
        order_list.append(orders[order_id])
    return str(order_list)


@app.route('/list_orders_by_supplier')
def list_orders_by_supplier():
    supplier = request.args['supplier']
    order_list = []
    for order_id in orders:
        if orders[order_id]['supplier'] == supplier:
            order_list.append(orders[order_id])
    return str(order_list)


@app.route('/list_orders_by_customer')
def list_orders_by_customer():
    customer = request.args['customer']
    order_list = []
    for order_id in orders:
        if orders[order_id]['customer'] == customer:
            order_list.append(orders[order_id])
    return str(order_list)


@app.route('/pay')
def pay():
    sender = request.args['sender']
    receiver = request.args['receiver']
    amt = int(request.args['amount'])

    for user in users:
        if user['id'] == sender:
            user['tokens'] -= amt
        if user['id'] == receiver:
            user['tokens'] += amt

    return "paid"


if __name__ == '__main__':
    socketio.run(app, debug=False)


