from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventory.models import product,cat
from django.views.decorators.csrf import csrf_exempt
import csv


# Create your views here.
def logout_view(request):
	logout(request)
	#return render_to_response('/')

def login_form(request):
	username=password=''
	if request.POST:
		username=request.POST['username']
		password=request.POST['password']

		user=authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect('/dashboard')
			else:
				messages.error(request,"Invalid username or password")
		else:
				messages.error(request,"Invalid username or password")
	return render(request=request,template_name="login/login.html")

@login_required
def dashboard(request):
	items=product.objects.order_by('category')
	graph_data=product.objects.raw('select * from (select id,category,sum(units) as units from inventory_product group by category UNION select id,p_category,1-1 from inventory_cat where p_category NOT IN (select category from inventory_product group by category)) group by category')
	
	category=cat.objects.order_by('p_category')

	my_context3={"items":items,"graph_data":graph_data,"category":category}
	return render(request,'main/index.html',my_context3)

@login_required
def Product(request):
	if request.POST and 'delete_selected' in request.POST:
		delete_products=request.POST.getlist('item_name')
		for item in delete_products:
			product.objects.filter(name=item).delete()

	items=product.objects.all()
	cats=cat.objects.all()
	my_context={
	"my_text":items,
	"categories":cats,
	}
	return render(request,'main/product.html',my_context)

@csrf_exempt
@login_required
def add_product(request):
	if request.POST:
		#id1=product.get_by_id(int(str(self.request.get("id"))))
		name=request.POST.get('pname')
		category=request.POST.get('pcategory')
		price=request.POST.get('pprice')
		expire_date=request.POST.get('pexpire_date')
		units=request.POST.get('punits')
		add_category=request.POST.get('category')
		add_cat=request.POST.get('category')
		units_capacity=request.POST.get('units')	

		if 'add-product' in request.POST:
			add=product(name=name,category=category,price=price,expire_date=expire_date,units=units)			
			add.save()
			messages.success(request,'product added successfully')

		else:
			add_category=cat(p_category=add_cat,capacity=units_capacity)			
			add_category.save()
			messages.success(request,'category added successfully')
		
	all_category=cat.objects.all()
	my_context2={
		"categories":all_category
		}	
	return render(request,'main/add-product.html',my_context2)

@login_required
def accounts(request):
	all_user=User.objects.all()
	if request.POST and 'add-user' in request.POST:
		username=request.POST.get('usr')
		password=request.POST.get('pass')
		pass2=request.POST.get('pass2')
		email=request.POST.get('email')

		if password==pass2:
			if User.objects.filter(username=username).exists():
				messages.error(request,'Username already exist')
			else:
				user=User.objects.create_superuser(username=True,password=password,email=email)
				user=User.objects.get(username='True')
				user.username=username
				user.save()
				user=authenticate(username=username,password=password)
				
				if user:
					messages.success(request,'User added successfully')
				else:
					messages.error(request,'Something went wrong')
		else:
			messages.error(request,'passwords doesn\'t match')					
	
	if request.POST and 'delete_selected' in request.POST:
		users=request.POST.getlist('account')
		for usr in users:
			User.objects.get(username=usr, is_superuser=True).delete()
		messages.success(request,'account deleted successfully')

	my_context4={
	"users":all_user
	}			

	return render(request,'main/account.html',my_context4)	

@login_required
def report(request):
	report_table=product.objects.raw('select id,category,sum(units) as units,sum(cost) as cost from (select id,category,units,units*price as cost from inventory_product) group by category')
	total_cost=0
	total_units=0

	for item in report_table:
		total_units += item.units
		total_cost += item.cost

	my_context5={
	"report_table":report_table,
	"total_cost":total_cost,
	"total_units":total_units
	}
	return render(request,'main/report.html',my_context5)

def export_product_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['product name', 'category', 'price', 'expire-date','units'])

    items = product.objects.all().values_list('name', 'category', 'price', 'expire_date','units')
    for item in items:
        writer.writerow(item)

    return response

@login_required
def edit_product(request,pk):
	item=product.objects.filter(id=pk)
	my_context6={
	"item":item,
	}

	if request.POST and 'save_product' in request.POST:
		product.objects.filter(id=pk).update(name=request.POST.get('pname'),price=request.POST.get('pprice'),units=request.POST.get('punits'))
		messages.success(request,"Updated successfully")

	if request.POST and 'delete_product' in request.POST:
		item.delete()
		return redirect('product')

	return render(request,'main/edit.html',my_context6)

@login_required
def search_product(request):
	
	item=request.POST.get('search_product')
	item='\'%{}%\''.format(item)
	items=product.objects.raw('select * from inventory_product where name like {}'.format(item))
		
	cats=cat.objects.all()
	
	my_context7={
	"my_text":items,
	"categories":cats,
	}
	return render(request,'main/product.html',my_context7)

