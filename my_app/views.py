from django.shortcuts import render
from . import models
#Web Scrapping Libraries
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
#for visualizations
import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go

# Create your views here.
BASE_CRAIGSLIST_URL = 'https://{a}.craigslist.org/search/?query={b}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def New_Search(request):

    search = request.POST.get('search')

    if request.method == "POST":
        city = request.POST.get('rose')

    min_price = request.POST.get('min_price')
    max_price = request.POST.get('max_price')

    models.Search.objects.create(search=search,minimum_price=min_price,maximum_price=max_price,city_name=city)

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

    return render(request,'my_app/new_search.html',context = {'search_item':search,'city':city,'final_postings':final_postings})

def Analytics_Page(request):
    search_db = models.Search.objects.values()
    search_df = pd.DataFrame(search_db)
    search_key = pd.DataFrame(search_df.groupby(['search'])['id'].count())

    search_key.reset_index(inplace = True)
    search_key.sort_values(by='id', ascending=False,inplace = True)
    search_key = search_key.head(10)

    plot_div = go.Bar(x=search_key['search'], y=search_key['id'],
                        opacity=0.8, marker_color='rgb(217, 78, 99)')
    data=go.Data([plot_div])
    layout=go.Layout(title=" Most Searched Keywords", xaxis={'title':'Keywords'}, yaxis={'title':'Count'})
    figure=go.Figure(data=data,layout=layout)
    bar_plot = plot(figure, auto_open=False, output_type='div')


    citywise = pd.DataFrame(search_df.groupby(['city_name'])['id'].count())
    citywise.reset_index(inplace = True)
    citywise.sort_values(by='id', ascending=False,inplace = True)

    fig = go.Pie(labels=citywise['city_name'], values=citywise['id'], textinfo='label+percent',
                                 insidetextorientation='radial'
                                )
    dat=go.Data([fig])
    lay=go.Layout(title=" City Wise Searches")
    figue=go.Figure(data=dat,layout=lay)
    pie_plot = plot(figue, auto_open=False, output_type='div')

    return render(request,'my_app/analytics.html',context={'search_db':search_db,'bar_plot': bar_plot,'pie_plot':pie_plot})
