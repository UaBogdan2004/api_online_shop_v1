import os
from datetime import datetime
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    descriptions = models.TextField()

    def __str__(self):
        return self.name

def product_image_path(instance, filename):
    """Формує шлях для збереження зображень за датою"""
    today = datetime.today().strftime('%Y/%m/%d')  # Створює шлях "YYYY/MM/DD"
    return os.path.join('products', today, filename)  # Наприклад: "products/2025/03/13/image.jpg"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to=product_image_path)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
