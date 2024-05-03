import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

input_csv_file = 'data_chrysler_1_100.csv' #файл для чтения
output_csv_file = 'data_chrysler_1_100_with_images.csv' #сохранения для чтения

df = pd.read_csv(input_csv_file)



df['Image_URL'] = ''
df['Image_URL2'] = ''
df['Image_URL3'] = ''


# Функция для извлечения URL изображений из HTML-кода страницы
def extract_image_url(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_urls = []
        img_div = soup.find('div', class_='product_gallery_for__panel carousel__slide')
        if img_div:
            img_url = img_div.get('data-src')
            img_urls.append(img_url)
        else:
            img_urls.append('')
        img_div2 = img_div.find_next('div', class_='product_gallery_for__panel carousel__slide')
        if img_div2:
            img_url2 = img_div2.get('data-src')
            img_urls.append(img_url2)
        else:
            img_urls.append('')
        img_div3 = img_div2.find_next('div', class_='product_gallery_for__panel carousel__slide')
        if img_div3:
            img_url3 = img_div3.get('data-src')
            img_urls.append(img_url3)
        else:
            img_urls.append('')
        return img_urls[:3]

    except Exception as e:
        return ['', '', '']







for index, row in df.iterrows():
    link = row['Link']
    image_url = extract_image_url(link)
    df.at[index, 'Image_URL'] = image_url[0]
    df.at[index, 'Image_URL2'] = image_url[1]
    df.at[index, 'Image_URL3'] = image_url[2]


df.to_csv(output_csv_file, index=False, encoding='utf-8-sig')

print(f"Изображения успешно добавлены в файл {output_csv_file}")
