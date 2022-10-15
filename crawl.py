import csv
import re
import requests

url1 = 'shopee.vn/-MÁY-ĐẸP-99-Điện-thoại-Samsung-j2-prime-g532-(1-5-8GB)-Máy-cũ-Hàng-chính-hãng-i.13480277.12363907844'
url2 = 'shopee.vn/Chuột-ko-dây-Bluetooth-2.4Ghz-tự-sạc-pin-cao-cấp-2-trong-1-chống-ồn-dùng-cho-ĐT-Máy-Tính-Laptop-laptop-táo-i.52528876.13856069722'
url3 = 'shopee.vn/-Mã-ELSS8-giảm-8-tối-đa-600K-Điện-Thoại-Samsung-Galaxy-S20-FE-(8GB-256GB)-Hàng-Chính-Hãng-i.65589552.9980498489'
url4 = 'shopee.vn/Điện-Thoại-Xiaomi-Redmi-10C-4-128GB-Pin-5000mAh-Snapdragon-680-i.340431675.16830053495'
url5 = 'shopee.vn/Chuột-không-dây-Logitech-M220-Silent-(không-tiếng-ồn)-tặng-bàn-di-chuột-BH-đổi-mới-trong-12-tháng-i.3558160.10510218531'
url6 = 'shopee.vn/Thẻ-Nhớ-Micro-SD-Tốc-Độ-100MB-S-Ultra-A1-Class-10-i.279844729.14488343611'
all_url = [url1,url2,url3,url4,url5,url6]

with open('dataset.csv', 'w', encoding='utf-8-sig') as f:
    headers = ['sentiment', 'comment']
    writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)
    writer.writeheader()
    for url in all_url:
        r = re.search(r"i\.(\d+)\.(\d+)", url)
        shop_id, item_id = r[1], r[2]
        ratings_url = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit=20&offset={offset}&shopid={shop_id}&type=0"
        offset = 0
        while True:
            data = requests.get(ratings_url.format(shop_id=shop_id, item_id=item_id, offset=offset)).json()
            i = 1
            try:
                for i, rating in enumerate(data["data"]["ratings"],1):
                    if rating["comment"] != '':
                        writer.writerow({headers[0]:rating["rating_star"], headers[1]:rating["comment"].replace('\n', ' ')})
            except:
                break
            if i % 20:
                break
            offset += 20