import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from utils import load_data


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text(50))
    last_name = db.Column(db.Text(50))
    age = db.Column(db.Integer)
    email = db.Column(db.Text(100))
    role = db.Column(db.Text(25))
    phone = db.Column(db.Text(25))

    def get_user(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
        }


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    description = db.Column(db.Text(100))
    start_date = db.Column(db.Text(50))
    end_date = db.Column(db.Text(50))
    address = db.Column(db.Text(150))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def get_order(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'address': self.address,
            'price': self.price,
            'customer_id': self.customer_id,
            'executor_id': self.executor_id,
        }




class Offers(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def get_offer(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'executor_id': self.executor_id,
        }


def insert_users():
    users = load_data('data/users.json')

    for user in users:
        new_user = Users(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone'],
        )
        db.session.add(new_user)
        db.session.commit()


def insert_orders():
    orders = load_data('data/orders.json')

    for order in orders:
        new_order = Orders(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=order['start_date'],
            end_date=order['end_date'],
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id'],
        )
        db.session.add(new_order)
        db.session.commit()


def insert_offers():
    offers = load_data('data/offers.json')

    for offer in offers:
        new_offer = Offers(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id'],
        )
        db.session.add(new_offer)
        db.session.commit()


def create_database():
    db.drop_all()
    db.create_all()
    insert_users()
    insert_orders()
    insert_offers()


@app.route('/users', methods=['GET', 'POST'])
def users_view():
    match request.method:
        case 'GET':
            users = []

            for user in Users.query.all():
                users.append(user.get_user())
            return jsonify(users)

        case 'POST':
            user_data = json.loads(request.data)
            new_user = Users(
                id=user_data['id'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                age=user_data['age'],
                email=user_data['email'],
                role=user_data['role'],
                phone=user_data['phone'],
            )
            db.session.add(new_user)
            db.session.commit()
            return 'User created'


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user_view(id):
    user = Users.query.get(id)

    match request.method:
        case 'GET':
            return jsonify(user.get_user())

        case 'PUT':
            user_data = json.loads(request.data)
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.age = user_data['age']
            user.email = user_data['email']
            user.role = user_data['role']
            user.phone = user_data['phone']
            db.session.add(user)
            db.session.commit()
            return 'User updated'

        case 'DELETE':
            db.session.delete(user)
            db.session.commit()
            return 'User deleted'


@app.route('/orders', methods=['GET', 'POST'])
def orders_view():
    match request.method:
        case 'GET':
            orders = []

            for order in Orders.query.all():
                orders.append(order.get_order())
            return jsonify(orders)

        case 'POST':
            order_data = json.loads(request.data)
            new_order = Orders(
                id=order_data['id'],
                name=order_data['name'],
                description=order_data['description'],
                start_date=order_data['start_date'],
                end_date=order_data['end_date'],
                address=order_data['address'],
                price=order_data['price'],
                customer_id=order_data['customer_id'],
                executor_id=order_data['executor_id'],
            )
            db.session.add(new_order)
            db.session.commit()
            return 'Order created'


@app.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def order_view(id):
    order = Orders.query.get(id)

    match request.method:
        case 'GET':
            return jsonify(order.get_order())

        case 'PUT':
            order_data = json.loads(request.data)
            order.name = order_data['name']
            order.description = order_data['description']
            order.start_date = order_data['start_date']
            order.end_date = order_data['end_date']
            order.address = order_data['address']
            order.price = order_data['price']
            order.customer_id = order_data['customer_id']
            order.executor_id = order_data['executor_id']
            db.session.add(order)
            db.session.commit()
            return 'Order updated'

        case 'DELETE':
            db.session.delete(order)
            db.session.commit()
            return 'Order deleted'


@app.route('/offers', methods=['GET', 'POST'])
def offers_view():
    match request.method:
        case 'GET':
            offers = []

            for offer in Offers.query.all():
                offers.append(offer.get_offer())
            return jsonify(offers)

        case 'POST':
            offer_data = json.loads(request.data)
            new_offer = Offers(
                id=offer_data['id'],
                order_id=offer_data['order_id'],
                executor_id=offer_data['executor_id'],
            )
            db.session.add(new_offer)
            db.session.commit()
            return 'Offer created'


@app.route('/offers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def offer_view(id):
    offer = Offers.query.get(id)

    match request.method:
        case 'GET':
            return jsonify(offer.get_offer())

        case 'PUT':
            offer_data = json.loads(request.data)
            offer.order_id = offer_data['order_id']
            offer.executor_id = offer_data['executor_id']
            db.session.add(offer)
            db.session.commit()
            return 'Offer updated'

        case 'DELETE':
            db.session.delete(offer)
            db.session.commit()
            return 'Offer deleted'


if __name__ == '__main__':
    create_database()
    app.run(debug=True)

