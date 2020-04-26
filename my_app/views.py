
import requests
from django.shortcuts import render
from . import models
from requests.compat import quote_plus
from bs4 import BeautifulSoup
import datetime

BASE_JUMIA_URL = 'https://www.jumia.com.ng/catalog/?q={}'
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('Tobi')
    models.Search.objects.create(search=search)
    final_url = BASE_JUMIA_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    product_listings = soup.find_all('div',{'class':'sku -gallery'})


    final_products = []
    for i in product_listings:
        product_title = i.find(class_='name').text
        product_url = i.find('a').get('href')
        product_price = i.find(class_='price').text
        product_image = i.find('img').get('data-src')

        final_products.append((product_title, product_url, product_price, product_image))


    #print(data)
    context = {'search': search,'final_products': final_products}
    return render(request, 'my_app/new_search.html', context)
