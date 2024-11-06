from app import celery
from app.image_processing import ImageProcessor

@celery.task
def process_product_image(product_id, image_url):
    processor = ImageProcessor()
    processed_path = processor.process_image(image_url, product_id)
    if processed_path:
        print(f"이미지 처리 완료: {processed_path}")

@celery.task
def collect_zentrade_data():
    from app.api_collection import ZentradeAPICollector
    api_url = "https://www.zentrade.co.kr/shop/proc/product.api.php"
    api_params = {
        'id': 'b00679540',
        'm_skey': '5284c44b0fcf078e7691c5884d6ea9',
    }
    collector = ZentradeAPICollector(api_url, api_params)
    collector.fetch_products()