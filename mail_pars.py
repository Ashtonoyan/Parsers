import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
login_url = ''
data = {
    'email': 'email',
    'password': 'password',
    'sign': 'true'
}



login_response = requests.post(login_url, data=data)

if login_response.status_code == 200:
    print('Успешно вошли на сайт')
    target_url = ''
    response = requests.get(target_url)

    # Проверка успешности запроса
    if response.status_code == 200:
        page_content = response.content
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        # Перейти на страницу для парсинга
        target_url = ''
        driver.get(target_url)


        wait = WebDriverWait(driver, 30)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                    'td.table-row-left.js-conversion-stats-field[data-field-id="partner"]')))
        requested_url = response.url
        print("Адрес сайта, который был запрошен:", requested_url)



        partner_elements = driver.find_elements(By.CSS_SELECTOR,
                                                'td.table-row-left.js-conversion-stats-field[data-field-id="partner"]')


        for element in partner_elements:
            partner_id = element.find_element(By.TAG_NAME, 'a').get_attribute('title')
            email = element.find_element(By.TAG_NAME, 'a').text

            print("Идентификатор партнера:", partner_id)
            print("Адрес электронной почты:", email)




        page_content = driver.page_source

        print("ok")
        soup = BeautifulSoup(page_content, 'html.parser')
        partner_elements = soup.find_all('td', {'class': 'table-row-left js-conversion-stats-field',
                                                'data-field-id': 'partner'})
        print(partner_elements)

        for element in partner_elements:
            links = element.find_all('a', {'class': 'underline'})


            for link in links:
                href = link.get('href')
                if '/partners/edit/' in href:
                    email = link.text.strip()
                    print('Название почты:', email)
                    break

        driver.quit()




    else:
        print('Не удалось получить доступ к целевой странице')
else:
    print(f'Не удалось войти на сайт. HTTP-статус: {login_response.status_code}')
    print('Содержимое ответа:')
    print(login_response.text)
