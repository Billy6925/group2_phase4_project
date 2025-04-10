from flask import Flask,make_response,jsonify,request
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api,Resource

from models import db,Product,Cart,User

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.json.compact=False

migrate=Migrate(app,db)
db.init_app(app)
api=Api(app)
CORS(app)

class Products(Resource):
    def get(self):
        products= [product.to_dict() for product in Product.query.all()]
        response= make_response(jsonify(products),200)
        return response
    
    def post(self):
        data= request.get_json()
        if not data:
            return {'error':'Unable to derive data'}
        new_product= Product(
            name= data.get('name'),
            price= data.get('price'),
            description= data.get('description'),
            image= data.get('image'),
            category= data.get('category'),
            quantity= data.get('quantity')
        )
        db.session.add(new_product)
        db.session.commit()

        response= make_response(jsonify({
            "id":new_product.id,
            "name":new_product.name,
            "price":new_product.price,
            "description":new_product.description,
            "category":new_product.category,
            "quantity":new_product.quantity
        }),201
        )
        return response

api.add_resource(Products,'/products')

class ProductByID(Resource):
    def get(self,id):
        product= Product.query.filter(Product.id==id).first()
        if not product:
            return {'error':'Product not found'},404
        response= make_response(jsonify(product.to_dict()),200)
        return response
    def patch(self,id):
        data= request.get_json()
        if not data:
            return {'error':'No data provided'},400
        product= Product.query.filter(Product.id==id).first()
        if not product:
            return {'error':'Product not found'},404
        for key,value in data.items():
            if hasattr(product,key):
                setattr(product,key,value)
        db.session.commit()
        response= make_response(jsonify(product.to_dict()),200)
        return response
    
    def delete(self,id):
        product= Product.query.filter(Product.id==id).first()
        if not product:
            return {'error':'Product not found'},404
        db.session.delete(product)
        db.session.commit()

        return make_response({'message':'Product deleted successfully'},200)

api.add_resource(ProductByID,'/products/<int:id>')

class Carts(Resource):
    def get(self):
        carts= [cart.to_dict() for cart in Cart.query.all()]
        response= make_response(jsonify(carts),200)
        return response
    
    def post(self):
        data= request.get_json()
        if not data:
            return make_response({'error':'No data provided'},400)
        new_cart= Cart(
            user_id=data.get('user_id'),
            product_id=data.get('product_id'),
            quantity=data.get('quantity'),
            created_at= data.get('created_at'),
            updated_at= data.get('updated_at')
        )
        db.session.add(new_cart)
        db.session.commit()

        response= make_response(jsonify(new_cart({
            'id':new_cart.id,
            'user_id':new_cart.user_id,
            'product_id':new_cart.product_id,
            'quantity':new_cart.quantity,
            'created_at':new_cart.created_at,
            'updated_at':new_cart.updated_at
        })),201)
        return response
    
api.add_resource(Carts,'/carts')

class CartByID(Resource):
    def get(self,id):
        cart = Cart.query.filter_by(id=id).first()
        if not cart:
            return {'error':'Cart not found'},404
        return make_response(jsonify(cart.to_dict()),200)
    
    def patch(self,id):
        cart = Cart.query.filter_by(id=id).first()
        if not cart:
            return {'error':'Cart not found'},404
        data= request.get_json()
        if not data:
            return {'error':'No data provided'},400
        for key,value in data.items():
            if hasattr(cart,key):
                setattr(cart,key,value)
        db.session.commit()

        response= make_response(jsonify(cart.to_dict()),200)
        return response
    
    def delete(self,id):
        cart= Cart.query.filter_by(id=id).first()
        if not cart:
            return {'error':'Cart not found'},404
        db.session.delete(cart)
        db.session.commit()

        return {'message':'Cart deleted successfully'}
    
api.add_resource(CartByID,'/carts/<int:id>')

class Users(Resource):
    def get(self):
        users= [user.to_dict() for user in User.query.all()]
        response= make_response(jsonify(users),200)
        return response
    
    def post(self):
        data= request.get_json()
        if not data:
            return {'error':'No data provided'},400
        new_user= User(username= data.get('username'))
        db.session.add(new_user)
        db.session.commit()

        response= make_response(jsonify({
            'id': new_user.id,
            'username': new_user.username
        }),201)
        return response
api.add_resource(Users,'/users')
        
if __name__=='__main__':
    app.run(port=5555, debug=True)