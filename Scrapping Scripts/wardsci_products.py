import math
import re
from module_package import *


def write_visited_log(url):
    with open(f'Visited_Wardsci_urls.txt', 'a', encoding='utf-8') as file:
        file.write(f'{url}\n')


def read_log_file():
    if os.path.exists(f'Visited_Wardsci_urls.txt'):
        with open(f'Visited_Wardsci_urls.txt', 'r', encoding='utf-8') as read_file:
            return read_file.read().split('\n')
    return []


if __name__ == '__main__':
    timestamp = datetime.now().date().strftime('%Y%m%d')
    file_name = 'Wardsci_products'
    url = 'https://www.wardsci.com/cms/products'
    base_url = 'https://www.wardsci.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    soup = get_soup(url, headers)
    content = soup.find_all('div', class_='teaser-item')[1:]
    for single_content in content:
        product_category = single_content.find('h6').text.strip()
        main_url = f"{base_url}{single_content.a['href']}"
        print(f'main_url----------------> {main_url}')
        if main_url in read_log_file():
            continue
        inner_req = get_soup(main_url, headers)
        if inner_req is None:
            continue
        inner_content = inner_req.find_all('div', class_='teaser-item')
        for single_inner_data in inner_content:
            sub_category = single_inner_data.find('h6').text.strip()
            href_tag = str(single_inner_data.a["href"]).replace(' ', '%20')
            inner_url = f'{base_url}{href_tag}'
            content_request = get_soup(inner_url, headers)
            if content_request is None:
                continue
            if content_request.find('div', class_='teaser-item'):
                other_content = content_request.find_all('div', class_='teaser-item')
                for single_tags in other_content:
                    sub_category = single_inner_data.find('h6').text.strip()
                    inner_category = single_tags.find('h6').text.strip()
                    href_tag = str(single_tags.a["href"]).replace(' ', '%20')
                    other_url = f'{base_url}{href_tag}'
                    other_request = get_soup(other_url, headers)
                    if other_request is None:
                        continue
                    if other_request.find('div', class_='teaser-item'):
                        sub_request = other_request.find_all('div', class_='teaser-item')
                        for single_sub in sub_request:
                            category = f'{sub_category} - {inner_category}'
                            inner_sub = single_sub.find('h6').text.strip()
                            product_sub_category = f'{category} - {inner_sub}'
                            href_tag = str(single_sub.a["href"]).replace(' ', '%20')
                            sub_url = f'{base_url}{href_tag}'
                            sub_soup = get_soup(sub_url, headers)
                            if sub_soup is None:
                                continue
                            if sub_soup.find('div', class_='left'):
                                page_content = strip_it(sub_soup.find('div', class_='left').text.strip())
                                split_tag = page_content.split('of', 1)
                                count = split_tag[-1].strip()
                                page_count = split_tag[0].split('-', 1)[-1].strip()
                                total_pages = math.ceil(int(count) / int(page_count))
                                for i in range(1, int(total_pages) + 1):
                                    page_link = f'{sub_url}&pageNo={i}'
                                    page_soup = get_soup(page_link, headers)
                                    if page_soup is None:
                                        continue
                                    inner_data = page_soup.find_all('div', class_='search_item')
                                    for single_data in inner_data:
                                        if 'product.jsp' not in str(single_data):
                                            '''IMAGE URL'''
                                            try:
                                                image_url = single_data.find('img', alt='Product Image')['src']
                                            except:
                                                image_url = ''
                                            name_tag = single_data.find('div', class_='search_product_name')
                                            main_name = name_tag.a.text.strip()
                                            product_url = f"{base_url}{name_tag.a['href']}"
                                            print(product_url)
                                            split_href = str(product_url).rsplit('/', 1)[0].split('product/')[
                                                -1].strip()
                                            request_url = f'https://www.wardsci.com/store/services/catalog/json/stiboOrderTableRender.jsp?productId={split_href}&catalogNumber=&discontinuedflag=&hasItemPages=false&specialCertRender=false&staticPage='
                                            product_request = get_soup(request_url, headers)
                                            if product_request is None:
                                                continue
                                            product_content = product_request.find_all('table', id='stiboGridTable')
                                            for single_product_content in product_content:
                                                content_tr_tag = single_product_content.find_all('tr',
                                                                                                 class_='productGrid')[
                                                                 1:]
                                                for single_tr in content_tr_tag:
                                                    try:
                                                        extract_tag = single_tr.find_all('td')[-1].extract()
                                                        inner_extract = single_tr.find_all('td')[-1].extract()
                                                    except:
                                                        extract_tag = ''
                                                    try:
                                                        quantity = single_tr.find_all('td')[-1].extract().text.strip()
                                                        if 'Each' in str(quantity):
                                                            product_quantity = '1'
                                                        else:
                                                            product_quantity = re.search('\d+', str(quantity)).group()
                                                    except:
                                                        product_quantity = ''
                                                    '''PRODUCT ID'''
                                                    try:
                                                        product_ids = single_tr.find_all('td')[-1].extract()
                                                        id_tag = product_ids.find('span')['id'].replace('_C',
                                                                                                        '').replace(
                                                            'CC_', '')
                                                        product_id = product_ids.text.strip()
                                                    except:
                                                        id_tag = ''
                                                        product_id = ''
                                                    try:
                                                        inner_extract_data = single_tr.find_all('td')[-1].extract()
                                                    except:
                                                        inner_extract_data = ''
                                                    '''PRODUCT DESCRIPTION'''
                                                    try:
                                                        description = single_tr.find('span',
                                                                                     itemprop="description").extract().text.strip()
                                                    except:
                                                        description = ''
                                                    '''PRODUCT NAME'''
                                                    try:
                                                        data_tag = single_tr.find_all('td')
                                                        name_list = []
                                                        for single_title in data_tag:
                                                            content_text = single_title.text.strip()
                                                            name_list.append(content_text)
                                                        product_names = ', '.join(name_list)
                                                        if main_name in product_names:
                                                            product_name = product_names
                                                        else:
                                                            product_name = f'{main_name} {product_names}'
                                                            product_name = product_name.replace(' , , ', ', ').strip(
                                                                ' , ').strip()
                                                    except:
                                                        product_name = main_name
                                                    if product_id in read_log_file():
                                                        continue
                                                    product_req_url = f'https://www.wardsci.com/store/services/pricing/json/skuPricing.jsp?skuIds={id_tag}&salesOrg=8000&salesOffice=0000&profileLocale=en_US&promoCatalogNumber=&promoCatalogNumberForSkuId=&forcePromo=false'
                                                    price_request = get_json_response(product_req_url, headers)
                                                    if price_request is None:
                                                        continue
                                                    for single_price in price_request:
                                                        product_price = single_price['salePrice']
                                                        print('current datetime------>', datetime.now())
                                                        dictionary = {
                                                            'Wardsci_product_category': product_category,
                                                            'Wardsci_product_sub_category': product_sub_category,
                                                            'Wardsci_product_id': product_id,
                                                            'Wardsci_product_name': product_name,
                                                            'Wardsci_product_quantity': product_quantity,
                                                            'Wardsci_product_price': product_price,
                                                            'Wardsci_product_url': product_url,
                                                            'Wardsci_image_url': image_url,
                                                            'Wardsci_product_desc': description
                                                        }
                                                        articles_df = pd.DataFrame([dictionary])
                                                        articles_df.drop_duplicates(
                                                            subset=['Wardsci_product_id', 'Wardsci_product_name'],
                                                            keep='first',
                                                            inplace=True)
                                                        if os.path.isfile(f'{file_name}.csv'):
                                                            articles_df.to_csv(f'{file_name}.csv', index=False,
                                                                               header=False, mode='a')
                                                        else:
                                                            articles_df.to_csv(f'{file_name}.csv', index=False)
                                                        write_visited_log(product_id)
                    else:
                        product_sub_category = f'{sub_category} - {inner_category}'
                        if other_request.find('div', class_='left'):
                            page_content = strip_it(other_request.find('div', class_='left').text.strip())
                            split_tag = page_content.split('of', 1)
                            count = split_tag[-1].strip()
                            page_count = split_tag[0].split('-', 1)[-1].strip()
                            total_pages = math.ceil(int(count) / int(page_count))
                            for i in range(1, int(total_pages) + 1):
                                page_link = f'{other_url}&pageNo={i}'
                                page_soup = get_soup(page_link, headers)
                                if page_soup is None:
                                    continue
                                inner_data = page_soup.find_all('div', class_='search_item')
                                for single_data in inner_data:
                                    if 'product.jsp' not in str(single_data):
                                        '''IMAGE URL'''
                                        try:
                                            image_url = single_data.find('img', alt='Product Image')['src']
                                        except:
                                            image_url = ''
                                        name_tag = single_data.find('div', class_='search_product_name')
                                        main_name = name_tag.a.text.strip()
                                        product_url = f"{base_url}{name_tag.a['href']}"
                                        print(product_url)
                                        split_href = str(product_url).rsplit('/', 1)[0].split('product/')[-1].strip()
                                        request_url = f'https://www.wardsci.com/store/services/catalog/json/stiboOrderTableRender.jsp?productId={split_href}&catalogNumber=&discontinuedflag=&hasItemPages=false&specialCertRender=false&staticPage='
                                        product_request = get_soup(request_url, headers)
                                        if product_request is None:
                                            continue
                                        product_content = product_request.find_all('table', id='stiboGridTable')
                                        for single_product_content in product_content:
                                            content_tr_tag = single_product_content.find_all('tr',
                                                                                             class_='productGrid')[1:]
                                            for single_tr in content_tr_tag:
                                                try:
                                                    extract_tag = single_tr.find_all('td')[-1].extract()
                                                    inner_extract = single_tr.find_all('td')[-1].extract()
                                                except:
                                                    extract_tag = ''
                                                try:
                                                    quantity = single_tr.find_all('td')[-1].extract().text.strip()
                                                    if 'Each' in str(quantity):
                                                        product_quantity = '1'
                                                    else:
                                                        product_quantity = re.search('\d+', str(quantity)).group()
                                                except:
                                                    product_quantity = ''
                                                '''PRODUCT ID'''
                                                try:
                                                    product_ids = single_tr.find_all('td')[-1].extract()
                                                    id_tag = product_ids.find('span')['id'].replace('_C', '').replace(
                                                        'CC_', '')
                                                    product_id = product_ids.text.strip()
                                                except:
                                                    id_tag = ''
                                                    product_id = ''
                                                try:
                                                    inner_extract_data = single_tr.find_all('td')[-1].extract()
                                                except:
                                                    inner_extract_data = ''
                                                '''PRODUCT DESCRIPTION'''
                                                try:
                                                    description = single_tr.find('span',
                                                                                 itemprop="description").extract().text.strip()
                                                except:
                                                    description = ''
                                                '''PRODUCT NAME'''
                                                try:
                                                    data_tag = single_tr.find_all('td')
                                                    name_list = []
                                                    for single_title in data_tag:
                                                        content_text = single_title.text.strip()
                                                        name_list.append(content_text)
                                                    product_names = ', '.join(name_list)
                                                    if main_name in product_names:
                                                        product_name = product_names
                                                    else:
                                                        product_name = f'{main_name} {product_names}'
                                                        product_name = product_name.replace(' , , ', ', ').strip(
                                                            ' , ').strip()
                                                except:
                                                    product_name = main_name
                                                if product_id in read_log_file():
                                                    continue
                                                product_req_url = f'https://www.wardsci.com/store/services/pricing/json/skuPricing.jsp?skuIds={id_tag}&salesOrg=8000&salesOffice=0000&profileLocale=en_US&promoCatalogNumber=&promoCatalogNumberForSkuId=&forcePromo=false'
                                                # print(product_req_url)
                                                price_request = get_json_response(product_req_url, headers)
                                                if price_request is None:
                                                    continue
                                                for single_price in price_request:
                                                    product_price = single_price['salePrice']
                                                    print('current datetime------>', datetime.now())
                                                    dictionary = {
                                                        'Wardsci_product_category': product_category,
                                                        'Wardsci_product_sub_category': product_sub_category,
                                                        'Wardsci_product_id': product_id,
                                                        'Wardsci_product_name': product_name,
                                                        'Wardsci_product_quantity': product_quantity,
                                                        'Wardsci_product_price': product_price,
                                                        'Wardsci_product_url': product_url,
                                                        'Wardsci_image_url': image_url,
                                                        'Wardsci_product_desc': description
                                                    }
                                                    articles_df = pd.DataFrame([dictionary])
                                                    articles_df.drop_duplicates(
                                                        subset=['Wardsci_product_id', 'Wardsci_product_name'],
                                                        keep='first',
                                                        inplace=True)
                                                    if os.path.isfile(f'{file_name}.csv'):
                                                        articles_df.to_csv(f'{file_name}.csv', index=False,
                                                                           header=False, mode='a')
                                                    else:
                                                        articles_df.to_csv(f'{file_name}.csv', index=False)
                                                    write_visited_log(product_id)
            else:
                product_sub_category = sub_category
                if content_request.find('div', class_='left'):
                    page_content = strip_it(content_request.find('div', class_='left').text.strip())
                    split_tag = page_content.split('of', 1)
                    count = split_tag[-1].strip()
                    page_count = split_tag[0].split('-', 1)[-1].strip()
                    total_pages = math.ceil(int(count) / int(page_count))
                    for i in range(1, int(total_pages)+ 1):
                        page_link = f'{inner_url}&pageNo={i}'
                        page_soup = get_soup(page_link, headers)
                        if page_soup is None:
                            continue
                        inner_data = page_soup.find_all('div', class_='search_item')
                        for single_data in inner_data:
                            if 'product.jsp' not in str(single_data):
                                '''IMAGE URL'''
                                try:
                                    image_url = single_data.find('img', alt='Product Image')['src']
                                except:
                                    image_url = ''
                                name_tag = single_data.find('div', class_='search_product_name')
                                main_name = name_tag.a.text.strip()
                                product_url = f"{base_url}{name_tag.a['href']}"
                                print(product_url)
                                split_href = str(product_url).rsplit('/', 1)[0].split('product/')[-1].strip()
                                request_url = f'https://www.wardsci.com/store/services/catalog/json/stiboOrderTableRender.jsp?productId={split_href}&catalogNumber=&discontinuedflag=&hasItemPages=false&specialCertRender=false&staticPage='
                                product_request = get_soup(request_url, headers)
                                if product_request is None:
                                    continue
                                product_content = product_request.find_all('table', id='stiboGridTable')
                                for single_product_content in product_content:
                                    content_tr_tag = single_product_content.find_all('tr', class_='productGrid')[1:]
                                    for single_tr in content_tr_tag:
                                        try:
                                            extract_tag = single_tr.find_all('td')[-1].extract()
                                            inner_extract = single_tr.find_all('td')[-1].extract()
                                        except:
                                            extract_tag = ''
                                        try:
                                            quantity = single_tr.find_all('td')[-1].extract().text.strip()
                                            if 'Each' in str(quantity):
                                                product_quantity = '1'
                                            else:
                                                product_quantity = re.search('\d+', str(quantity)).group()
                                        except:
                                            product_quantity = ''
                                        '''PRODUCT ID'''
                                        try:
                                            product_ids = single_tr.find_all('td')[-1].extract()
                                            id_tag = product_ids.find('span')['id'].replace('_C', '').replace('CC_', '')
                                            product_id = product_ids.text.strip()
                                        except:
                                            id_tag = ''
                                            product_id = ''
                                        try:
                                            inner_extract_data = single_tr.find_all('td')[-1].extract()
                                        except:
                                            inner_extract_data = ''
                                        '''PRODUCT DESCRIPTION'''
                                        try:
                                            description = single_tr.find('span',
                                                                         itemprop="description").extract().text.strip()
                                        except:
                                            description = ''
                                        '''PRODUCT NAME'''
                                        try:
                                            data_tag = single_tr.find_all('td')
                                            name_list = []
                                            for single_title in data_tag:
                                                content_text = single_title.text.strip()
                                                name_list.append(content_text)
                                            product_names = ', '.join(name_list)
                                            if main_name in product_names:
                                                product_name = product_names
                                            else:
                                                product_name = f'{main_name} {product_names}'
                                                product_name = product_name.replace(' , , ', ', ').strip(' , ').strip()
                                        except:
                                            product_name = main_name
                                        if product_id in read_log_file():
                                            continue
                                        product_req_url = f'https://www.wardsci.com/store/services/pricing/json/skuPricing.jsp?skuIds={id_tag}&salesOrg=8000&salesOffice=0000&profileLocale=en_US&promoCatalogNumber=&promoCatalogNumberForSkuId=&forcePromo=false'
                                        # print(product_req_url)
                                        price_request = get_json_response(product_req_url, headers)
                                        if price_request is None:
                                            continue
                                        for single_price in price_request:
                                            product_price = single_price['salePrice']
                                            print('current datetime------>', datetime.now())
                                            dictionary = {
                                                'Wardsci_product_category': product_category,
                                                'Wardsci_product_sub_category': product_sub_category,
                                                'Wardsci_product_id': product_id,
                                                'Wardsci_product_name': product_name,
                                                'Wardsci_product_quantity': product_quantity,
                                                'Wardsci_product_price': product_price,
                                                'Wardsci_product_url': product_url,
                                                'Wardsci_image_url': image_url,
                                                'Wardsci_product_desc': description
                                            }
                                            articles_df = pd.DataFrame([dictionary])
                                            articles_df.drop_duplicates(
                                                subset=['Wardsci_product_id', 'Wardsci_product_name'],
                                                keep='first',
                                                inplace=True)
                                            if os.path.isfile(f'{file_name}.csv'):
                                                articles_df.to_csv(f'{file_name}.csv', index=False,
                                                                   header=False, mode='a')
                                            else:
                                                articles_df.to_csv(f'{file_name}.csv', index=False)
                                            write_visited_log(product_id)
        write_visited_log(main_url)