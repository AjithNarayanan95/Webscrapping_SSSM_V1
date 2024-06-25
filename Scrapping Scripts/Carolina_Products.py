from module_package import *
from zenrows import ZenRowsClient


def write_visited_log(url):
    with open(f'Visited_Carolina_urls.txt', 'a', encoding='utf-8') as file:
        file.write(f'{url}\n')


def read_log_file():
    if os.path.exists(f'Visited_Carolina_urls.txt'):
        with open(f'Visited_Carolina_urls.txt', 'r', encoding='utf-8') as read_file:
            return read_file.read().split('\n')
    return []


if __name__ == '__main__':
    timestamp = datetime.now().date().strftime('%Y%m%d')
    file_name = os.path.basename(__file__).rstrip('.py')
    url = 'https://www.carolina.com/'
    base_url = 'https://www.carolina.com'
    soup = get_zenrowa(url, params = {'js_render': 'false'})
    content = soup.find('li', class_='nav-item c-nav-menu-link').find_all('li', class_='row c-nav-menu-l1')
    for single_content in content:
        inner_content = single_content.find('div', class_='c-nav-menu-subnav col-12 col-lg-7')
        product_category = inner_content.find('h3', class_='d-none d-lg-block').text.strip()
        if inner_content.find('ul', class_='row'):
            all_urls = inner_content.find('ul', class_='row').find_all('li')
            for single_url in all_urls:
                product_sub_category = single_url.a.text.strip()
                main_url = f"{base_url}{single_url.a['href']}"
                print(f'main_url -----------> {main_url}')
                if main_url in read_log_file():
                    continue
                inner_request = get_zenrowa(main_url, params = {'js_render': 'false'})
                if inner_request is None:
                    continue
                if inner_request.find('div', class_='row px-1'):
                    inner_data = inner_request.find('div', class_='row px-1').find_all('a', class_='c-category-list')
                    for single_data in inner_data:
                        inner_url = f'{base_url}{single_data["href"]}'
                        inner_category = strip_it(single_data.find('h3', class_='c-category-title').text.strip())
                        product_sub_category = f'{product_sub_category}-{inner_category}'
                        other_request = get_zenrowa(inner_url, params = {'js_render': 'false'})
                        '''GET PAGINATION'''
                        if other_request.find('ul', class_='c-pagination pagination justify-content-start pagination-lg'):
                            total_page = other_request.find('ul', class_='c-pagination pagination justify-content-start pagination-lg').find_all(
                                'li')[-2].text.strip()
                            for i in range(0, int(total_page)):
                                number = int(i) * int(60)
                                page_link = f'{main_url}?Nf=product.cbsLowPrice%7CGT+0.0%7C%7Cproduct.startDate%7CLTEQ+1.71504E12%7C%7Cproduct.startDate%7CLTEQ+1.71504E12&No={number}&Nr=&'
                                if page_link in read_log_file():
                                    continue
                                page_soup = get_zenrowa(page_link, params = {'js_render': 'false'})
                                if page_soup is None:
                                    continue
                                inner_data = page_soup.find_all('div', class_='c-feature-product qv-model')
                                for single_data in inner_data:
                                    product_url = f'{base_url}{single_data.find("a")["href"]}'
                                    print(product_url)
                                    product_request = get_zenrowa(product_url, params = {'js_render': 'true', "premium_proxy": "true", "proxy_country": "us"})
                                    if product_request is None:
                                        continue
                                    '''PRODUCT NAME AND PRODUCT QUANTITY'''
                                    try:
                                        product_name = strip_it(product_request.find('div', class_='col prod-nav-title').text.strip())
                                        if re.search('Pack of \d+', str(product_name)):
                                            product_quantity = re.search('Pack of \d+', str(product_name)).group().replace('Pack of', '').strip()
                                        else:
                                            product_quantity = strip_it(product_request.find('input', attrs={'name': 'quantity'})['value'])
                                    except:
                                        product_name = ''
                                        product_quantity = '1'
                                    '''PRODUCT NAME'''
                                    try:
                                        product_id = strip_it(product_request.find('span', id='pdp-skuId').text.strip())
                                    except:
                                        product_id = ''
                                    '''PRODUCT PRICE'''
                                    try:
                                        if product_request.find('span', class_='pdp-order-price'):
                                            product_price = strip_it(product_request.find('span', class_='pdp-order-price').text.strip())
                                        elif product_request.find('div', class_='pdp-order-price'):
                                            product_price = strip_it(product_request.find('div', class_='pdp-order-price').text.strip())
                                        else:
                                            product_price = ''
                                    except Exception as e:
                                        print('product price', e)
                                        product_price = ''
                                    if product_id in read_log_file():
                                        continue
                                    print('current datetime------>', datetime.now())
                                    dictionary = {
                                        'Carolina_product_category': product_category,
                                        'Carolina_product_sub_category': product_sub_category,
                                        'Carolina_product_id': product_id,
                                        'Carolina_product_name': product_name,
                                        'Carolina_product_quantity': product_quantity,
                                        'Carolina_product_price': product_price,
                                        'Carolina_product_url': product_url
                                    }
                                    articles_df = pd.DataFrame([dictionary])
                                    articles_df.drop_duplicates(subset=['Carolina_product_id', 'Carolina_product_name'], keep='first',
                                                                inplace=True)
                                    if os.path.isfile(f'{file_name}.csv'):
                                        articles_df.to_csv(f'{file_name}.csv', index=False, header=False,
                                                           mode='a')
                                    else:
                                        articles_df.to_csv(f'{file_name}.csv', index=False)
                                    write_visited_log(product_id)
                                write_visited_log(page_link)
                        else:
                            inner_data = other_request.find_all('div', class_='c-feature-product qv-model')
                            for single_data in inner_data:
                                product_url = f'{base_url}{single_data.find("a")["href"]}'
                                print(product_url)
                                product_request = get_zenrowa(product_url, params = {'js_render': 'true', "premium_proxy": "true", "proxy_country": "us"})
                                if product_request is None:
                                    continue
                                '''PRODUCT NAME AND PRODUCT QUANTITY'''
                                try:
                                    product_name = strip_it(product_request.find('div', class_='col prod-nav-title').text.strip())
                                    if re.search('Pack of \d+', str(product_name)):
                                        product_quantity = re.search('Pack of \d+', str(product_name)).group().replace(
                                            'Pack of', '').strip()
                                    else:
                                        product_quantity = strip_it(product_request.find('input', attrs={'name': 'quantity'})['value'])
                                except:
                                    product_name = ''
                                    product_quantity = '1'
                                '''PRODUCT NAME'''
                                try:
                                    product_id = strip_it(product_request.find('span', id='pdp-skuId').text.strip())
                                except:
                                    product_id = ''
                                '''PRODUCT PRICE'''
                                try:
                                    if product_request.find('span', class_='pdp-order-price'):
                                        product_price = strip_it(product_request.find('span', class_='pdp-order-price').text.strip())
                                    elif product_request.find('div', class_='pdp-order-price'):
                                        product_price = strip_it(product_request.find('div', class_='pdp-order-price').text.strip())
                                    else:
                                        product_price = ''
                                except Exception as e:
                                    print('product price', e)
                                    product_price = ''
                                if product_id in read_log_file():
                                    continue
                                print('current datetime------>', datetime.now())
                                dictionary = {
                                    'Carolina_product_category': product_category,
                                    'Carolina_product_sub_category': product_sub_category,
                                    'Carolina_product_id': product_id,
                                    'Carolina_product_name': product_name,
                                    'Carolina_product_quantity': product_quantity,
                                    'Carolina_product_price': product_price,
                                    'Carolina_product_url': product_url
                                }
                                articles_df = pd.DataFrame([dictionary])
                                articles_df.drop_duplicates(subset=['Carolina_product_id', 'Carolina_product_name'], keep='first', inplace=True)
                                if os.path.isfile(f'{file_name}.csv'):
                                    articles_df.to_csv(f'{file_name}.csv', index=False, header=False,
                                                       mode='a')
                                else:
                                    articles_df.to_csv(f'{file_name}.csv', index=False)
                                write_visited_log(product_id)
                else:
                    '''GET PAGINATION'''
                    if inner_request.find('ul', class_='c-pagination pagination justify-content-start pagination-lg'):
                        total_page = inner_request.find('ul', class_='c-pagination pagination justify-content-start pagination-lg').find_all(
                            'li')[-2].text.strip()
                        for i in range(0, int(total_page)):
                            number = int(i) * int(60)
                            page_link = f'{main_url}?Nf=product.cbsLowPrice%7CGT+0.0%7C%7Cproduct.startDate%7CLTEQ+1.71504E12%7C%7Cproduct.startDate%7CLTEQ+1.71504E12&No={number}&Nr=&'
                            if page_link in read_log_file():
                                continue
                            page_soup = get_zenrowa(page_link, params = {'js_render': 'false'})
                            if page_soup is None:
                                continue
                            inner_data = page_soup.find_all('div', class_='c-feature-product qv-model')
                            for single_data in inner_data:
                                product_url = f'{base_url}{single_data.find("a")["href"]}'
                                print(product_url)
                                product_request = get_zenrowa(product_url, params = {'js_render': 'true', "premium_proxy": "true", "proxy_country": "us"})
                                if product_request is None:
                                    continue
                                '''PRODUCT NAME AND PRODUCT QUANTITY'''
                                try:
                                    product_name = strip_it(product_request.find('div', class_='col prod-nav-title').text.strip())
                                    if re.search('Pack of \d+', str(product_name)):
                                        product_quantity = re.search('Pack of \d+', str(product_name)).group().replace('Pack of', '').strip()
                                    else:
                                        product_quantity = strip_it(product_request.find('input', attrs={'name': 'quantity'})['value'])
                                except:
                                    product_name = ''
                                    product_quantity = '1'
                                '''PRODUCT NAME'''
                                try:
                                    product_id = strip_it(product_request.find('span', id='pdp-skuId').text.strip())
                                except:
                                    product_id = ''
                                '''PRODUCT PRICE'''
                                try:
                                    if product_request.find('span', class_='pdp-order-price'):
                                        product_price = strip_it(product_request.find('span', class_='pdp-order-price').text.strip())
                                    elif product_request.find('div', class_='pdp-order-price'):
                                        product_price = strip_it(product_request.find('div', class_='pdp-order-price').text.strip())
                                    else:
                                        product_price = ''
                                except Exception as e:
                                    print('product price', e)
                                    product_price = ''
                                if product_id in read_log_file():
                                    continue
                                print('current datetime------>', datetime.now())
                                dictionary = {
                                    'Carolina_product_category': product_category,
                                    'Carolina_product_sub_category': product_sub_category,
                                    'Carolina_product_id': product_id,
                                    'Carolina_product_name': product_name,
                                    'Carolina_product_quantity': product_quantity,
                                    'Carolina_product_price': product_price,
                                    'Carolina_product_url': product_url
                                }
                                articles_df = pd.DataFrame([dictionary])
                                articles_df.drop_duplicates(subset=['Carolina_product_id', 'Carolina_product_name'], keep='first',
                                                            inplace=True)
                                if os.path.isfile(f'{file_name}.csv'):
                                    articles_df.to_csv(f'{file_name}.csv', index=False, header=False,
                                                       mode='a')
                                else:
                                    articles_df.to_csv(f'{file_name}.csv', index=False)
                                write_visited_log(product_id)
                            write_visited_log(page_link)
                    else:
                        inner_data = inner_request.find_all('div', class_='c-feature-product qv-model')
                        for single_data in inner_data:
                            product_url = f'{base_url}{single_data.find("a")["href"]}'
                            print(product_url)
                            product_request = get_zenrowa(product_url, params = {'js_render': 'true', "premium_proxy": "true", "proxy_country": "us"})
                            if product_request is None:
                                continue
                            '''PRODUCT NAME AND PRODUCT QUANTITY'''
                            try:
                                product_name = strip_it(product_request.find('div', class_='col prod-nav-title').text.strip())
                                if re.search('Pack of \d+', str(product_name)):
                                    product_quantity = re.search('Pack of \d+', str(product_name)).group().replace(
                                        'Pack of', '').strip()
                                else:
                                    product_quantity = strip_it(product_request.find('input', attrs={'name': 'quantity'})['value'])
                            except:
                                product_name = ''
                                product_quantity = '1'
                            '''PRODUCT NAME'''
                            try:
                                product_id = strip_it(product_request.find('span', id='pdp-skuId').text.strip())
                            except:
                                product_id = ''
                            '''PRODUCT PRICE'''
                            try:
                                if product_request.find('span', class_='pdp-order-price'):
                                    product_price = strip_it(product_request.find('span', class_='pdp-order-price').text.strip())
                                elif product_request.find('div', class_='pdp-order-price'):
                                    product_price = strip_it(product_request.find('div', class_='pdp-order-price').text.strip())
                                else:
                                    product_price = ''
                            except Exception as e:
                                print('product price', e)
                                product_price = ''
                            if product_id in read_log_file():
                                continue
                            print('current datetime------>', datetime.now())
                            dictionary = {
                                'Carolina_product_category': product_category,
                                'Carolina_product_sub_category': product_sub_category,
                                'Carolina_product_id': product_id,
                                'Carolina_product_name': product_name,
                                'Carolina_product_quantity': product_quantity,
                                'Carolina_product_price': product_price,
                                'Carolina_product_url': product_url
                            }
                            articles_df = pd.DataFrame([dictionary])
                            articles_df.drop_duplicates(subset=['Carolina_product_id', 'Carolina_product_name'], keep='first', inplace=True)
                            if os.path.isfile(f'{file_name}.csv'):
                                articles_df.to_csv(f'{file_name}.csv', index=False, header=False,
                                                   mode='a')
                            else:
                                articles_df.to_csv(f'{file_name}.csv', index=False)
                            write_visited_log(product_id)
                write_visited_log(main_url)