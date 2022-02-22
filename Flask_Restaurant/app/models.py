from app import application
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:manager@localhost/restaurant'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)

class User(db.Model):
        __tablename__ = 'user'

        userId = db.Column(db.String(100), primary_key = True)
        name = db.Column(db.String(200), unique=True)
        userName = db.Column(db.String(200), unique=True)
        password = db.Column(db.String(200))
        level = db.Column(db.Integer, default=0)
        isActive = db.Column(db.Integer, default = 1)
        createdTs = db.Column(db.DateTime, default = datetime.utcnow)
        updatedTs = db.Column(db.DateTime)

        def __init__(self, userId, name, userName, password, level):
            self.userId = userId
            self.name = name
            self.userName = userName
            self.password = password
            self.level = level
            self.isActive = 1
            self.createdTs = datetime.utcnow()

class Item(db.Model):
        __tablename__ = 'item'
    
        item_id = db.Column(db.String(100), primary_key = True)
        vendor_id = db.Column(db.String(100), db.ForeignKey("user.userId"))
        item_name = db.Column(db.String(500))
        calories_per_gm = db.Column(db.Integer)
        available_quantity = db.Column(db.Integer)
        restaurant_name = db.Column(db.String(500))
        unit_price = db.Column(db.Integer)
        isActive = db.Column(db.Integer, default = 1)
        createdTs = db.Column(db.DateTime, default = datetime.utcnow)
        updatedTs = db.Column(db.DateTime)

        def __init__(self, item_id, vendor_id, item_name, calories_per_gm, available_quantity, restaurant_name, unit_price):
            self.item_id = item_id
            self.vendor_id = vendor_id
            self.item_name = item_name
            self.calories_per_gm = calories_per_gm
            self.available_quantity = available_quantity
            self.restaurant_name=restaurant_name
            self.unit_price = unit_price
            self.isActive = 1
            self.createdTs = datetime.utcnow()

class Order(db.Model):
        __tablename__ = 'order'
        
        order_id = db.Column(db.String(100), primary_key = True)
        userId = db.Column(db.String(100), db.ForeignKey("user.userId"))
        total_amount = db.Column(db.Integer, default=0)
        is_placed = db.Column(db.Integer, default=0)
        isActive = db.Column(db.Integer, default = 1)
        createdTs = db.Column(db.DateTime, default = datetime.utcnow)
        updatedTs = db.Column(db.DateTime)

        def __init__(self, order_id, userId):
            self.order_id = order_id
            self.userId = userId
            self.total_amount = 0
            self.isActive = 1
            self.createdTs = datetime.utcnow()

class OrderItems(db.Model):
        __tablename__ = 'order_items'
        
        id = db.Column(db.String(100), primary_key = True)
        order_id = db.Column(db.String(100), db.ForeignKey("order.order_id"))
        item_id = db.Column(db.String(100), db.ForeignKey("item.item_id"))
        quantity = db.Column(db.Integer)
        isActive = db.Column(db.Integer, default = 1)
        createdTs = db.Column(db.DateTime, default = datetime.utcnow)
        updatedTs = db.Column(db.DateTime)

        def __init__(self, id, order_id, item_id, quantity):
            self.id = id
            self.order_id = order_id
            self.item_id = item_id
            self.quantity = quantity
            self.isActive = 1
            self.createdTs = datetime.utcnow()

db.create_all()
db.session.commit()