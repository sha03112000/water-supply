from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage

# delete old images when product is deleted
from django.db.models.signals import post_delete
from django.dispatch import receiver



User = get_user_model()
# Create your models here.
class Products(models.Model):
    product_name = models.CharField(max_length=100)
    product_rate = models.DecimalField(max_digits=10, decimal_places=2)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    product_image = models.ImageField(upload_to='product_images/' , blank=True, null=True) # folder will be created in MEDIA_ROOT automatically
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products_created', null=True, blank=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products_updated', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name
    class Meta:
        db_table = 'products'
        
    # delete old images when product is updated
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_image = Products.objects.get(pk=self.pk).product_image
                if old_image and old_image != self.product_image:
                    if default_storage.exists(old_image.name):
                        default_storage.delete(old_image.name)
            except Products.DoesNotExist:
                pass
        super().save(*args, **kwargs)

# delete old images when product is deleted
@receiver(post_delete, sender=Products)
def delete_product_image(sender, instance, **kwargs):
    if instance.product_image:
        if default_storage.exists(instance.product_image.name):
            default_storage.delete(instance.product_image.name)
            

class Orders(models.Model):
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    delivery_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    payment_method = models.IntegerField(choices=[
        (1, 'Cash'),
        (2, 'Card'),
        (3, 'Online')
    ], default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.ordered_by.username}"

    class Meta:
        db_table = 'orders'