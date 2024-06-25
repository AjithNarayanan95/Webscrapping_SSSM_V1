from module_package import *
import math


'''PRODUCT NAME'''


def get_product_name(single_content):
    try:
        product_name = strip_it(single_content.find('a', class_='hide-on-mobile').text.strip())
    except Exception as e:
        print(e)
        product_name = ''
    return product_name


'''PRODUCT URL'''


def get_product_url(single_content):
    url_href = single_content.find('a', class_='hide-on-mobile')['href']
    if 'http' not in str(url_href):
        product_url = f"{base_url}{url_href}"
    else:
        product_url = url_href
    return product_url


'''PRODUCT PRICE'''


def get_product_price(single_content):
    try:
        product_price = strip_it(single_content.find('span', class_='price_data price').text.strip())
    except:
        product_price = ''
    return product_price


'''PRODUCT QUANTITY'''


def get_product_quantity(single_content):
    try:
        product_quantity = single_content.find('div', class_='quantity_section').find('input', class_='quantity_input')[
            'value']
    except:
        product_quantity = '1'
    return product_quantity


'''PRODUCT ID'''


def get_product_id(single_content):
    try:
        product_id = strip_it(single_content.find('div', class_='product_SKU').text.replace('Item #:', ''))
    except:
        product_id = ''
    return product_id


def write_visited_log(url):
    with open(f'Visited_Frey_urls.txt', 'a', encoding='utf-8') as file:
        file.write(f'{url}\n')


def read_log_file():
    if os.path.exists(f'Visited_Frey_urls.txt'):
        with open(f'Visited_Frey_urls.txt', 'r', encoding='utf-8') as read_file:
            return read_file.read().split('\n')
    return []


if __name__ == '__main__':
    timestamp = datetime.now().date().strftime('%Y%m%d')
    file_name = 'Frey_products'
    url = 'https://schoolspecialty.com/'
    base_url = 'https://schoolspecialty.com'
    cookies = {
        '_fbp': 'fb.1.1713871737044.384901192',
        'BVBRANDID': 'acf65f4f-f6af-414f-955b-e4dc3252dd5b',
        '_CEFT': 'Q%3D%3D%3D',
        '_gcl_au': '1.1.1757711006.1713871736.1298973188.1713947476.1713947475',
        '_evga_ccc6': '{%22uuid%22:%221eda7a9bcddf8ad7%22}',
        '_pin_unauth': 'dWlkPU16TXdNemd6T0RjdE9UYzJPUzAwWkdKa0xXSXpPVGN0WW1GalpESTRNak01TXpCaA',
        '_sfid_3117': '{%22anonymousId%22:%221eda7a9bcddf8ad7%22%2C%22consents%22:[]}',
        'WC_PERSISTENT': '0aKvRKFWVhuDaz%2B0L5vgsVauvPnFoS%2Bwv%2FsNCP2bo4s%3D%3B2024-04-24+08%3A37%3A54.992_1713947844880-670443_10801',
        'salsify_session_id': '90ac5e0d-2b84-4966-9c4c-47da3d40b871',
        '_ga': 'GA1.1.1810007287.1713871736',
        '_ga_08EYCBPMK6': 'GS1.2.1713965583.1.0.1713965583.60.0.0',
        '_ga_JEM1SLV40Y': 'GS1.1.1713965583.1.0.1713965588.0.0.0',
        'WC_timeoffset': 'GMT%2B5.5',
        '_ce.irv': 'returning',
        'cebs': '1',
        '_ce.clock_event': '1',
        '_ce.clock_data': '1046%2C115.246.235.83%2C1%2Ca16ddaab909d2cf27fce353f26dd2ff2',
        'CompareItems_10801': '',
        'WC_SESSION_ESTABLISHED': 'true',
        'WC_AUTHENTICATION_-1002': '-1002%2CJdh5JVzqovGDGuZIS9A0yAc11LCiDPi1CWNOoTX%2B9xo%3D',
        'WC_ACTIVEPOINTER': '-1%2C10801',
        'WC_USERACTIVITY_-1002': '-1002%2C10801%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C1383256606%2Cver_null%2CGUn2pcYHiHZUjx65taxOw66BKmhzyWvEunt8Qd9cYYXetkq%2BULIaVlvkvARbkK88e2c3UGZZG%2BNj35hnvHHPDZp%2F%2BAKKA%2FTvKn%2FLFHWUcJ7DMX0qljuJq%2FGOeR8Z%2Fl2J8%2BqBYyvdBfh2OGjaZcP0CG3iRJ1J1A6ttRnqbipr1gXlsrW4zIElsVElNOcWq5fMBF0ynJyvvOT2CUf9lntYctPWU17dvLJxLNi46nce%2FG1Ep15iYak95Jl7KKJQKi2d',
        'WC_GENERIC_ACTIVITYDATA': '[2922735289%3Atrue%3Afalse%3A0%3AKNVtMbUkaeORV70%2FN6THB%2FaB2EBTeRCriff3hedtVDw%3D][com.ibm.commerce.context.entitlement.EntitlementContext|4000000000000000006%264000000000000000006%26null%26-2000%26null%26null%26null][com.ssi.commerce.context.baseimpl.SSIBusinessContext|null%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26null%26null%26null%26null%26false%26false%26false%26null%26false%26false%26null%26false%26null%26true%26true%26null%26null%26null%26null][com.ibm.commerce.context.audit.AuditContext|1713947844880-670443][com.ibm.commerce.context.globalization.GlobalizationContext|-1%26USD%26-1%26USD][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.catalog.businesscontext.CatalogContext|10101%26null%26false%26false%26false][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.ExternalCartContext|null][CTXSETNAME|Store][com.ibm.commerce.context.base.BaseContext|10801%26-1002%26-1002%26-1][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null]',
        'BVImplecomm': '19403_1_0',
        'analyticsPreCategoryAttributes': '""',
        'priceMode': '1',
        'searchTermHistory': '%7Chttps%3A%2F%2Fschoolspecialty.com%2Ffurniture%2Fperforming-arts%2Fstage-dolly-1296560%7CNPS%20Stage%20Dolly%2C%2014%20ga%20Tubular%20Steel%2C%204%20Wheel',
        'BVBRANDSID': '4eb5d105-0483-4884-acb2-da04f5f4e9d3',
        'AKA_A2': 'A',
        'analyticsSearchTerm': '[Ljava.lang.String',
        '_uetsid': 'bf12b8a005f611efa31ca5ded7993656|11o8j2z|2|flc|0|1580',
        'cebsp_': '32',
        '_uetvid': 'ac2d1700016411efaf702f1556e701e5|jxsgbp|1714393795327|14|1|bat.bing.com/p/insights/c/x',
        'JSESSIONID': '0000zkGI_tWt_wpDNqn_j86667L:-1',
        '_ce.s': 'v~eacec7d9f59071ae59ad0092bbdc7f18ec3c6618~lcw~1714393855782~lva~1714374280055~vpv~6~v11.fhb~1714025543230~v11.lhb~1714053534151~v11.cs~35468~v11.s~abf3e530-0621-11ef-b8b1-bbde91b4e845~v11.sla~1714393856447~gtrk.la~lvkxu56g~v11.send~1714393855518~lcw~1714393856447',
        'RT': '"z=1&dm=www.schoolspecialty.com&si=4a20830d-a932-460b-858a-16ab7d0e80ef&ss=lvkx5mqq&sl=5&tt=3wu&obo=4&rl=1"',
        'analyticsFacetAttributes': '',
        '_ga_0YC9X40B5X': 'GS1.1.1713871736.20.1.1714393857.59.0.0',
    }
    post_header = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': '_fbp=fb.1.1713871737044.384901192; BVBRANDID=acf65f4f-f6af-414f-955b-e4dc3252dd5b; _CEFT=Q%3D%3D%3D; _gcl_au=1.1.1757711006.1713871736.1298973188.1713947476.1713947475; _evga_ccc6={%22uuid%22:%221eda7a9bcddf8ad7%22}; _pin_unauth=dWlkPU16TXdNemd6T0RjdE9UYzJPUzAwWkdKa0xXSXpPVGN0WW1GalpESTRNak01TXpCaA; _sfid_3117={%22anonymousId%22:%221eda7a9bcddf8ad7%22%2C%22consents%22:[]}; WC_PERSISTENT=0aKvRKFWVhuDaz%2B0L5vgsVauvPnFoS%2Bwv%2FsNCP2bo4s%3D%3B2024-04-24+08%3A37%3A54.992_1713947844880-670443_10801; salsify_session_id=90ac5e0d-2b84-4966-9c4c-47da3d40b871; _ga=GA1.1.1810007287.1713871736; _ga_08EYCBPMK6=GS1.2.1713965583.1.0.1713965583.60.0.0; _ga_JEM1SLV40Y=GS1.1.1713965583.1.0.1713965588.0.0.0; WC_timeoffset=GMT%2B5.5; _ce.irv=returning; cebs=1; _ce.clock_event=1; _ce.clock_data=1046%2C115.246.235.83%2C1%2Ca16ddaab909d2cf27fce353f26dd2ff2; CompareItems_10801=; WC_SESSION_ESTABLISHED=true; WC_AUTHENTICATION_-1002=-1002%2CJdh5JVzqovGDGuZIS9A0yAc11LCiDPi1CWNOoTX%2B9xo%3D; WC_ACTIVEPOINTER=-1%2C10801; WC_USERACTIVITY_-1002=-1002%2C10801%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C1383256606%2Cver_null%2CGUn2pcYHiHZUjx65taxOw66BKmhzyWvEunt8Qd9cYYXetkq%2BULIaVlvkvARbkK88e2c3UGZZG%2BNj35hnvHHPDZp%2F%2BAKKA%2FTvKn%2FLFHWUcJ7DMX0qljuJq%2FGOeR8Z%2Fl2J8%2BqBYyvdBfh2OGjaZcP0CG3iRJ1J1A6ttRnqbipr1gXlsrW4zIElsVElNOcWq5fMBF0ynJyvvOT2CUf9lntYctPWU17dvLJxLNi46nce%2FG1Ep15iYak95Jl7KKJQKi2d; WC_GENERIC_ACTIVITYDATA=[2922735289%3Atrue%3Afalse%3A0%3AKNVtMbUkaeORV70%2FN6THB%2FaB2EBTeRCriff3hedtVDw%3D][com.ibm.commerce.context.entitlement.EntitlementContext|4000000000000000006%264000000000000000006%26null%26-2000%26null%26null%26null][com.ssi.commerce.context.baseimpl.SSIBusinessContext|null%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26null%26null%26null%26null%26false%26false%26false%26null%26false%26false%26null%26false%26null%26true%26true%26null%26null%26null%26null][com.ibm.commerce.context.audit.AuditContext|1713947844880-670443][com.ibm.commerce.context.globalization.GlobalizationContext|-1%26USD%26-1%26USD][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.catalog.businesscontext.CatalogContext|10101%26null%26false%26false%26false][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.ExternalCartContext|null][CTXSETNAME|Store][com.ibm.commerce.context.base.BaseContext|10801%26-1002%26-1002%26-1][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null]; BVImplecomm=19403_1_0; analyticsPreCategoryAttributes=""; priceMode=1; searchTermHistory=%7Chttps%3A%2F%2Fschoolspecialty.com%2Ffurniture%2Fperforming-arts%2Fstage-dolly-1296560%7CNPS%20Stage%20Dolly%2C%2014%20ga%20Tubular%20Steel%2C%204%20Wheel; BVBRANDSID=4eb5d105-0483-4884-acb2-da04f5f4e9d3; AKA_A2=A; analyticsSearchTerm=[Ljava.lang.String; _uetsid=bf12b8a005f611efa31ca5ded7993656|11o8j2z|2|flc|0|1580; cebsp_=32; _uetvid=ac2d1700016411efaf702f1556e701e5|jxsgbp|1714393795327|14|1|bat.bing.com/p/insights/c/x; JSESSIONID=0000zkGI_tWt_wpDNqn_j86667L:-1; _ce.s=v~eacec7d9f59071ae59ad0092bbdc7f18ec3c6618~lcw~1714393855782~lva~1714374280055~vpv~6~v11.fhb~1714025543230~v11.lhb~1714053534151~v11.cs~35468~v11.s~abf3e530-0621-11ef-b8b1-bbde91b4e845~v11.sla~1714393856447~gtrk.la~lvkxu56g~v11.send~1714393855518~lcw~1714393856447; RT="z=1&dm=www.schoolspecialty.com&si=4a20830d-a932-460b-858a-16ab7d0e80ef&ss=lvkx5mqq&sl=5&tt=3wu&obo=4&rl=1"; analyticsFacetAttributes=; _ga_0YC9X40B5X=GS1.1.1713871736.20.1.1714393857.59.0.0',
        'origin': 'https://www.schoolspecialty.com',
        'priority': 'u=1, i',
        'referer': 'https://www.schoolspecialty.com/furniture/learning-environment-decor',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    headers = {
        'authority': 'select.schoolspecialty.com',
        'method': 'GET',
        'path': '/',
        'scheme': 'https',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        # 'Cookie': '_ga=GA1.1.1810007287.1713871736; _evga_3e99={%22uuid%22:%22832c6b72e6778da9%22}; salsify_session_id=26df4396-d7af-4cc9-9a65-2bbe1c4a1305; _fbp=fb.1.1713871737044.384901192; BVBRANDID=acf65f4f-f6af-414f-955b-e4dc3252dd5b; _ce.clock_event=1; _pin_unauth=dWlkPU16TXdNemd6T0RjdE9UYzJPUzAwWkdKa0xXSXpPVGN0WW1GalpESTRNak01TXpCaA; _ce.clock_data=689%2C115.246.235.83%2C1%2Ca16ddaab909d2cf27fce353f26dd2ff2; _CEFT=Q%3D%3D%3D; _sfid_da9d={%22anonymousId%22:%22832c6b72e6778da9%22%2C%22consents%22:[]}; WC_PERSISTENT=NwrUxliVjOARhO%2BlAcC2iTS1WrmpoBrKRq%2BBQy%2BMiAc%3D%3B2024-04-23+11%3A56%3A46.595_1713873406596-566962_0; _gcl_au=1.1.1757711006.1713871736.2032095064.1713873963.1713873963; RT="z=1&dm=select.schoolspecialty.com&si=979c9bca-4a22-4eaf-af05-150fc649fcd7&ss=lvdgv1by&sl=0&tt=0"; WC_timeoffset=GMT%2B5.5; _ce.irv=returning; cebs=1; CompareItems_11301=; WC_SESSION_ESTABLISHED=true; WC_AUTHENTICATION_-1002=-1002%2CJdh5JVzqovGDGuZIS9A0yAc11LCiDPi1CWNOoTX%2B9xo%3D; WC_ACTIVEPOINTER=-1%2C11301; WC_USERACTIVITY_-1002=-1002%2C11301%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C1383256606%2Cver_null%2CuHNl8CoRwv8Smcse1uoy6oivfLLfjw%2BKvnFjRp1Ih8qpWHvg4ge5k%2Fb8BR0jYMHJErTXE%2BDi1NjDok1heNuJVx4%2F%2FT4uh59MXbUk%2FFO3EgwagcOE7iPeMWQv0Vf4sawba6x6Wqa86Ng2BwY9ExQYylwFlft1gihYgJfSHEs%2Fua2vN91pLdPhOLzGDP89AoFSG2ixq9X6pzxKUn%2Bw2ZzuoVTPhj08bW9DkhsKYl1JBT4fmR8dvhkROn6W%2FW%2B9u7OE; WC_GENERIC_ACTIVITYDATA=[2906860453%3Atrue%3Afalse%3A0%3AryTYitf5v78vbvk0ynX1X0oMa%2Fef7HYh94YTVoBSE0k%3D][com.ibm.commerce.context.entitlement.EntitlementContext|4000000000000000504%264000000000000000504%26null%26-2000%26null%26null%26null][com.ssi.commerce.context.baseimpl.SSIBusinessContext|null%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26false%26null%26null%26null%26null%26false%26false%26false%26null%26false%26false%26null%26false%26null%26true%26true%26null%26null%26null%26null][com.ibm.commerce.context.audit.AuditContext|null][com.ibm.commerce.context.globalization.GlobalizationContext|-1%26USD%26-1%26USD][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.catalog.businesscontext.CatalogContext|10151%26null%26false%26false%26false][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.ExternalCartContext|null][CTXSETNAME|Store][com.ibm.commerce.context.base.BaseContext|11301%26-1002%26-1002%26-1][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null]; priceMode=1; analyticsPreCategoryAttributes=""; analyticsSearchTerm=[Ljava.lang.String; AKA_A2=A; BVBRANDSID=c5f4b07c-c183-46db-80c0-2a85d4fea47f; BVImplecomm=19403_1_0; analyticsFacetAttributes=""; _ga_0YC9X40B5X=GS1.1.1713871736.3.1.1713943297.59.0.0; _uetsid=ac2ce880016411ef9d136bce95964d11|ba4zm0|2|fl7|0|1574; cebsp_=8; _uetvid=ac2d1700016411efaf702f1556e701e5|iwutho|1713943298172|8|1|bat.bing.com/p/insights/c/b; JSESSIONID=0000lIoEKwFosp633hQN8nXLeGT:-1; _ce.s=v~eacec7d9f59071ae59ad0092bbdc7f18ec3c6618~lcw~1713943422227~lva~1713942086423~vpv~1~v11.fhb~1713942086444~v11.lhb~1713943417786~v11.cs~35468~v11.s~77ca8650-0208-11ef-b1f3-e9b72652907d~v11.sla~1713943422226~gtrk.la~lvdhnrkn~v11.send~1713943422920~lcw~1713943422921',
        'Priority': 'u=0, i',
        'Referer': 'https://select.schoolspecialty.com/shop-our-products',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    soup = get_soup_verify(url, headers)
    all_datas = soup.find_all('ul', class_='subcategoryList subcategoryList-level3')
    for main_product in all_datas:
        '''PRODUCT CATEGORY'''
        product_category = main_product.find('li').extract().text.strip()
        sub_product = main_product.find_all('li', class_='')
        for products in sub_product:
            product_sub_category = products.a.text.strip()
            main_url = f"{base_url}{products.a['href']}"
            if 'shop-by-learning-environment/' in str(products):
                main_url = f"{base_url}{products.a['href']}"
                if main_url in read_log_file():
                    continue
                sub_request = get_soup_verify(main_url, headers)
                if sub_request is None:
                    continue
                for other_content in sub_request.find_all('div', class_='ssi-card-container'):
                    inner_href = other_content.a['href']
                    if 'http' not in str(inner_href):
                        inner_url = f"{base_url}{inner_href}"
                    else:
                        inner_url = inner_href
                    inner_request = get_soup_verify(inner_url, headers)
                    if inner_request is None:
                        continue
                    '''GET PAGINATION'''
                    if inner_request.find('span', class_='product_count_label'):
                        page_id = inner_request.find('meta', attrs={'name': 'pageId'})['content']
                        page_content = strip_it(inner_request.find('span', class_='product_count_label').text).replace(',', '').split('-', 1)[-1].split('of', 1)
                        count = page_content[-1].strip()
                        page_count = page_content[0].strip()
                        total_pages = math.ceil(int(count) / int(page_count))
                        for i in range(0, int(total_pages)):
                            page_nav = int(i) * int(24)
                            params = {
                                'top_category3': '',
                                'top_category2': '',
                                'top_category5': '',
                                'top_category4': '',
                                'advancedSearch': '',
                                'orgId': '-2000',
                                'manufacturer': '',
                                'metaData': '',
                                'enableSKUListView': 'false',
                                'catalogId': '10101',
                                'searchTerm': '',
                                'resultsPerPage': '24',
                                'filterFacet': '',
                                'resultCatEntryType': '',
                                'gridPosition': '',
                                'top_category': '3074457345616724775',
                                'categoryFacetHierarchyPath': '',
                                'ajaxStoreImageDir': '/wcsstore/SSIB2BStorefrontAssetStore/',
                                'searchType': '',
                                'filterTerm': '',
                                'searchTermScope': '',
                                'storeId': '10801',
                                'ddkey': 'ProductListingView_6_3074457345618259675_3074457345618288753',
                                'sType': 'SimpleSearch',
                                'emsName': 'Widget_CatalogEntryList-SSI_3074457345618795066',
                                'disableProductCompare': 'false',
                                'langId': '-1',
                                'facet': '',
                                'categoryId': f"{page_id}",
                                'parent_category_rn': '3074457345616724775',
                            }
                            payload = {
                                'contentBeginIndex': '0',
                                'productBeginIndex': f"{page_nav}",
                                'beginIndex': f"{page_nav}",
                                'orderBy': '',
                                'facetId': '',
                                'pageView': '',
                                'resultType': 'both',
                                'orderByContent': '',
                                'searchTerm': '',
                                'facet': '',
                                'facetLimit': '',
                                'minPrice': '',
                                'maxPrice': '',
                                'pageSize': '',
                                'loadProductsList': 'true',
                                'storeId': '10801',
                                'catalogId': '10101',
                                'langId': '-1',
                                'homePageURL': '/en/ssistore',
                                'commandContextCurrency': 'USD',
                                'urlPrefixForHTTPS': 'https://www.schoolspecialty.com',
                                'urlPrefixForHTTP': 'http://www.schoolspecialty.com',
                                'wcc_integration_origin': '',
                                'avToken': 'fc358ed3-dee6-40ed-92ba-e8946491838a',
                                'avURL': 'https://api.edq.com/capture/address/v2/search?query=',
                                'avCountryCode': 'usa',
                                'userId': '-1002',
                                'enableSKUListView': 'FALSE',
                                'widgetPrefix': '6_3074457345618288753',
                                'pgl_widgetId': '3074457345618288753',
                                'objectId': '_6_3074457345618259675_3074457345618288753',
                                'requesttype': 'ajax',
                            }
                            post_url = 'https://www.schoolspecialty.com/ProductListingView'
                            response = requests.post(post_url,
                                                     params=params, cookies=cookies, headers=post_header,
                                                     data=payload)
                            page_soup = BeautifulSoup(response.text, 'html.parser')
                            if page_soup is None:
                                continue
                            content_url = page_soup.find_all('div', class_='product product-container')
                            for single_content in content_url:
                                frey_image_url = single_content.find('img')['src']
                                product_name = get_product_name(single_content)
                                product_url = get_product_url(single_content)
                                product_price = get_product_price(single_content)
                                product_quantity = get_product_quantity(single_content)
                                product_id = get_product_id(single_content)
                                print(product_url)
                                if product_id in read_log_file():
                                    continue
                                print('current datetime------>', datetime.now())
                                dictionary = {
                                    'Frey_product_category': product_category,
                                    'Frey_product_sub_category': product_sub_category,
                                    'Frey_product_id': product_id,
                                    'Frey_product_name': product_name,
                                    'Frey_product_quantity': product_quantity,
                                    'Frey_product_price': product_price,
                                    'Frey_product_url': product_url,
                                    'Frey_image_url': frey_image_url
                                }
                                articles_df = pd.DataFrame([dictionary])
                                articles_df.drop_duplicates(subset=['Frey_product_id', 'Frey_product_name'],
                                                            keep='first',
                                                            inplace=True)
                                if os.path.isfile(f"{file_name}.csv"):
                                    articles_df.to_csv(f"{file_name}.csv", index=False, header=False, mode='a')
                                else:
                                    articles_df.to_csv(f"{file_name}.csv", index=False)
                                write_visited_log(product_id)

                    else:
                        content_url = inner_request.find_all('div', class_='product product-container')
                        for single_content in content_url:
                            frey_image_url = single_content.find('img')['src']
                            product_name = get_product_name(single_content)
                            product_url = get_product_url(single_content)
                            product_price = get_product_price(single_content)
                            product_quantity = get_product_quantity(single_content)
                            product_id = get_product_id(single_content)
                            print(product_url)
                            if product_id in read_log_file():
                                continue
                            print('current datetime------>', datetime.now())
                            dictionary = {
                                'Frey_product_category': product_category,
                                'Frey_product_sub_category': product_sub_category,
                                'Frey_product_id': product_id,
                                'Frey_product_name': product_name,
                                'Frey_product_quantity': product_quantity,
                                'Frey_product_price': product_price,
                                'Frey_product_url': product_url,
                                'Frey_image_url': frey_image_url
                            }
                            articles_df = pd.DataFrame([dictionary])
                            articles_df.drop_duplicates(subset=['Frey_product_id', 'Frey_product_name'], keep='first',
                                                        inplace=True)
                            if os.path.isfile(f"{file_name}.csv"):
                                articles_df.to_csv(f'{file_name}.csv', index=False, header=False, mode='a')
                            else:
                                articles_df.to_csv(f'{file_name}.csv', index=False)
                            write_visited_log(product_id)
                write_visited_log(main_url)
            else:
                if 'ideas-resources' not in str(products):
                    main_url = f"{base_url}{products.a['href']}"
                    if main_url in read_log_file():
                        continue
                    inner_request = get_soup_verify(main_url, headers)
                    if inner_request is None:
                        continue
                    page_id = inner_request.find('meta', attrs={'name': 'pageId'})['content']
                    '''GET PAGINATION'''
                    if inner_request.find('span', class_='product_count_label'):
                        page_content = strip_it(inner_request.find('span', class_='product_count_label').text).replace(',', '').split('-', 1)[-1].split('of', 1)
                        count = page_content[-1].strip()
                        page_count = page_content[0].strip()
                        total_pages = math.ceil(int(count) / int(page_count))
                        for i in range(0, int(total_pages)):
                            page_nav = int(i) * int(24)
                            params = {
                                'top_category3': '',
                                'top_category2': '',
                                'top_category5': '',
                                'top_category4': '',
                                'advancedSearch': '',
                                'orgId': '-2000',
                                'manufacturer': '',
                                'metaData': '',
                                'enableSKUListView': 'false',
                                'catalogId': '10101',
                                'searchTerm': '',
                                'resultsPerPage': '24',
                                'filterFacet': '',
                                'resultCatEntryType': '',
                                'gridPosition': '',
                                'top_category': '3074457345616724775',
                                'categoryFacetHierarchyPath': '',
                                'ajaxStoreImageDir': '/wcsstore/SSIB2BStorefrontAssetStore/',
                                'searchType': '',
                                'filterTerm': '',
                                'searchTermScope': '',
                                'storeId': '10801',
                                'ddkey': 'ProductListingView_6_3074457345618259675_3074457345618288753',
                                'sType': 'SimpleSearch',
                                'emsName': 'Widget_CatalogEntryList-SSI_3074457345618795066',
                                'disableProductCompare': 'false',
                                'langId': '-1',
                                'facet': '',
                                'categoryId': f'{page_id}',
                                'parent_category_rn': '3074457345616724775',
                            }
                            payload = {
                                'contentBeginIndex': '0',
                                'productBeginIndex': f'{page_nav}',
                                'beginIndex': f'{page_nav}',
                                'orderBy': '',
                                'facetId': '',
                                'pageView': '',
                                'resultType': 'both',
                                'orderByContent': '',
                                'searchTerm': '',
                                'facet': '',
                                'facetLimit': '',
                                'minPrice': '',
                                'maxPrice': '',
                                'pageSize': '',
                                'loadProductsList': 'true',
                                'storeId': '10801',
                                'catalogId': '10101',
                                'langId': '-1',
                                'homePageURL': '/en/ssistore',
                                'commandContextCurrency': 'USD',
                                'urlPrefixForHTTPS': 'https://www.schoolspecialty.com',
                                'urlPrefixForHTTP': 'http://www.schoolspecialty.com',
                                'wcc_integration_origin': '',
                                'avToken': 'fc358ed3-dee6-40ed-92ba-e8946491838a',
                                'avURL': 'https://api.edq.com/capture/address/v2/search?query=',
                                'avCountryCode': 'usa',
                                'userId': '-1002',
                                'enableSKUListView': 'FALSE',
                                'widgetPrefix': '6_3074457345618288753',
                                'pgl_widgetId': '3074457345618288753',
                                'objectId': '_6_3074457345618259675_3074457345618288753',
                                'requesttype': 'ajax',
                            }
                            response = requests.post('https://www.schoolspecialty.com/ProductListingView',
                                                     params=params, cookies=cookies, headers=post_header,
                                                     data=payload)
                            page_soup = BeautifulSoup(response.text, 'html.parser')
                            if page_soup is None:
                                continue
                            content_url = page_soup.find_all('div', class_='product product-container')
                            for single_content in content_url:
                                frey_image_url = single_content.find('img')['src']
                                product_name = get_product_name(single_content)
                                product_url = get_product_url(single_content)
                                product_price = get_product_price(single_content)
                                product_quantity = get_product_quantity(single_content)
                                product_id = get_product_id(single_content)
                                print(product_url)
                                if product_id in read_log_file():
                                    continue
                                print('current datetime------>', datetime.now())
                                dictionary = {
                                    'Frey_product_category': product_category,
                                    'Frey_product_sub_category': product_sub_category,
                                    'Frey_product_id': product_id,
                                    'Frey_product_name': product_name,
                                    'Frey_product_quantity': product_quantity,
                                    'Frey_product_price': product_price,
                                    'Frey_product_url': product_url,
                                    'Frey_image_url': frey_image_url
                                }
                                articles_df = pd.DataFrame([dictionary])
                                articles_df.drop_duplicates(subset=['Frey_product_id', 'Frey_product_name'],
                                                            keep='first',
                                                            inplace=True)
                                if os.path.isfile(f'{file_name}.csv'):
                                    articles_df.to_csv(f'{file_name}.csv', index=False, header=False, mode='a')
                                else:
                                    articles_df.to_csv(f'{file_name}.csv', index=False)
                                write_visited_log(product_id)
                    else:
                        content_url = inner_request.find_all('div', class_='product product-container')
                        for single_content in content_url:
                            frey_image_url = single_content.find('img')['src']
                            product_name = get_product_name(single_content)
                            product_url = get_product_url(single_content)
                            product_price = get_product_price(single_content)
                            product_quantity = get_product_quantity(single_content)
                            product_id = get_product_id(single_content)
                            print(product_url)
                            if product_id in read_log_file():
                                continue
                            print('current datetime------>', datetime.now())
                            dictionary = {
                                'Frey_product_category': product_category,
                                'Frey_product_sub_category': product_sub_category,
                                'Frey_product_id': product_id,
                                'Frey_product_name': product_name,
                                'Frey_product_quantity': product_quantity,
                                'Frey_product_price': product_price,
                                'Frey_product_url': product_url,
                                'Frey_image_url': frey_image_url
                            }
                            articles_df = pd.DataFrame([dictionary])
                            articles_df.drop_duplicates(subset=['Frey_product_id', 'Frey_product_name'], keep='first',
                                                        inplace=True)
                            if os.path.isfile(f'{file_name}.csv'):
                                articles_df.to_csv(f'{file_name}.csv', index=False, header=False, mode='a')
                            else:
                                articles_df.to_csv(f'{file_name}.csv', index=False)
                            write_visited_log(product_id)
                    write_visited_log(main_url)
