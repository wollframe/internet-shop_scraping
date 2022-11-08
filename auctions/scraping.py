# -*- condig: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from .models import Goods

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
}


def collect_products(url="https://rozetka.com.ua/promo/pricefall/?section_id=80004"):
    response = requests.get(url = url, headers = headers)
    c = 0
    soup = BeautifulSoup(response.text, 'lxml')
    page_cout = int(soup.find('div', class_='pagination ng-star-inserted').find_all(f'li', class_='pagination__item')[-1].text.strip())
    print(f'[INFO] Total pages: { page_cout }')
    products = ()
    for page in range(1, page_cout + 1):
        print(f'[INFO] Processing {page} page')
        url = f"https://rozetka.com.ua/promo/pricefall/?page={page}&section_id=80004"
        response = requests.get(url = url, headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('li', class_ = 'catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted')
        for item in items:
            name = item.find('a', class_ = 'goods-tile__heading ng-star-inserted', ).text.strip()
            link = item.find('a', class_ = 'goods-tile__heading ng-star-inserted').get('href').strip()
            try:
                prices = item.find('div', class_ = 'goods-tile__prices').find('p',class_ = 'ng-star-inserted').text.strip()
            except:
                prices = 'Not available'
            try:    
                images = soup.find('div', class_ = 'goods-tile__inner').find('img')['src']
            except:
                images = 'Not available'
            url = f"{link}"
            response = requests.get(url = url, headers = headers)
            soup = BeautifulSoup(response.text, 'lxml')
            description = soup.find('p', class_ = 'product-about__brief ng-star-inserted').text.strip()

            # c += 1
            # print(f'{c}) {title}')
            # print(link)
            # print(price)
            # print(image)
            # print(description)
            products += ({
                'title': name,
                'link': link,
                'price': prices,
                'image': images,
                'description':description,
            },) 

            Goods.objects.create(
                title = name,
                content = description,
                price = prices,
                content = description,
                imgage = images
            )   
    return products

if __name__ == '__main__':
    collect_products()