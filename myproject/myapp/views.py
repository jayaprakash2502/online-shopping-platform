from django.shortcuts import render,redirect
from .models import customer
from .models import products,category,cart_items,order_table
from django.contrib.auth.hashers import check_password,make_password
from django.contrib import messages
from django.http import JsonResponse




def signup(request):
    if request.method == 'POST':
        userdata = request.POST
        error = validateData(userdata)
        
        if error:
            return render(request, 'signup.html', {"error": error})
        
        isexist = customer.emailexists(userdata['email'])
        
        
        if isexist is None:
            customer.objects.create(
                name=userdata['name'],
                password=make_password(userdata['password']),
                email=userdata['email'],
                phone=userdata['phone']
            )
            
            return redirect('login')

        return render(request, 'signup.html', {'error': 'email already exists'})
    
    return render(request, 'signup.html')
    

def validateData(userData):
		error = {}
		if not userData['name'] or not userData['email']  or not userData['phone']  or not userData['password'] or not userData['confirm_password']:
			error["field_error"] = "All field must be required"
		elif len(userData['password'])<8 and len(userData['confirm_password'])<8 :
			error['minPass_error'] = "Password must be 8 char"
		elif len(userData['name']) > 25 or len(userData['name']) < 3 :
			error["name_error"] = "Name must be 3-25 charecter"
		elif len(userData['phone']) != 10:
			error["phoneNumber_error"] = "Phone number must be 10 charecter."
		elif userData['password'] != userData['confirm_password']:
			error["notMatch_error"] = "Password doesn't match"	

		return error if error else None

def login(request):
	if(request.method=='POST'):
		userdata=request.POST
		isexist=customer.emailexists(userdata['email'])
		if isexist is None:
			return render(request,'login.html',{'error':'email is not registered'})
		if check_password(request.POST['password'],isexist.password):
			request.session['customer']=isexist.id
			request.session['customer_name']=isexist.name
			return redirect('home')
		else:
			return render(request,'login.html',{'pass_error':'incorrect password'})
	return render(request,'login.html')


def home(request):
    search = request.GET.get("search", "")

    _category = category.showcategory()

    if search:
        _products = products.objects.filter(product_name__icontains=search)
		
    else:
        cat_id = request.GET.get('category_id')
        if cat_id:
            _products = products.showproductsbycat(cat_id)
        else:
            _products = products.showproducts()

    return render(request, 'home.html', {
        'products': _products,
        'category': _category
    })



def product_detail(request):
	if(request.method=='GET'):
		productid=request.GET.get('product_id')
		productdetails=products.showproductsbypid(productid)
		return render(request,'product_detail.html',{'products':productdetails})

def addtocart(request):
	if(request.method=='GET'):
		customer_id = request.session.get('customer')
		if not customer_id:
			return redirect('login')
		product_id=request.GET.get('product_id')
		product=products.objects.get(id=product_id)
		customer_instance=customer.objects.get(id=customer_id)
		

		try:
			cart_products=cart_items.objects.get(customer=customer_instance,product=product)
			cart_products.quantity+=1
			cart_products.save()
		
		except:
			cart_items.objects.create(customer=customer_instance,product=product,quantity=1)
		return redirect('cart_item')


def cart_item(request):
	customer_id=request.session.get('customer')
	if not customer_id:
		return redirect('login')
	customer_instance=customer.objects.get(id=customer_id)
	cart_products=cart_items.objects.filter(customer=customer_instance)
	sum=0
	
	for i in cart_products:
		sum+=i.total_price()

	return render(request,'cart_item.html',{'cart_items':cart_products,'totalprice':sum})
	
def update_quantity(request):
    if request.method == 'GET':
        customer_id = request.session.get('customer')
        if not customer_id:
            return redirect('login')

        customer_instance = customer.objects.get(id=customer_id)

        if request.GET.get('productid_increase'):
                increament = request.GET.get('productid_increase')
                plus = cart_items.objects.get(id=increament, customer=customer_instance)
                plus.quantity += 1
                plus.save()

        elif request.GET.get('productid_decrease'):
                decreament = request.GET.get('productid_decrease')
                minus = cart_items.objects.get(id=decreament, customer=customer_instance)
                if minus.quantity > 1:
                    minus.quantity -= 1
                    minus.save()
                else:
                    minus.delete()
        
        previous_url = request.META.get('HTTP_REFERER', 'cart_item')
        return redirect(previous_url)

        
    return redirect('cart_item')


def check_out(request):
	if(request.method=='GET'):
		customerid=request.session.get('customer')
		if not customer:
			return redirect('login')
		customer_instance=customer.objects.get(id=customerid)
		cart_products=cart_items.objects.filter(customer=customer_instance)
		order_data=[]
		for item in cart_products:
			order_data.append({
				'product_id':item.product.id,
				'product_name':item.product.product_name,
				'quantity':item.quantity,
				'price':item.product.price	
			})
		request.session['order_data']=order_data
		
		return redirect('order_form')
	
def order_form(request):
	customerid=request.session.get('customer')
	if not customerid:
		return redirect('login')
	customer_instance=customer.objects.get(id=customerid)
	
	order_data=request.session.get('order_data',[])
	if request.method=='POST':
		name=request.POST['name']
		contact_no=request.POST['contact_no']
		alternate_no=request.POST['alternate_no']
		plot_no=request.POST['plot_no']
		streetaddress=request.POST['streetaddress']
		city=request.POST['city']
		pincode=request.POST['pincode']
		
		for item in order_data:
			product_instance=products.objects.get(id=item['product_id'])
			order_table.objects.create(
				customer=customer_instance,
				product=product_instance,
				quantity=item['quantity'],
				name=name,
				contact_no=contact_no,
				alternate_no=alternate_no,
				plot_no=plot_no,
				streetaddress=streetaddress,
				city=city,
				pincode=pincode,
				
			)
		
		del request.session['order_data']
		messages.success(request, " Your order has been placed successfully!")
		cart_products=cart_items.objects.filter(customer=customer_instance)
		cart_products.delete()
		return redirect('orders_page')

		

	return render(request,'order_form.html')
		

def orders_page(request):
	customerid=request.session.get('customer')
	if not customerid:
		return redirect('login')
	customer_instance=customer.objects.get(id=customerid)
	order_products=order_table.objects.filter(customer=customer_instance)
	for item in order_products:
		if not item.delivered:
			item.delivered="pending"
			item.save()
		else:
			item.delivered="completed"
			item.save()
		

	
	return render(request,'orders_page.html',{'order_products':order_products})

def logout(request):
	request.session.clear()
	return redirect('home')