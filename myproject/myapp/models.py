from django.db import models
from django.utils import timezone



class customer(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=255)
    phone=models.CharField(max_length=10)
    password=models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def emailexists(currentemail):
        try:
            email=customer.objects.get(email=currentemail)
            return email
        except:
            return None

class category(models.Model):
    category_name=models.CharField(max_length=55)

    def __str__(self):
        return self.category_name
    
    @staticmethod
    def showcategory():
        return category.objects.all()

class products(models.Model):
    image=models.ImageField()
    product_name=models.CharField(max_length=55)

    price=models.IntegerField()
    category=models.ForeignKey(category,on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=255)

    def __str__(self):
        return self.product_name
    @staticmethod
    def showproducts():
        return products.objects.all()
    @staticmethod
    def showproductsbycat(cat_id):
        return products.objects.filter(category=cat_id)
    @staticmethod
    def showproductsbypid(pid):
        return products.objects.filter(id=pid)
    



class cart_items(models.Model):
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField()   

    
    def total_price(self):
        return self.product.price*self.quantity
    
class order_table(models.Model):
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField()
    name=models.CharField(max_length=50)   
    contact_no=models.CharField(max_length=10)
    alternate_no=models.CharField(max_length=10)
    plot_no=models.TextField()
    streetaddress=models.TextField()
    city=models.CharField()
    pincode=models.PositiveBigIntegerField()
    order_date = models.DateTimeField(default=timezone.now)
    delivered=False

    def total_price(self):
        return self.product.price*self.quantity
    

