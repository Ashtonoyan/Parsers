import requests
from bs4 import BeautifulSoup
import pandas as pd


data = pd.read_csv('data_chrysler_1_100.csv') #файл для чтения


prices = []
delivery_prices = []
total_prices=[]
count=1
count_data=1
price_count=1

for i, link in enumerate(data['Link']):

   try:
    # Отправить запрос на сайт
    response = requests.get(link)
    if response.status_code != 200:
        print(f"Не удалось получить данные с ссылки: {link}, статус код: {response.status_code}")
        data.loc[i, 'Price'] = None
        data.loc[i, 'Delivery Price'] = None
        data.loc[i, 'Total Price'] = None
        data.loc[i, 'Заголовок'] = None
        data.loc[i, 'Код'] = None
        data.loc[i, 'Title'] = None
        data.loc[i, 'Series'] = series
        data.loc[i, 'Годы производства'] = None
        data.loc[i, 'Год'] = None
        data.loc[i, 'Положение рулевого колеса'] = None
        data.loc[i, 'Ведущие колеса'] = None
        data.loc[i, 'Тип топлива'] = None
        data.loc[i, 'Объем двигателя, cm3'] = None
        data.loc[i, 'Мощность двигателя, kW'] = None
        data.loc[i, 'Код двигателя'] = None
        data.loc[i, 'Title only'] = None
        data.loc[i, 'Series only'] = None
        data.loc[i, 'Product cat'] = None
        data.loc[i, 'Product cat2'] = None
        data.loc[i, 'Product cat3'] = None
    soup = BeautifulSoup(response.content, "html.parser")

    price_element = soup.find('span', class_='product_price_block_amount').text.strip()
    data.loc[i, 'Price'] = price_element

    price = float(price_element.replace(',', '.').replace('€', ''))
    # delivery_price_element = soup.find('span', class_='product_price_block__delivery__price').text.strip()
    delivery_price_element = soup.find('span', class_='product_price_block__delivery__price')
    if delivery_price_element:
        delivery_price_element = delivery_price_element.text.strip()
        data.loc[i, 'Delivery Price'] = delivery_price_element
        cleaned_string = delivery_price_element.strip().replace('+', '').strip()
        delivery = float(cleaned_string.replace(',', '.').replace('€', ''))
        if delivery < 7:
            total_price = (price * 1.2) + (delivery * 3)
        else:
            total_price = (price * 1.2) + (delivery * 1.5)
        rounded_total_price = round(total_price, 2)
        data.loc[i, 'Total Price'] = rounded_total_price
        #print("price_count", price_count)
        #price_count += 1
    else:
        total_price = price * 1.3
        rounded_total_price = round(total_price, 2)
        #print(f"Не удалось найти цену доставки для ссылки: {link}")
        data.loc[i, 'Delivery Price'] = None
        data.loc[i, 'Total Price'] = rounded_total_price
        # print(data.loc[i, 'Total Price'])
        # print("count", count)
        # count += 1

    soup = BeautifulSoup(response.content, "html.parser")
    title_element = soup.find('h1', class_='text-uppercase part__title part__title--desktop')
    title_zag = title_element.text.strip() if title_element else "Н/Д"


    code_element = soup.find(name="a", attrs={"data-testid": "part-code"})
    code_avto = code_element.text if code_element else "Н/Д"

    product_column = soup.find("div", class_="product_column product_column--right product-column-right-pos-js")
    #print(product_column)
    if product_column:
        product_desc = product_column.find("div", class_="product_desc skip-delivery-price")
        #print(product_desc)
        if product_desc:
            product_desc_blocks = product_desc.find_all("div", class_="product_desc__block")

            # Проверяем, что есть хотя бы два элемента
            if len(product_desc_blocks) >= 2:
                # Выбираем второй элемент
                second_product_desc_block = product_desc_blocks[1]

                product_desc_panels = second_product_desc_block.find("div", class_="product_desc__panels open clearfix product-desc-panels-js")

                if product_desc_panels:
                    product_details = product_desc_panels.find("dl", class_="product_details")

                    if product_details:
                        first_product_details_term = product_details.find("dd", class_="product_details__term")


                        if first_product_details_term:
                            link_element = first_product_details_term.find("a")
                            if link_element:
                                title1 = link_element.get("title")


                        second_product_details_term = first_product_details_term.find_next("dd",
                                                                                           class_="product_details__term")
                        third_product_details_term = second_product_details_term.find_next("dd",
                                                                                           class_="product_details__term")
                        #print(third_product_details_term)
                        four_3_product_details_term = third_product_details_term.find_next("dd",
                                                                                           class_="product_details__term")
                        #print(four_3_product_details_term)
                        # Если такой элемент найден, извлекаем ссылку и серию
                        four_4_product_details_term = four_3_product_details_term.find_next("dd",
                                                                                           class_="product_details__term")
                        #print(four_4_product_details_term)
                        five_product_details_term = four_4_product_details_term.find_next("dd",
                                                                                           class_="product_details__term")
                        #print(five_product_details_term)
                        six_product_details_term=five_product_details_term.find_next("dd",
                                                                                           class_="product_details__term")
                        #print(six_product_details_term)
                        seven_product_details_term = six_product_details_term.find_next("dd",
                                                                                       class_="product_details__term")
                        #print(seven_product_details_term)
                        eight_product_details_term = seven_product_details_term.find_next("dd",
                                                                                       class_="product_details__term")
                        #print(eight_product_details_term)
                        nine_product_details_term = eight_product_details_term.find_next("dd",
                                                                                       class_="product_details__term")
                        #print(nine_product_details_term)
                        ten_product_details_term= nine_product_details_term.find_next("dd",
                                                                                       class_="product_details__term")
                        #print(ten_product_details_term)
                        #eleven_product_details_term=ten_product_details_term.find_next("dd",
                                                                                       #class_="product_details__term")
                        eleven_product_details_term = ten_product_details_term.find_next("dd",
                                                                                         class_="product_details__term")

                        #print(eleven_product_details_term)

                        if second_product_details_term:
                            link_element = second_product_details_term.find("a")
                            if link_element:
                                series = link_element.get("title")




                        if four_3_product_details_term:
                            years_of_production = four_3_product_details_term.text.strip()
                        if four_4_product_details_term:
                            year=four_4_product_details_term.text.strip()
                        if six_product_details_term:
                            st_position=six_product_details_term.text.strip()
                        if seven_product_details_term:
                            driving_wheels=seven_product_details_term.text.strip()
                        if eight_product_details_term:
                            fuel=eight_product_details_term.text.strip()
                        if nine_product_details_term:
                            volume=nine_product_details_term.text.strip()
                        if ten_product_details_term:
                            power=ten_product_details_term.text.strip()
                        if eleven_product_details_term:
                            class_attribute = eleven_product_details_term.get("class")

                            # Проверяем, что значение атрибута class не равно "product_details__term product_help__time"
                            if eleven_product_details_term and not all(
                                    cls in eleven_product_details_term.get("class", []) for cls in
                                    ['product_details__term', 'product_help__time']):
                                box_codes = eleven_product_details_term.text.strip()
                                #print(class_attribute)
                                #print(box_codes)
                            else:
                                #print("Else", class_attribute)
                                box_codes=None
                                #print('Else', eleven_product_details_term.text.strip())


                        data.loc[i, 'Заголовок'] = title_zag
                        data.loc[i, 'Код'] = code_avto
                        data.loc[i, 'Title'] = title1
                        data.loc[i, 'Series'] = series
                        data.loc[i, 'Годы производства'] = years_of_production
                        data.loc[i, 'Год'] = year
                        data.loc[i, 'Положение рулевого колеса'] = st_position
                        data.loc[i, 'Ведущие колеса'] = driving_wheels
                        data.loc[i, 'Тип топлива'] = fuel
                        data.loc[i, 'Объем двигателя, cm3'] = volume
                        data.loc[i, 'Мощность двигателя, kW'] = power
                        data.loc[i, 'Код двигателя'] = box_codes
                        data.loc[i, 'Title only'] = title1
                        data.loc[i, 'Series only'] = series
                        #print(count)
                        #count+=1
                        #print("count_data", count_data)
                        count_data += 1


    soup = BeautifulSoup(response.content, "html.parser")

    first_product_cat = soup.find("li", class_="breadcrumb__items")
    second_product_cat = first_product_cat.find_next("li", class_="breadcrumb__items")
    third_product_cat = second_product_cat.find_next("li", class_="breadcrumb__items")
    four_product_cat = third_product_cat.find_next("li", class_="breadcrumb__items")
    if four_product_cat:
        cat_element = four_product_cat.find("a")
        if cat_element:
          product_cat = cat_element.get("title")

    five_product_cat = four_product_cat.find_next("li", class_="breadcrumb__items")
    if five_product_cat:
        cat_element1 = five_product_cat.find("a")
        if cat_element1:
            product_cat1 = cat_element1.get("title")
            #print(product_cat1)
    six_product_cat = five_product_cat.find_next("li", class_="breadcrumb__items")
    if six_product_cat:
        cat_element2 = six_product_cat.find("a")
        if cat_element2:
            product_cat2 = cat_element2.get("title")
            #print(product_cat2)
    if (product_cat == text):
        data.loc[i, 'Product cat'] = None
    if (product_cat1 == text):
        data.loc[i, 'Product cat2'] = None
    if (product_cat2 == text):
        data.loc[i, 'Product cat3'] = None
    data.loc[i, 'Product cat'] = product_cat
    data.loc[i, 'Product cat2'] = product_cat1
    data.loc[i, 'Product cat3'] = product_cat2


   except Exception as e:
        print(f"Ошибка при обработке ссылки: {link}")
        print(f"Ошибка: {str(e)}")
        data.loc[i, 'Price'] = None
        data.loc[i, 'Delivery Price'] = None
        data.loc[i, 'Total Price'] = None
        data.loc[i, 'Заголовок'] = None
        data.loc[i, 'Код'] = None
        data.loc[i, 'Title'] = None
        data.loc[i, 'Series'] = None
        data.loc[i, 'Годы производства'] = None
        data.loc[i, 'Год'] = None
        data.loc[i, 'Положение рулевого колеса'] = None
        data.loc[i, 'Ведущие колеса'] = None
        data.loc[i, 'Тип топлива'] = None
        data.loc[i, 'Объем двигателя, cm3'] = None
        data.loc[i, 'Мощность двигателя, kW'] = None
        data.loc[i, 'Код двигателя'] = None
        data.loc[i, 'Title only'] = None
        data.loc[i, 'Series only'] = None
        data.loc[i, 'Product cat'] = None
        data.loc[i, 'Product cat2'] = None
        data.loc[i, 'Product cat3'] = None
        print("count_data", count_data)
        count_data += 1


"""
for i, link in enumerate(data['Link']):
    try:
        # Отправить запрос на сайт
        response = requests.get(link)
        if response.status_code != 200:
            print(f"Не удалось получить данные с ссылки: {link}, статус код: {response.status_code}")
            data.loc[i, 'Product cat'] = None
        else:
            # Создать объект BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            first_product_cat = soup.find("li", class_="breadcrumb__items")
            second_product_cat = first_product_cat.find_next("li", class_="breadcrumb__items")
            third_product_cat = second_product_cat.find_next("li", class_="breadcrumb__items")
            four_product_cat = third_product_cat.find_next("li", class_="breadcrumb__items")
            if four_product_cat:
                 cat_element = four_product_cat.find("a")
                 if cat_element:
                        product_cat = cat_element.get("title")
            data.loc[i, 'Product cat'] = product_cat
            print(count)
            count += 1
    except Exception as e:
            data.loc[i, 'Product cat'] = None
"""

start_id = 1

# Создание столбца "ID" с начальным значением
data["ID"] =  [f"chrysler{i}" for i in range(start_id, start_id + len(data))] #меняем название марки

# Сохранение изменений в файле]

data.to_csv('data_chrysler_1_100.csv', index=False, encoding='utf-8-sig')


