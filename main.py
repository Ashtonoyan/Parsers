import requests
from bs4 import BeautifulSoup
import pandas as pd


# Функция для парсинга одной страницы и извлечения данных
def parse_page(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        link_texts = soup.find_all('a', class_='products__items')
        product_texts = soup.find_all('div', class_='products__text')
        #print(link_texts)

        extracted_data = []
        #print(link_texts)

        for product_text in (link_texts):

                link = ""
                title = ""
                main_description = ""
                additional_description = ""


                try:

                    if product_text:
                        link = product_text['href']
                        #print(link)
                        #title = product_text.find('h3', class_='products__text__header').text.strip()
                        #print(title)

                       # description_div = product_text.find('div', class_='products__text__description')

                        #main_description = description_div.find('div',
                                                             #   class_='products__text__description__main').text.strip()
                        #(main_description)
                        #additional_description = description_div.find('div',
                                                                   #   class_='products__text__description__additional').text.strip()
                    else:
                        link=None
                        #print(link)

                except AttributeError:
                    pass



                extracted_data.append({
                    'Link': link,
                   # 'Название': title,
                   # 'Основное описание': main_description,
                   # 'Дополнительное описание': additional_description

                })

        return extracted_data

# Функция для парсинга и сохранения данных
def scrape_and_save_data(base_url,  start_page, end_page):
    all_data = []

    for page_num in range(start_page, end_page + 1):
        page_url = f"{base_url}&page={page_num}"
        page_data = parse_page(page_url)
        if not page_data:
            break
        all_data.extend(page_data)

    # Создаем DataFrame для данных и сохраняем его в CSV
    df_data = pd.DataFrame(all_data)
    df_data.to_csv('data_chrysler_1_100.csv', index=False, encoding='utf-8-sig') #
    print(f"Данные сохранены в 'data_chrysler_1_100.csv'.")

# базовый URL сайта и количество страниц, которые хотим спарсить
base_url = "https://rrr.lt/ru/poisk?man_id=36&mfi=36;&prs=1"

start_page_to_scrape = 2 #начинаем с 1000 страницы
end_page_to_scrape = 100 #парсим до 1500 страницы

# Вызываем функцию для парсинга и сохранения данных
scrape_and_save_data(base_url, start_page_to_scrape, end_page_to_scrape)

print(f"Данные с {start_page_to_scrape} по {end_page_to_scrape} страницы сохранены в 'data_chrysler_1_100.csv'.")
