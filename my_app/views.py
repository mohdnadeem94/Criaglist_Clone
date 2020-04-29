from django.shortcuts import render
from . import models
#Web Scrapping Libraries
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
# Create your views here.
BASE_CRAIGSLIST_URL = 'https://{a}.craigslist.org/search/?query={b}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def Home(request):
    return render(request,'base.html')

def New_Search(request):

    search = request.POST.get('search')

    if request.method == "POST":
        city = request.POST.get('rose')
    print(city)

    min_price = request.POST.get('min_price')
    max_price = request.POST.get('max_price')

    models.Search.objects.create(search=search)

    final_url = BASE_CRAIGSLIST_URL.format(a =city,b=quote_plus(search))
    response = requests.get(final_url)


    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://newprojects.99acres.com/projects/dgp_builders/dgp_chengleput/images/photo_not_available.gif'

        if post_price != 'N/A':
            pprice = post_price.replace('$','')
            pprice = float(pprice)
            if min_price == '':
                min_price ='0'
            if max_price == '':
                max_price ='1000000000000000000000000000'
            min_price = float(min_price)
            max_price = float(max_price)
            if pprice >=min_price and pprice <=max_price:
                final_postings.append((post_title, post_url, post_price,post_image_url))
        else:
            final_postings.append((post_title, post_url, post_price,post_image_url))
    print(search)
    print(min_price)
    print(max_price)
    return render(request,'my_app/new_search.html',context = {'search_item':search,'city':city,'final_postings':final_postings})
