from flask import Blueprint, request, render_template
import requests

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    products = Product.query.all()
    return render_template('dashboard.html', products=products)

@main.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@main.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        api_url = "https://www.zentrade.co.kr/shop/proc/product.api.php"
        api_params = {
            'id': 'b00679540',
            'm_skey': '5284c44b0fcf078e7691c5884d6ea9',
            'search': query
        }
        response = requests.get(api_url, params=api_params)
        if response.status_code == 200:
            products = response.json()  # 응답이 JSON 형식이라고 가정
            return render_template('search_results.html', products=products)
        else:
            return "API 요청 실패", 500
    return render_template('search.html')