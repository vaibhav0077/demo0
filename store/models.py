from django.db import models
import datetime

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    @staticmethod
    def all_category():
        return Category.objects.all()
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200, default=1)
    image = models.ImageField(upload_to = 'products/')
    Category =  models.ForeignKey(Category, on_delete=models.CASCADE, default=1)



    @staticmethod
    def get_product_by_ids(ids):
        return Product.objects.filter(id__in = ids)

    @staticmethod
    def all_product():
        return Product.objects.all()
        
    @staticmethod
    def all_product_category_by_id(category_id):
        return Product.objects.filter(Category = category_id)
        
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return  False


class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
