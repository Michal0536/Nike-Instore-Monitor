from utils import *
links = list()
init(convert=True)
init(autoreset=True)

def monitor(sku):
    cities = list()
    with open('stores.csv') as csvStoreFile:
        csvReader = csv.reader(csvStoreFile)
        for row in csvReader:
            cities.append(row[0])

    log_success(f"Starting monitoring {Fore.RED}{sku}{Fore.LIGHTGREEN_EX} in {Fore.BLUE}{', '.join(cities)}...")
    shops = list()
    
    #Fetch stores in city
    for shop in cities:
        with lock:
            for store in fetch_stores(shop):
                shops.append(store)
    
    sizeDict = fetchgtin(sku)[0]
    checkDICT = dict()
    for shop in shops:
        shopID = shop['id']
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
        response = requests.get('https://api.nike.com/deliver/available_gtins/v3?filter=styleColor('+sku+')&filter=storeId('+shopID+')&filter=method(INSTORE)', headers=headers)
        if response.status_code == 200:
            try:
                checkDICT[shop['name']] = {}
                temp = list()
                for size in response.json()['objects']:
                    timesatmp = size.get("modificationDate")
                    temp.append(timesatmp)

                    checkDICT[shop['name']]["amount"] = max(temp)
                   
            except KeyError:continue
            except Exception as e:
                log_error(f"[{sku}] Scraping error: "+str(e))
                continue

    while True:
        if sku not in links:
            log(Fore.RED+f'Removed from monitor {Fore.GREEN}{sku}'+Style.RESET_ALL)
            break

        for shop in shops:
            
            shopID = shop['id']
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
            response2 = requests.get('https://api.nike.com/deliver/available_gtins/v3?filter=styleColor('+sku+')&filter=storeId('+shopID+')&filter=method(INSTORE)', headers=headers)
            if response2.status_code == 200:
                try:
                    temp1 = list()
                    for size in response2.json()['objects']:
                        stock = size['level']
                        available = size['available']
                        timesatmp = size.get("modificationDate")
                        
                        temp1.append(timesatmp)

                    checkamount = max(temp1)

                except KeyError:continue
                except Exception as e:
                    log_error(str(e))
                    continue
            
                if datetime.fromisoformat(checkDICT[shop['name']]['amount']) < datetime.fromisoformat(checkamount):
                    #RESTOCK
                    log_success(f'[{sku}] {Fore.RED}[{checkDICT[shop["name"]]["amount"]}] [{checkamount}]{Fore.LIGHTGREEN_EX} Restocked {Fore.LIGHTBLUE_EX}{shop["name"]}')
                    checkDICT[shop['name']]["amount"] = checkamount

                    webhook(sku,shop['id'],shop['name'])

                if datetime.fromisoformat(checkDICT[shop['name']]['amount']) == datetime.fromisoformat(checkamount):
                    continue

        log(f"{Fore.GREEN}[{sku}]{Fore.LIGHTBLUE_EX} Monitoring {Fore.BLUE}{', '.join(cities)}...")  
        time.sleep(10)
    

with open('skus.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        links.append(row[0])
        
for link in links:
    thread = threading.Thread(target=monitor,args=(link,))
    thread.start()

while True:
    links1  = []
    with open('skus.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            links1.append(row[0])
    
    time.sleep(10)
    links2  = []
    with open('skus.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            links2.append(row[0])
            
    if len(links1) != len(links2):
        if len(links2) > len(links1):
            diff = list(set(links2) - set(links1))
            for link in diff:
                links.append(link)
                thread = threading.Thread(target=monitor,args=(link,))
                thread.start()
        else:
            diff = list(set(links1) - set(links2))
            for link in diff:
                links.remove(link)