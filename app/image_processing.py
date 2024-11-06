import requests
from PIL import Image, ImageOps
from io import BytesIO
import os

class ImageProcessor:
    def __init__(self, save_dir='processed_images'):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def download_image(self, url):
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except requests.exceptions.RequestException as e:
            print(f"이미지 다운로드 실패: {e}")
            return None

    def process_image(self, url, product_id):
        image = self.download_image(url)
        if not image:
            return None
        image = self.flip_image(image)
        output_path = os.path.join(self.save_dir, f"{product_id}.jpg")
        self.optimize_image(image, output_path)
        return output_path

    def flip_image(self, image):
        return ImageOps.mirror(image)

    def optimize_image(self, image, output_path):
        image.save(output_path, format='JPEG', optimize=True, quality=85)