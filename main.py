import os.path as path
import os
import json
from textwrap import fill
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as firefox_service
from webdriver_manager.firefox import GeckoDriverManager

USERNAME = "lars@atilf.no"
PASSWORD = "XRKxmtKhecuyGu6"

class Cv:
    """A class for accessing CV in JSON format."""
   
    
    def import_cv(self, path_string="cv.json"):
        """
        Imports CV in JSON format
            
            Parameters:
                path_string (string): path to cv file, defaults to ./cv.json
            Returns:
                cv_dict (dict): cv as a python dict
        """
        exists = path.exists(path_string)
        if not exists:
            raise Exception("path does not exist")
        with open(path_string, "r") as file:
            cv_json = file.read()
            cv_dict = json.loads(cv_json)
            return cv_dict

def log_in(driver):
    username = driver.find_element(by=By.ID, value="username")
    username.send_keys(USERNAME)
    password = driver.find_element(by=By.ID, value="password")
    password.send_keys(PASSWORD)
    submit_button = driver.find_element(by=By.ID, value="login-btn")
    submit_button.click()


def fill_form(cv_dict, driver: webdriver):
    #class=   icon-pencil, icon-plus
    # fields: educations, work-history
    #kanskje loop gjennom class: section
    sections = driver.find_elements(By.CLASS_NAME, 'card-container')
    try:
        for element in sections:
            #attempt to match input field to json-field
            #create another dictionary with names of fields used? 
            # manually map them to fields in JSON?
            element_title = element.find_element(By.XPATH, "./div[@class='header']").text
            print(element_title)
            #content = cv_dict[element_title]
    except KeyError as e:
        print(e)
    except Exception as e:
        print(e)

def main():
    new_cv = Cv()
    cv_dict = new_cv.import_cv()
    driver = webdriver.Firefox(service=firefox_service(executable_path=GeckoDriverManager().install()))
    try:    
        driver.get("https://www.academicwork.no/Account/LoginAuth?url=https%3A%2F%2Fwww.academicwork.no%2F")
        driver.implicitly_wait(3)
        log_in(driver)
        driver.implicitly_wait(3)
        fill_form(cv_dict, driver)
    finally:
        driver.quit()

main()