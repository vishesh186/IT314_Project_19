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
    driver.get("https://project-management-system.up.railway.app/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("E000001")

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
    driver.get("https://project-management-system.up.railway.app/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("E000002")

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
    driver.get("https://project-management-system.up.railway.app/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("E000002")

    # Find the password input element and enter a value
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("pass")
    password_input.send_keys(Keys.RETURN)

    driver.get("https://project-management-system.up.railway.app/resources/")

    # Verify that resource dashboard is displayed
    project_id = driver.find_element(By.XPATH,'/html/body/main/div/div/div[1]/h3').text
    assert project_id == "Resources"

    # Close the browser
    driver.close()



def test_view_Teams_Manager():
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.get("https://project-management-system.up.railway.app/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("PM00001")

    # Find the password input element and enter a value
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("pass")
    password_input.send_keys(Keys.RETURN)

    driver.get("https://project-management-system.up.railway.app/manage-teams/")

    # Verify that team dashboard is displayed
    project_id = driver.find_element(By.XPATH,'/html/body/main/div/div/div[1]/h3').text
    assert project_id == "Team Management Dashboard"

    # Close the browser
    driver.close()



def test_view_Resource_booking():
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.get("https://project-management-system.up.railway.app/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("PM00001")

    # Find the password input element and enter a value
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("pass")
    password_input.send_keys(Keys.RETURN)

    driver.get("https://project-management-system.up.railway.app/resources/")

    # Verify that resource booking request dashboard is displayed
    project_id = driver.find_element(By.XPATH,'/html/body/main/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/a')
    project_id.click()

    txt = driver.find_element(By.XPATH,"/html/body/main/div/div/div[1]/h3").text
    assert txt == "Resource Booking Request"

    # Close the browser
    driver.close()



def test_view_avilable_resources():
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.get("https://project-management-system.up.railway.app/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("E000004")

    # Find the password input element and enter a value
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("pass")
    password_input.send_keys(Keys.RETURN)

    driver.get("https://project-management-system.up.railway.app/resources/")

    manage = driver.find_element(By.XPATH,'/html/body/header/nav[1]/div/div/a[3]')
    manage.click()

    resources = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/ul/li[1]/a')
    resources.click()

    avilable = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/ul/li[1]/ul/li[1]/button')
    avilable.click()

    # Verify that available resources are displayed
    txt = driver.find_element(By.XPATH,"/html/body/main/div/div/div[1]/h3").text
    assert txt == 'Resources'

    # Close the browser
    driver.close()



def test_view_task_manager():
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.get("https://project-management-system.up.railway.app/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("PM00002")

    # Find the password input element and enter a value
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("pass")
    password_input.send_keys(Keys.RETURN)


    manage = driver.find_element(By.XPATH,'/html/body/header/nav[1]/div/div/a[1]')
    manage.click()

    project = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div/div[1]/div[1]/div/div[2]/a')
    project.click()

    mt = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/ul/li[1]/a')
    mt.click()

    bt = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/ul/li[1]/ul/li[1]/button')
    bt.click()

    view = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/a')
    view.click()

    # Verify that task view for manager is displayed
    txt = driver.find_element(By.XPATH,"/html/body/main/div/div/div[1]/h3").text
    assert txt == "TS200001 : Develop App"

    # Close the browser
    driver.close()

    
    
def test_create_new_team():
    driver = webdriver.Chrome()

    driver.maximize_window()
    driver.get("https://project-management-system.up.railway.app/login/")

    # Find the username input element and enter a value
    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("E000010")

    # Find the password input element and enter a value
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("pass")
    password_input.send_keys(Keys.RETURN)

    driver.get("https://project-management-system.up.railway.app/manage-teams/")

    create = driver.find_element(By.XPATH,'/html/body/main/div/div/div[2]/ul/li[2]/button')
    create.click()

    name = driver.find_element(By.NAME, 'name')
    name.clear()
    name.send_keys("test_team")

    manager = driver.find_element(By.NAME, 'manager')
    manager.click()

    man = driver.find_element(By.XPATH,"/html/body/main/div/div/div[2]/div/div[2]/div/div[2]/div/div/form/div[1]/div[2]/select/option[4]")
    man.click()

    description = driver.find_element(By.NAME,"description")
    description.clear()
    description.send_keys("testing_team_creation")

    submit = driver.find_element(By.XPATH, '/html/body/main/div/div/div[2]/div/div[2]/div/div[2]/div/div/form/button')
    submit.click()

    validate = driver.find_element(By.XPATH, '/html/body/div').text
    assert validate == 'New Team Created Successfully.'

    # Close the browser
    driver.close()
