from django.contrib import admin
from .models import *

admin.site.register(Size)

class BanneerAdmin(admin.ModelAdmin):
    list_display = ('alt_text','image_tag')
admin.site.register(Banneer, BanneerAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag')
admin.site.register(Brand, BrandAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag')
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'category','brand','size','status', 'is_featured')
    list_editable = ('status', 'is_featured')
admin.site.register(Product,ProductAdmin)

#Атрибуты товаров
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'product','price','size')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

# #Заказы
# class CartOrderAdmin(admin.ModelAdmin):
#     list_display = ('user','total_amt', 'paid_status', 'order_dt')
# admin.site.register(CartOrder, CartOrderAdmin)
#
# #Детали заказа
# class CartOrderItemsAdmin(admin.ModelAdmin):
#     list_display = ('invoice_no','item', 'image', 'qty', 'price', 'total')
# admin.site.register(CartOrderItems, CartOrderItemsAdmin)

#Отзыв товара
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)