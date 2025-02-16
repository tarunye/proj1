from PIL import Image
import io
from typing import Union
import base64
from app.services.llm_service import llm_service
from app.config import settings

class ImageService:
    def __init__(self):
        self.data_dir = settings.DATA_DIR

    async def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from an image using LLM vision capabilities."""
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
        prompt = f"""
        Analyze this image and extract any text or numbers you see.
        If you see a credit card number, only return that number without spaces.
        """
        
        result = await llm_service.get_completion(prompt)
        return result.strip()

    def compress_image(self, input_path: str, output_path: str, quality: int = 85) -> None:
        """Compress an image while maintaining reasonable quality."""
        with Image.open(input_path) as img:
            img.save(output_path, quality=quality, optimize=True)

    def resize_image(self, input_path: str, output_path: str, max_size: tuple) -> None:
        """Resize an image while maintaining aspect ratio."""
        with Image.open(input_path) as img:
            img.thumbnail(max_size)
            img.save(output_path)

image_service = ImageService()