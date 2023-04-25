import time
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_web():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://127.0.0.1:8000/view-projects/")
    print("Title: ", driver.title)


def test_login():
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.get("http://127.0.0.1:8000/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("000002")

    # Find the password input element and enter a value
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("pass")

    # Submit the login form
    password_input.send_keys(Keys.RETURN)

    # Wait for the page to load
    time.sleep(2)

    # Check if the login was successful
    assert "Project Management System" in driver.title

    # Close the browser
    driver.close()



def test_view_Projects_employee():
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.get("http://127.0.0.1:8000/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("000002")

    # Find the password input element and enter a value
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("pass")
    password_input.send_keys(Keys.RETURN)

    # Verify that project dashboard is displayed
    project_id = driver.find_element(By.XPATH,'/html/body/main/div/div/div[1]/h3').text
    assert project_id == "Your Projects"

    # Close the browser
    driver.close()




def test_view_Resources_employee():
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.get("http://127.0.0.1:8000/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("000002")

    # Find the password input element and enter a value
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("pass")
    password_input.send_keys(Keys.RETURN)

    driver.get("http://127.0.0.1:8000/resources/")

    # Verify that resource dashboard is displayed
    project_id = driver.find_element(By.XPATH,'/html/body/main/div/div/div[1]/h3').text
    assert project_id == "Resources"

    # Close the browser
    driver.close()
