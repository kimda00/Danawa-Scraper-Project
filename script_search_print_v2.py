import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 검색어
search_keyword = "후드티"

# 다나와 검색 결과 URL
base_url = f"https://search.danawa.com/dsearch.php?query={search_keyword}"

# HTTP 요청 보내기
response = requests.get(base_url, headers=headers)
response.raise_for_status()  # 요청 실패 시 예외 발생

# HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 상품명, 가격, 링크, 썸네일 정보 추출
product_elements = soup.select("a.click_log_product_standard_title_")
product_prices = soup.select("a.click_log_product_standard_price_ > strong")
product_images = soup.select("a.thumb_link img")

for product, price_element, img in zip(product_elements, product_prices, product_images):
    product_name = product.text.strip()
    product_price = price_element.text.strip()
    product_link = product['href']

    # 썸네일 URL 추출
    _class = img.get('class')
    if (_class is not None) and ("lazyload" in _class):
        product_thumbnail = img.get('data-src')
    else:
        product_thumbnail = img.get('src')

    print(f"상품명: {product_name}, 가격: {product_price}원, 링크: {product_link}, 썸네일: https:{product_thumbnail}")

    # 상세 페이지 접근
    try:
        detail_response = requests.get(product_link, headers=headers)
        detail_response.raise_for_status()
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

        # 판매 업체 정보 추출
        seller_elements = detail_soup.select("div.box__logo > img")
        price_elements = detail_soup.select("div.sell-price > span.text__num")
        delivery_elements = detail_soup.select("div.box__delivery")

        for seller, price, delivery in zip(seller_elements, price_elements, delivery_elements):
            seller_name = seller.get('alt')
            seller_price = price.text.strip()
            seller_delivery = delivery.text.strip()
            print(f"\t판매 업체: {seller_name}, 가격: {seller_price}원, 배달비: {seller_delivery}")
    except Exception as e:
        print(f"\t판매 업체 정보 추출 중 오류 발생: {e}")
