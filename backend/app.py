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

if __name__=='__main__':
    app.run(port=5555, debug=True)