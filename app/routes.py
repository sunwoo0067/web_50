from flask import Blueprint, render_template, jsonify
from app.models import Product

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    products = Product.query.all()
    return render_template('dashboard.html', products=products)

@main.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])