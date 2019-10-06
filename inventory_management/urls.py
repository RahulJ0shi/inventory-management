"""inventory_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from inventory import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.login_form,name='login'),
    url(r'^$',views.logout_view,name='logout'),
    url('dashboard/',views.dashboard,name='dashboard'),
    url('add-product/',views.add_product,name='add_product'),
    url('product/',views.Product,name='product'),
    url('account/',views.accounts,name='account'),
    url('report/',views.report,name='report'),
    url(r'^export/csv/$', views.export_product_csv, name='export_product_csv'),
    url('edit/(?P<pk>\d+)$',views.edit_product,name='edit'),
    url('search',views.search_product,name='search_product')
]
