
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
      # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield pytest.driver

    pytest.driver.quit()
@pytest.fixture()
def test_show_my_pets():
    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.ID, 'email')))
    pytest.driver.find_element(By.ID, 'email').send_keys('rama@mail.ru')
    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.ID, 'pass')))
    pytest.driver.find_element(By.ID, 'pass').send_keys('Qwert')
    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Установка явного ожидания
    element = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.XPATH, ' //a[@class="nav-link"]')))

    pytest.driver.find_element(By.XPATH, ' //a[@class="nav-link"]').click()
    # Проверяем, что мы оказались на странице списка моих питомцев
    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Kukish"

    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_pets_num(testing):
    pytest.driver = testing
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('rama@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('Wert')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Проверяем, работает ли кнопка "Мои питомцы" c явным ожиданием

def my_pets_clickable(by, desc):
    wait = WebDriverWait(webdriver, 10)
    by = by.upper()
    if by == 'XPATH':
        wait.until(ec.element_to_be_clickable((By.XPATH, desc))).click()
        if by == 'ID':
            wait.until(ec.element_to_be_clickable((By.ID, desc))).click()
            if by == 'LINK_TEXT':
                wait.until(ec.element_to_be_clickable((By.LINK_TEXT, desc))).click()
                my_pets_clickable('link_text', 'Moи питомцы')

    # Нажимаем на кнопку "Мои питомцы"
    pytest.driver.find_element(By.XPATH, ' //a[@class="nav-link"]').click()

    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Kukish"

    images = WebDriverWait(pytest.driver, 10).until(
         ec.presence_of_all_elements_located(By.CSS_SELECTOR, ".card-deck .card-img-top"))
    names = WebDriverWait(pytest.driver, 10).until(
         ec.presence_of_all_elements_located(By.CSS_SELECTOR, ".card-deck .card-title"))
    descriptions = WebDriverWait(pytest.driver, 10).until(
         ec.presence_of_all_elements_located(By.CSS_SELECTOR, ".card-deck .card-text"))

    my_pets_num = int(
        pytest.driver.find_element(By.CSS_SELECTOR, 'html>body>div>div>div').text.split("\n")[1].split(":")[1].strip())
    print(my_pets_num)
    my_pets_num = int(
        pytest.driver.find_element(By.CSS_SELECTOR, 'html>body>div>div>div').text.split("\n")[1].split(":")[1].strip())
    pytest.driver.implicitly_wait(10)
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    pet_names = []
    for pet in all_pets:
        pet_names.append(pet.text.split(' ')[0])
        print(pet_names)
        print(len(pet_names))
        assert len(pet_names) == my_pets_num


def test_uniq_pets(testing):
    pytest.driver.implicitly_wait(10)
    pytest.driver = testing
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('rama@mail.ru')
    pytest.driver.find_element(By.ID, 'pass').send_keys('Qwert')

    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на странице списка моих питомцев
    pytest.driver.find_element(By.XPATH, ' //a[@class="nav-link"]').click()

    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Kukish"
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@class="marked-element"]')
    all_pets_data = [pet.text for pet in all_pets]
    uniq_pets = set(all_pets_data)
    if len(all_pets_data) == len(uniq_pets):
        print("Все питомцы имеют одинаковые имена")

    else:
        print("В списке есть питомцы c повторяющимися данными:")
        assert len(all_pets_data) == len(uniq_pets)
    not_uniq_pets = set([pet.text for pet in all_pets if all_pets_data.count(pet.text) > 1])
    print(f'Повторяющиеся питомцы {not_uniq_pets}')

