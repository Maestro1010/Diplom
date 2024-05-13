from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

#Баннеры
class Banneer(models.Model):
    image=models.ImageField(upload_to='banner_img/')
    alt_text=models.CharField(max_length=300)

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.image.url))

    def __str__(self):
        return self.alt_text

    class Meta:
        verbose_name = '1. Баннеры'
        verbose_name_plural = '1. Баннеры'

class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='cat_img/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    class Meta:
        verbose_name = '2. Категории'
        verbose_name_plural = '2. Категории'

class Brand(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='brand_img/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="60" height="60" />' % (self.image.url))

    class Meta:
        verbose_name = '3. Мерч'
        verbose_name_plural = '3. Мерч'



#Размер товара
class Size(models.Model):
    title=models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '4. Размеры'
        verbose_name_plural = '4. Размеры'

#Товары
class Product(models.Model):
    title=models.CharField(max_length=200)
    slug = models.CharField(max_length=400)
    detail = models.TextField()
    specs = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '5. Товары'
        verbose_name_plural = '5. Товары'

#Атрибуты товаров
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='prod_imgs/', null=True)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = '6. Атрибуты товаров'
        verbose_name_plural = '6. Атрибуты товаров'

    def image_tag(self):
        return mark_safe('<img src="%s" width="60" height="60" />' % (self.image.url))

# # Заказы
# class CartOrder(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     total_amt = models.FloatField()
#     paid_status=models.BooleanField(default=False)
#     order_dt=models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user
#
#     class Meta:
#         verbose_name = '7. Заказы'
#         verbose_name_plural = '7. Заказы'
#
#
# #Детали заказа
# class CartOrderItems(models.Model):
#     order=models.ForeignKey(CartOrder, on_delete=models.CASCADE)
#     invoice_no=models.CharField(max_length=150)
#     item = models.CharField(max_length=150)
#     image = models.CharField(max_length=200)
#     qty = models.IntegerField()
#     price = models.FloatField()
#     total = models.FloatField()
#
#     def __str__(self):
#         return self.order
#
#     class Meta:
#         verbose_name = '8. Детали заказа'
#         verbose_name_plural = '8. Детали заказа'

# Отзыв товара
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    def get_review_rating(self):
        return self.review_rating

    class Meta:
        verbose_name = '#. Оценки товаров'
        verbose_name_plural = '#. Оценки товаров'