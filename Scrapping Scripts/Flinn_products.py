import logging
from module_package import *


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def write_visited_log(url):
    with open(f'Visited_urls_flinn.txt', 'a', encoding='utf-8') as file:
        file.write(f'{url}\n')


def read_log_file():
    if os.path.exists(f'Visited_urls_flinn.txt'):
        with open(f'Visited_urls_flinn.txt', 'r', encoding='utf-8') as read_file:
            return read_file.read().split('\n')
    return []


def get_main_url(base_url, content):
    if 'http' not in str(content):
        return f'{base_url}{content["href"]}'
    else:
        return content['href']


def scrape_product(product_url, headers):
    response = requests.get(product_url, headers=headers)
    product_request = BeautifulSoup(response.text, 'html.parser')
    if product_request is None:
        logging.error(f"Failed to scrape product page: {product_url}")
        return None
    return product_request


def extract_product_info(single_contents, product_request):
    ids = single_contents['SKUNumbers']
    if ';' not in str(ids):
        product_name = single_contents['Name']
        product_url = f'{base_url}{single_contents["Url"]}'
        product_price = f'${single_contents["PriceMax"]}'
        product_id = ''
        product_quantity = 1
        '''IMAGE CONTENT'''
        try:
            image_link = product_request.find('a', class_='full-size-image')['href']
            flinn_image_url = f'{base_url}{image_link}'
        except:
            flinn_image_url = ''
        try:
            product_id_element = product_request.find('div', styel='display: flex; align-items: center;')
            if product_id_element:
                product_id = strip_it(product_id_element.text.replace('Item #:', '').strip())
            else:
                product_id = str(single_contents['SKUNumbers']).replace("['", '').replace("']", '').strip()
        except:
            pass
        if re.search(r'Pkg. of \d+', str(product_name)):
            product_quantity = re.search(r'Pkg. of \d+', str(product_name)).group().replace('Pkg. of', '').strip()
        if product_id in read_log_file():
            return
        write_visited_log(product_id)
        product_dict = {
            'Flinn_product_category': product_category,
            'Flinn_product_sub_category': product_sub_category,
            'Flinn_product_id': product_id,
            'Flinn_product_name': product_name,
            'Flinn_product_quantity': product_quantity,
            'Flinn_product_price': product_price,
            'Flinn_product_url': product_url,
            'Flinn_image_url': flinn_image_url
        }
        return product_dict


def extract_sub_product_info(product_request, product_url):

    '''IMAGE CONTENT'''
    try:
        image_link = product_request.find('a', class_='full-size-image')['href']
        flinn_image_url = f'{base_url}{image_link}'
    except:
        flinn_image_url = ''
    '''PRODUCT NAME AND PRODUCT ID'''
    try:
        inner_data = product_request.find('div', class_='product-page__info--item list col-xs-8')
        product_id = inner_data.find('span', class_='code').extract().text.replace('(', '').replace(')', '').strip()
        product_names = strip_it(inner_data.text.strip())
        product_name = product_names
        if re.search('Pkg. of \d+', str(product_name)):
            product_quantity = re.search('Pkg. of \d+', str(product_name)).group().replace('Pkg. of', '').strip()
        else:
            product_quantity = 1
    except:
        product_name = ''
        product_id = ''
        product_quantity = ''
    '''PRODUCT PRICE'''
    try:
        if product_request.find('span', class_='product-page__price'):
            product_price = strip_it(product_request.find('span', class_='product-page__price').text.strip())
        elif product_request.find('div', class_='product-page__price'):
            product_data = product_request.find('div', class_='product-page__price')
            if product_data.find('span', class_='product-page__original-price'):
                extract_tag = product_data.find('span', class_='product-page__original-price').extract()
                product_price = strip_it(product_data.text.strip())
            else:
                product_price = strip_it(product_data.text.strip())
        else:
            product_price = ''
    except:
        product_price = ''
    if product_id in read_log_file():
        return
    write_visited_log(product_id)
    product_dict = {
        'Flinn_product_category': product_category,
        'Flinn_product_sub_category': product_sub_category,
        'Flinn_product_id': product_id,
        'Flinn_product_name': product_name,
        'Flinn_product_quantity': product_quantity,
        'Flinn_product_price': product_price,
        'Flinn_product_url': product_url,
        'Flinn_image_url': flinn_image_url
    }
    return product_dict


def sub_category(inner_req, headers, base_url):
    content_id_element = inner_req.find('div', id='FilteredListList')
    if not content_id_element:
        logging.error(f"Failed to find content ID for category: {category_url}")
        return
    content_id = content_id_element.get('data-category')
    page_nav_number = inner_req.find('h3', class_='hidden-lg hidden-xs b-filtered-list__nav-heading__current-category').text.split('(', 1)[-1].replace(')', '').strip()
    page_data = math.ceil(int(page_nav_number) / 6)
    for i in range(page_data):
        json_url = f'{base_url}/api/Search/{content_id}/{i}?type=All&srt=d'
        json_soup = get_json_response(json_url, headers)
        content_json = json_soup.get('Items', [])
        for single_contents in content_json:
            product_url = f'{base_url}{single_contents["Url"]}'
            product_request = scrape_product(product_url, headers)
            if not product_request:
                logging.error(f"Failed to scrape product page: {product_url}")
                continue
            if not product_request.find('ul', class_='product-page__info--options list'):
                product_dict = extract_product_info(single_contents, product_request)
                save_product_data(product_dict)
            else:
                sub_product = product_request.find('ul', class_='product-page__info--options list').find_all('li')
                for single_product in sub_product:
                    product_url = f"{base_url}{single_product.find('a', class_='option-link col-xs-12 col-sm-6')['href']}"
                    product_request = get_soup(product_url, headers)
                    if product_request is None:
                        continue
                    product_dict = extract_sub_product_info(product_request, product_url)
                    save_product_data(product_dict)


def scrape_category(category_url, headers, base_url):
    category_req = get_soup(category_url, headers)
    if not category_req:
        logging.error(f"Failed to get soup for category: {category_url}")
        return
    content_id_element = category_req.find('div', id='FilteredListList')
    if not content_id_element:
        logging.error(f"Failed to find content ID for category: {category_url}")
        return
    content_id = content_id_element.get('data-category')
    page_nav_number = category_req.find('h3', class_='hidden-lg hidden-xs b-filtered-list__nav-heading__current-category').text.split('(', 1)[-1].replace(')', '').strip()
    page_data = math.ceil(int(page_nav_number) / 6)
    for i in range(page_data):
        json_url = f"{base_url}/api/Search/{content_id}/{i}?type=All&srt=d"
        json_soup = get_json_response(json_url, headers)
        content_json = json_soup.get('Items', [])
        for single_contents in content_json:
            product_url = f'{base_url}{single_contents["Url"]}'
            product_request = scrape_product(product_url, headers)
            if not product_request:
                logging.error(f"Failed to scrape product page: {product_url}")
                continue
            if not product_request.find('ul', class_='product-page__info--options list'):
                product_dict = extract_product_info(single_contents, product_request)
                save_product_data(product_dict)
            else:
                sub_product = product_request.find('ul', class_='product-page__info--options list').find_all('li')
                for single_product in sub_product:
                    product_url = f"{base_url}{single_product.find('a', class_='option-link col-xs-12 col-sm-6')['href']}"
                    product_request = get_soup(product_url, headers)
                    if product_request is None:
                        continue
                    product_dict = extract_sub_product_info(product_request, product_url)
                    save_product_data(product_dict)


def save_product_data(product_dict):
    if product_dict is not None:
        articles_df = pd.DataFrame([product_dict])
        articles_df.drop_duplicates(subset=['Flinn_product_id', 'Flinn_product_name'], keep='first', inplace=True)
        if os.path.isfile(f'{file_name}.csv'):
            articles_df.to_csv(f'{file_name}.csv', index=False, header=False, mode='a')
        else:
            articles_df.to_csv(f'{file_name}.csv', index=False)
        logging.info(f"Saved product: {product_dict.get('Flinn_product_name', 'N/A')}")


if __name__ == '__main__':
    file_name = os.path.basename(__file__).rstrip('.py')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    url = 'https://www.flinnsci.com/'
    base_url = 'https://www.flinnsci.com'
    soup = get_soup(url, headers)
    data = soup.find_all('li', class_='b-main-nav-inner-content__hidden-content__links-list-item_first-level')
    for single_data in data:
        content = single_data.find('a')
        product_category = content.text.strip()
        main_url = get_main_url(base_url, content)
        logging.info(f'main_url------------->{main_url}')
        if main_url in read_log_file():
            continue
        inner_req = get_soup(main_url, headers)
        if inner_req.find('a', class_='b-categories__category__link'):
            inner_category = inner_req.find_all('a', class_='b-categories__category__link')
            for category in inner_category:
                category_url = f'{base_url}{category["href"]}'
                if category.find('h3', class_='b-categories__category__name'):
                    product_sub_category = category.find('h3', class_='b-categories__category__name').text.strip()
                else:
                    product_sub_category = 'NA'
                scrape_category(category_url, headers, base_url)
        elif inner_req.find('div', id='FilteredListList'):
            product_sub_category = 'NA'
            sub_category(inner_req, headers, base_url)
        else:
            product_sub_category = 'NA'
            scrape_category(main_url, headers, base_url)
        write_visited_log(main_url)
