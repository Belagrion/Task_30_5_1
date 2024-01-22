import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_all_pets(web_driver):
    driver = web_driver
    # Проверяем, что мы оказались на главной странице
    assert web_driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Нажимаем на кнопку Мои питомцы
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
    # Проверяем что мы оказались на странице Мои питомцы
    WebDriverWait(web_driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))

    images = web_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = web_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = web_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        image_source = images[i].get_attribute('src')
        name_text = names[i].text
        print(f"Image source: {image_source}")
        print(f"Name text: {name_text}")
        assert image_source != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_pets_30_3_1(web_driver):
    driver = web_driver
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
    WebDriverWait(web_driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))

    images = web_driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    names = web_driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    descriptions = web_driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    age = web_driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(": ")[1]
    pets_count = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    all_pets = web_driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    # Присутствуют все питомцы
    assert int(pets_number) == len(pets_count)

    # Хотя бы у половины питомцев есть фото
    list_images = []
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            list_images.append(images[i])
    assert len(list_images) >= float(pets_number) / 2

    # У всех питомцев есть имя, возраст и порода
    for i in range(len(all_pets)):
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert age[i].text != ''

    # У всех питомцев разные имена
    list_name_my_pets = []
    for i in range(len(names)):
        list_name_my_pets.append(names[i].text)
    list_name_my_pets = set(list_name_my_pets)
    assert len(list_name_my_pets) == int(pets_number)

    # В списке нет повторяющихся питомцев
    list_of_pets = []
    for i in range(len(all_pets)):
        list_data = all_pets[i].text.split("\n")  # Отделяем от данных питомца "х" удаления питомца
        list_of_pets.append(list_data[0])  # Выбираем элемент с данными питомца и добавляем его в список
    list_of_pets = set(list_of_pets)
    assert len(list_of_pets) == len(all_pets)
