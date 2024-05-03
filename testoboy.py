import requests
from bs4 import BeautifulSoup
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot
import os
import schedule
import time



bot = Bot(token='токен_нашего_бота')

def read_sku_from_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    skus = []
    for row in sheet.iter_rows(values_only=True):
        sku = row[0]  # Допустим, что SKU номера хранятся в столбце 0
        skus.append(sku)
    return skus

#так как на странице товара не хранятся все отзывы, нам нужно перейти на страницу отзывов. Поэтому я использовал webdriver
#и кликаем на кнопку отзывы, чтобы случился переход на страницу всех отзывов. Дальше ожидаем, пока загрузятся все отзывы и после начинаем парсить
#так как мы должны были перейти на новую страницу, я решил парсить название товара и рейтинг с новой страницы.
def get_product_info(sku):
    url = f"https://www.wildberries.ru/catalog/{sku}/detail.aspx"


    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # Вот здесь и находим кнопку, чтобы перейти к странице всех отзывов
        see_all_reviews_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-base.comments__btn-all"))
        )
        see_all_reviews_button.click()

        # Ждем, пока загрузятся все отзывы
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-card-customer-review"))
        )

        page_source = driver.page_source
    finally:
        driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    product_info = soup.find('div', class_='product-line__main')

    # Здесь хранится название бренда
    brand = product_info.find('b').text.strip()

    # Здесь хранится название товара
    product_name = product_info.find('a', class_='product-line__name hide-mobile').text.strip()

    # Соединяем вместе
    product_title = f"{brand} {product_name}"
    rating = soup.find('div', class_='product-line__desc hide-mobile').find('span',
                                                                            class_='address-rate-mini address-rate-mini--sm').text.strip()
    # Рейтинг хранится в классе выше, мы извлекаем числовую часть
    rating = float(rating)

    # Находим все отзывы
    reviews = soup.find_all('li', class_='comments__item feedback j-feedback-slide')


    negative_reviews = []
    for review in reviews:
        # получаем рейтинга товара от пользователя
        review_rating_class = review.find('span', class_='feedback__rating').attrs['class'][-1]
        # извлекаем числовую часть и
        review_rating = int(review_rating_class.replace('star', ''))
        #здесь ищем только отрицательные товары. В задании было написано от 1 до 4 звезд, но я прочитал отзывы
        #и 4 и 3 звезды не являются отрицательными
        if review_rating in (1, 2):
            feedback_info = review.find_parent('div', class_='feedback__info')
            # Переходим к родительскому элементу с классом 'feedback__top-wrap'
            feedback_top_wrap = feedback_info.find_parent('div', class_='feedback__top-wrap')
            # Находим дочерний элемент с id 'pCEJP95wdPqZXHqKgmkV'
            feedback_content = feedback_top_wrap.find('div', id='pCEJP95wdPqZXHqKgmkV')
            # Извлекаем текст отзыва
            review_text = feedback_content.find('p', class_='feedback__text').text.strip()


            negative_reviews.append((review_text, review_rating))

    return product_title, rating, negative_reviews


def monitor_reviews(skus):
    # Так как мы будем запускать периодически, важно чтобы в телеграм группу отправлялись только свежие отзывы, чтобы старые не повторялись
    #поэтому создал текстовой файл, в которым будем записывать все отзывы, а потом проверять на свежесть
    if os.path.exists('sent_reviews.txt'):
        with open('sent_reviews.txt', 'r') as file:
            sent_reviews = set(file.read().splitlines())
    else:
        sent_reviews = set()

    for sku in skus:
        product_title, product_rating, negative_reviews = get_product_info(sku)
        if product_title and product_rating:
            for review_text, review_rating in negative_reviews:
                review_info = f"{product_title} - {review_text}"

                # Здесь происходит проверка на свежесть отзыва
                if review_info not in sent_reviews:
                    message = f"Товар: {product_title}, Рейтинг товара: {product_rating}\n"
                    message += f"Негативный отзыв: {review_text}, Рейтинг отзыва: {review_rating}"

                    # Отправка в телеграмм
                    bot.send_message(chat_id='YOUR_GROUP_CHAT_ID', text=message)

                    #Обновляем файл
                    with open('sent_reviews.txt', 'a') as file:
                        file.write(review_info + '\n')
        else:
            print(f"Ошибка при получении информации о товаре с SKU: {sku}")
#создал функцию, которая будет запускаться два раза в день
def run_monitoring():
    excel_file = "products.xlsx"
    skus = read_sku_from_excel(excel_file)
    monitor_reviews(skus)

# Запускаем наш код 2 раза в день, сперва в 8 утра, а после в 8 вечера
schedule.every().day.at("08:00").do(run_monitoring)
schedule.every().day.at("20:00").do(run_monitoring)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
