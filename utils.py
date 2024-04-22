import requests
import requests
import json
import time
import random
from datetime import datetime
import threading
from discord_webhook import *
import csv
from colorama import Fore, Style, init

lock = threading.Lock()

def log(content):
    with lock:
        print(f'[{datetime.now()}] {Fore.LIGHTBLUE_EX}{content}{Style.RESET_ALL}')
def log_success(content):
    with lock:
        print(f'[{datetime.now()}] {Fore.LIGHTGREEN_EX}{content}{Style.RESET_ALL}')
def log_error(content):
    with lock:
        print(f'[{datetime.now()}] {Fore.LIGHTRED_EX}{content}{Style.RESET_ALL}')   

headers = {
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'dnt': '1',
                'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            }
    
def fetch_coordinates(city):
    headers = {
            'authority': 'maps.googleapis.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.104", "Not A(Brand";v="24.0.0.0", "Google Chrome";v="110.0.5481.104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'x-client-data': 'CK+1yQEIhLbJAQiltskBCMS2yQEIqZ3KAQiQi8sBCJOhywEIzuHMAQjR9cwBCISMzQEIx43NAQjTjc0BCLCPzQEIjJPNAQj1k80BCNLhrAI=',
        }

    params = {
            'key': 'AIzaSyDdyfolbJMdjMA-gWzUiw-rqBAcGDD4NPI',
            'address': city,
        }

    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params, headers=headers)
    lat = round(response.json()['results'][0]['geometry']['location']['lat'],2)
    lng =  round(response.json()['results'][0]['geometry']['location']['lng'],2)
    return {"lat":lat,"lng":lng}

def fetch_stores(city):
    SHOPS = list()
    coordinates = fetch_coordinates(city)
    headers = {
        'authority': 'api.nike.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
    
    country = 'POLAND'
    max_dist = '20'
    units = 'km'
    latutide = coordinates.get('lat')
    longitude = coordinates.get('lng')

    ep2 = f'https://api.nike.com/store/store_locations/v1?language=pl-PL&search=%28%28%28brand%3D%3DNIKE%20and%20facilityType%3D%3DNIKE_OWNED_STORE%20or%20facilityType%3D%3DFRANCHISEE_PARTNER_STORE%20or%20facilityType%3D%3DMONO_BRAND_NON_FRANCHISEE_PARTNER_STORE%20and%20%28region%21%3D{country}%29%29%20and%20%28businessConcept%21%3DEMPLOYEE_STORE%20and%20businessConcept%21%3DBRAND_POP_UP%29%29%20and%20%28coordinates%3DgeoProximity%3D%7B%22maxDistance%22%3A%20{max_dist}%2C%20%22measurementUnits%22%3A%20%22{units}%22%2C%22latitude%22%3A%20{latutide}%2C%20%22longitude%22%3A%20{longitude}%7D%29%29'

    response = requests.get(ep2,  headers=headers)
    for shop in response.json()['objects']:
        if shop['locale'] == 'pl-PL':
            SHOPS.append({'id':shop['id'],'name':shop['name']})

    return SHOPS

def fetchgtin(sku):
    sizesDict = dict()
    headers = {
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'dnt': '1',
                'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            }
                
    response = requests.get('https://api.nike.com/product_feed/threads/v2?filter=language(pl)&filter=marketplace(PL)&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&filter=productInfo.merchProduct.styleColor('+sku+')',headers=headers)
    colorDescription = response.json()['objects'][0]['productInfo'][0]['productContent']['colorDescription']
    fullTitle = response.json()['objects'][0]['productInfo'][0]['productContent']['fullTitle']
    
    name = f'{fullTitle} {colorDescription}'
    link = f'https://www.nike.com/pl/t/pzdr/{sku}'
    sku2 = sku.replace('-','_')
    image = f'https://secure-images.nike.com/is/image/DotCom/{sku2}'
    price = str(response.json()['objects'][0]['productInfo'][0]['merchPrice']['currentPrice'])+f'PLN'
    for size in response.json()['objects'][0]['productInfo'][0]['skus']:
        sizesDict[size['gtin']] = size['countrySpecifications'][0]['localizedSize']
    
    return [sizesDict,name,link,image,price]

def get_proxy():
    proxies_list =[]
    with open('proxy.txt') as f:
        for line in f:
            proxies_list.append(line.strip())
        f.close()

    proxy_chosen = random.choice(proxies_list)
    proxy_ditails = proxy_chosen.split(":")
    proxy = proxy_ditails
    pelneproxy = proxy[2]+":"+proxy[3]+"@"+proxy[0]+":"+proxy[1]
    proxies = {
        'http': 'http://'+pelneproxy,
        'https': 'http://'+pelneproxy}
    return proxies

def fetchProductID(SKU) -> str:
    urlx = "https://api.nike.com/product_feed/threads/v2/?filter=marketplace%28PL%29&filter=language%28pl%29&filter=channelId%28d9a5bc42-4b9c-4976-858a-f159cf99c647%29&&filter=productInfo.merchProduct.styleColor(" + str(SKU).upper() + ")"
    
    product_page = requests.get(url=urlx, headers = headers , timeout=10,proxies=get_proxy())

    if product_page.status_code == 200:
        jsonData = json.loads(product_page.content)
        objects = jsonData["objects"]
        if not objects:
            return fetchProductIDSNKRS(SKU)
        else:   
            nodes = objects[0]
            ProductID = nodes["productInfo"][0]["merchProduct"]['id']
            return ProductID    
        

def fetchProductIDSNKRS(SKU) -> str:
    urlsnkrs = 'https://api.nike.com/product_feed/threads/v2/?filter=marketplace%28PL%29&filter=language%28pl%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&&filter=exclusiveAccess%28true%2Cfalse%29&filter=productInfo.merchProduct.styleColor(' + str(SKU).upper() + ")"    
   
    product_page = requests.get(url=urlsnkrs, headers = headers, timeout=10,proxies=get_proxy())

    if product_page.status_code == 200:
        jsonData = json.loads(product_page.content)
        objects = jsonData["objects"]
        if objects: 
            nodes = objects[0]
            ProductID = nodes["productInfo"][0]["merchProduct"]['id']
            return ProductID


def webhook(webhook_type,sku,shopid,shopname):
    productID = fetchProductID(sku)
    productDATA = fetchgtin(sku)
    sizeDict = productDATA[0]
    name = productDATA[1]
    link = productDATA[2]
    image = productDATA[3]
    price = productDATA[4]

    response2 = requests.get('https://api.nike.com/deliver/available_gtins/v3?filter=styleColor('+sku+')&filter=storeId('+shopid+')&filter=method(INSTORE)', headers=headers)
    if response2.status_code == 200:
        sizes = list()
        dates=list()
        try:
            for size in response2.json()['objects']:
                try:
                    sizeEU = sizeDict[size['gtin']]
                except KeyError:continue

                stock = size['level']
                available = size['available']
                modificationDate = size['modificationDate']

                import dateutil.parser as dp
                from datetime import datetime, timedelta
                modificationDate = dp.parse(modificationDate)
                modificationDate_plus_2_hours = modificationDate + timedelta(hours=2)
                
                formated_date = "<t:"+str(dp.parse(str(modificationDate_plus_2_hours)).timestamp()).split('.')[0] + '>\n'
                
                if available == True:
                    if stock != "OUT_OF_STOCK":
                        sizes.append(f'{sizeEU} [{stock}]\n')
                        dates.append(formated_date)
                    
        except Exception as er:
            log_error(str(er))
       

    discord_url = 'paste here url'
    webhook = DiscordWebhook(url=discord_url,rate_limit_retry=True, username = f'Nike Instore',avatar_url='https://i.imgur.com/RWFzrEi.png')
    embed = DiscordEmbed(title=f"{name}",description=f"{shopname}\n**{webhook_type}**",url=link, color='0x50d68d')
    embed.set_thumbnail(url = image)
    embed.add_embed_field(name='Price:', value=price,inline=True)
    embed.add_embed_field(name='StockX', value=f"[{sku}](https://stockx.com/search?s={sku})",inline=False)
    e = sizes
    embed.add_embed_field(name='Size [Stock]',value=f'{" ".join(e)}',inline=True)
    embed.add_embed_field(name='Modification Date',value=f'{" ".join(dates)}',inline=True)
    embed.set_timestamp()
    webhook.add_embed(embed)
    response = webhook.execute()
