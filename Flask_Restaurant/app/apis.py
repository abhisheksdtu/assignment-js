from app import application
from flask import jsonify, Response, session
from app.models import *
from app import *
import uuid
import datetime
from marshmallow import Schema, fields
from flask_restful import Resource, Api
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
import json

class SignUpRequest(Schema):
    userName = fields.Str(default = "userName")
    password = fields.Str(default = "password")
    name = fields.Str(default = "name")
    level = fields.Int(default = 0)

class LoginRequest(Schema):
    userName = fields.Str(default="userName")
    password = fields.Str(default="password")

class AddVendorRequest(Schema):
    userId = fields.Str(default="userId")

class AddItemRequest(Schema):
    itemName  = fields.Str(default="item name")
    caloriesPerGram = fields.Int(default=100)
    available_quantity = fields.Int(default=100)
    restaurantName = fields.Str(default="abc hotel")
    unitPrice = fields.Int(default=0)

class VendorsListResponse(Schema):
    vendors = fields.List(fields.Dict())

class ItemListResponse(Schema):
    items = fields.List(fields.Dict())

class APIResponse(Schema):
    message = fields.Str(default="Success")

class ItemsOrderList(Schema):
    items = fields.List(fields.Dict())

class PlaceOrderRequest(Schema):
    orderId = fields.Str(default="orderId")

class ListOrderResponse(Schema):
    orders = fields.List(fields.Dict())

# CREATING APIs IN A RESTFUL WAY THROUGH FLASK RESTFUL
class SignUpAPI(MethodResource, Resource):
    @doc(description='Sign Up API', tags=['SignUp API'])
    @use_kwargs(SignUpRequest, location=('json'))
    # MARSHALLING
    @marshal_with(APIResponse)  
    def post(self, **kwargs):
        try:
            user = User(
                uuid.uuid4(), 
                kwargs['name'], 
                kwargs['userName'], 
                kwargs['password'], 
                kwargs['level'])

            db.session.add(user)
            db.session.commit()
            return APIResponse().dump(dict(message='User is successfully registerd')), 200
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to register User : {str(e)}')), 400
            

api.add_resource(SignUpAPI, '/signup')
docs.register(SignUpAPI)

class LoginAPI(MethodResource, Resource):
    @doc(description='Login API', tags=['Login API'])
    @use_kwargs(LoginRequest, location=('json'))
    # MARSHALLING
    @marshal_with(APIResponse)  
    def post(self, **kwargs):
        try:
            user = User.query.filter_by(userName=kwargs['userName'], password = kwargs['password']).first()
            if user:
                print('logged in')
                session['userId'] = user.userId
                print(f'User id : {str(session["userId"])}')
                return APIResponse().dump(dict(message='User is successfully logged in')), 200
                
            else:
                return APIResponse().dump(dict(message='User not found')), 404
                
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to login User : {str(e)}')), 400
            

api.add_resource(LoginAPI, '/login')
docs.register(LoginAPI)

class LogoutAPI(MethodResource, Resource):
    @doc(description='Logout API', tags=['Logout API'])
    # MARSHALLING
    @marshal_with(APIResponse)  
    def post(self, **kwargs):
        try:
            if session['userId']:
                session['userId'] = None
                return APIResponse().dump(dict(message='User is successfully logged out')), 200
                
            else:
                return APIResponse().dump(dict(message='User is not logged in')), 401
                
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to logout User : {str(e)}')), 400
            

api.add_resource(LogoutAPI, '/logout')
docs.register(LogoutAPI)


class AddVendorAPI(MethodResource, Resource):
    @doc(description='Add Vendor API', tags=['Vendor API'])
    @use_kwargs(AddVendorRequest, location=('json'))
    # MARSHALLING
    @marshal_with(APIResponse)  
    def post(self, **kwargs):
        try:
            if session['userId']:
                userId = session['userId']
                user_type = User.query.filter_by(userId=userId).first().level
                print(userId)
                if user_type  == 2:
                    vendor_userId = kwargs['userId']
                    print(vendor_userId)
                    user = User.query.filter_by(userId=vendor_userId).first()
                    print(user.level)
                    user.level = 1
                    # db.session.add(user)
                    db.session.commit()
                    return APIResponse().dump(dict(message='Vendor is successfully added.')), 200
                else:
                    return APIResponse().dump(dict(message='Logged User is not an Admin')), 405
            else:
                return APIResponse().dump(dict(message='User is not logged in')), 401
                
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to add vendor : {str(e)}')), 400
            

api.add_resource(AddVendorAPI, '/add_vendor')
docs.register(AddVendorAPI)


class GetVendorsAPI(MethodResource, Resource):
    @doc(description='Get All Vendors API', tags=['Vendor API'])
    # MARSHALLING
    # @marshal_with(VendorsListResponse)  
    def get(self):
        try:
            if session['userId']:
                userId = session['userId']
                user_type = User.query.filter_by(userId=userId).first().level
                print(userId)
                if user_type  == 2:
                    vendors = User.query.filter_by(level=1)
                    vendors_list = list()
                    for vendor in vendors:
                        vendor_dict = dict()
                        vendor_dict['vendor_id'] = vendor.userId
                        vendor_dict['name'] = vendor.name
                        vendors_list.append(vendor_dict)
                    return VendorsListResponse().dump(dict(vendors = vendors_list)), 200
                else:
                    return APIResponse().dump(dict(message='Logged User is not an Admin')), 405
            else:
                return APIResponse().dump(dict(message='User is not logged in')), 401
                
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list vendors : {str(e)}')), 400
            

api.add_resource(GetVendorsAPI, '/list_vendors')
docs.register(GetVendorsAPI)

class AddItemAPI(MethodResource, Resource):
    @doc(description='Add Item API', tags=['Items API'])
    @use_kwargs(AddItemRequest, location=('json'))
    # MARSHALLING
    @marshal_with(APIResponse)  
    def post(self, **kwargs):
        try:
            if session['userId']:
                userId = session['userId']
                user_type = User.query.filter_by(userId=userId).first().level
                print(userId)
                if user_type  == 1:
                    item = Item(
                        uuid.uuid4(),
                        session['userId'],
                        kwargs['itemName'],
                        kwargs['caloriesPerGram'],
                        kwargs['available_quantity'],
                        kwargs['restaurantName'],
                        kwargs['unitPrice']
                    )
                    db.session.add(item)
                    db.session.commit()
                    return APIResponse().dump(dict(message='Item is successfully added.')), 200
                else:
                    return APIResponse().dump(dict(message='LoggedIn User is not a Vendor')), 405
            else:
                return APIResponse().dump(dict(message='Vendor is not logged in')), 401
                
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list vendors : {str(e)}')), 400
            

api.add_resource(AddItemAPI, '/add_item')
docs.register(AddItemAPI)


class ListItemsAPI(MethodResource, Resource):
    @doc(description='List All Items API', tags=['Items API'])
    # MARSHALLING
    # @marshal_with(ItemListResponse)  
    def get(self):
        try:
            if session['userId']:
                    items = Item.query.all()
                    items_list = list()
                    for item in items:
                        item_dict = dict()
                        item_dict['item_id'] = item.item_id
                        item_dict['itemName'] = item.itemName
                        item_dict['caloriesPerGram'] = item.caloriesPerGram
                        item_dict['available_quantity'] = item.available_quantity
                        item_dict['unitPrice'] = item.unitPrice

                        items_list.append(item_dict)
                        
                    return ItemListResponse().dump(dict(items = items_list)), 200
            else:
                return APIResponse().dump(dict(message='User is not logged in')), 401
                
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list items : {str(e)}')), 400

api.add_resource(ListItemsAPI, '/list_items')
docs.register(ListItemsAPI)


class CreateItemOrderAPI(MethodResource, Resource):
    @doc(description='Create Items Order API', tags=['Order API'])
    @use_kwargs(ItemsOrderList, location=('json'))
    # MARSHALLING
    @marshal_with(APIResponse) 
    def post(self, **kwargs):
        try:
            if session['userId']:
                userId = session['userId']
                user_type = User.query.filter_by(userId=userId).first().level
                print(userId)
                if user_type  == 0:
                    orderId = uuid.uuid4()
                    order = Order(orderId, userId)
                    db.session.add(order)
                    
                    for item in kwargs['items']:
                        item = dict(item)
                        order_item = OrderItems(
                            uuid.uuid4(),
                            orderId,
                            item['item_id'],
                            item['quantity']
                        )
                        db.session.add(order_item)
                    
                    db.session.commit()
                    return APIResponse().dump(dict(message=f'Items for the Order are successfully added with order id : {orderId}')), 200
                else:
                    return APIResponse().dump(dict(message='LoggedIn User is not a Customer')), 405
            else:
                return APIResponse().dump(dict(message='Customer is not logged in')), 401
                
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to add items for ordering : {str(e)}')), 400
            

api.add_resource(CreateItemOrderAPI, '/create_items_order')
docs.register(CreateItemOrderAPI)


class PlaceOrderAPI(MethodResource, Resource):
    @doc(description='Place Order API', tags=['Order API'])
    @use_kwargs(PlaceOrderRequest, location=('json'))
    # MARSHALLING
    @marshal_with(APIResponse)  
    def post(self, **kwargs):
        try:
            if session['userId']:
                userId = session['userId']
                user_type = User.query.filter_by(userId=userId).first().level
                print(userId)

                if user_type  == 0:
                    order_items = OrderItems.query.filter_by(orderId=kwargs['orderId'], isActive=1)
                    order = Order.query.filter_by(orderId=kwargs['orderId'], isActive=1).first()
                    total_amount = 0

                    for order_item in order_items:
                        item_id = order_item.item_id
                        quantity = order_item.quantity

                        item = Item.query.filter_by(item_id=item_id, isActive=1).first()

                        total_amount += quantity * item.unitPrice

                        item.available_quantity = item.available_quantity - quantity
                    
                    order.total_amount = total_amount
                    db.session.commit()
                    return APIResponse().dump(dict(message='Order is successfully placed.')), 200
                else:
                    return APIResponse().dump(dict(message='LoggedIn User is not a Customer')), 405
            else:
                return APIResponse().dump(dict(message='Customer is not logged in')), 401
                
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to place order : {str(e)}')), 400
            

api.add_resource(PlaceOrderAPI, '/place_order')
docs.register(PlaceOrderAPI)

class ListOrdersByCustomerAPI(MethodResource, Resource):
    @doc(description='List Orders by Customer API', tags=['Order API'])
    # MARSHALLING
    # @marshal_with(ListOrderResponse)  
    def get(self, **kwargs):
        try:
            if session['userId']:
                userId = session['userId']
                user_type = User.query.filter_by(userId=userId).first().level
                print(userId)

                if user_type  == 0:
                    orders = Order.query.filter_by(userId=userId, isActive=1)
                    order_list = list()
                    for order in orders:
                        order_items = OrderItems.query.filter_by(orderId=order.orderId, isActive=1)
                        
                        order_dict = dict()
                        order_dict['orderId'] = order.orderId
                        order_dict['items'] = list()
                        
                        for order_item in order_items:
                            order_item_dict = dict()
                            order_item_dict['item_id'] = order_item.item_id
                            order_item_dict['quantity'] = order_item.quantity
                            order_dict['items'].append(order_item_dict)
                        
                        order_list.append(order_dict)
                        
                    return ListOrderResponse().dump(dict(orders=order_list)), 200
                else:
                    return APIResponse().dump(dict(message='LoggedIn User is not a Customer')), 405
            else:
                return APIResponse().dump(dict(message='Customer is not logged in')), 401
                
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list orders : {str(e)}')), 400
            

api.add_resource(ListOrdersByCustomerAPI, '/list_orders')
docs.register(ListOrdersByCustomerAPI)


class ListAllOrdersAPI(MethodResource, Resource):
    @doc(description='List All Orders API', tags=['Order API'])
    # MARSHALLING
    # @marshal_with(ListOrderResponse)  
    def get(self, **kwargs):
        try:
            if session['userId']:
                userId = session['userId']
                user_type = User.query.filter_by(userId=userId).first().level
                print(userId)

                if user_type  == 2:
                    orders = Order.query.filter_by(isActive=1)
                    order_list = list()
                    for order in orders:
                        order_items = OrderItems.query.filter_by(orderId=order.orderId, isActive=1)
                        
                        order_dict = dict()
                        order_dict['orderId'] = order.orderId
                        order_dict['items'] = list()
                        
                        for order_item in order_items:
                            order_item_dict = dict()
                            order_item_dict['item_id'] = order_item.item_id
                            order_item_dict['quantity'] = order_item.quantity
                            order_dict['items'].append(order_item_dict)

                        order_list.append(order_dict)
                        
                    return ListOrderResponse().dump(dict(orders=order_list)), 200
                else:
                    return APIResponse().dump(dict(message='LoggedIn User is not an Admin')), 405
            else:
                return APIResponse().dump(dict(message='Admin is not logged in')), 401
                
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list all orders : {str(e)}')), 400
            

api.add_resource(ListAllOrdersAPI, '/list_all_orders')
docs.register(ListAllOrdersAPI)