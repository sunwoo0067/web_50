import requests
import xml.etree.ElementTree as ET
from app.models import db, Product, Category
from app.tasks import process_product_image
from datetime import datetime

class ZentradeAPICollector:
    def __init__(self, api_url, api_params):
        self.api_url = api_url
        self.api_params = api_params

    def fetch_products(self):
        try:
            response = requests.get(self.api_url, params=self.api_params)
            response.raise_for_status()
            data = response.content
            self.parse_and_store_data(data)
        except requests.exceptions.RequestException as e:
            print(f"API 요청 실패: {e}")

    def parse_and_store_data(self, xml_data):
        root = ET.fromstring(xml_data)
        for product in root.findall('product'):
            name = product.find('name').text
            price = product.find('price').text
            category_name = product.find('category').text
            image_url = product.find('image_url').text

            category = self.get_or_create_category(category_name)
            new_product = Product(
                name=name,
                price=float(price),
                category_id=category.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_product)
            db.session.flush()

            process_product_image.delay(new_product.id, image_url)

        db.session.commit()

    def get_or_create_category(self, category_name):
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
            db.session.add(category)
            db.session.commit()
        return category 