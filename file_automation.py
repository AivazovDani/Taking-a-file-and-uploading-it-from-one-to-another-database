import os
import tempfile
from pyairtable import Api
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time

UPLOAD_URL = 'https://i.textyou.online/campaign/login/signin'
AIRTABLE_API_KEY = "pat5CgRLCXHna9XPq.9ea1c27ae2822b58ab92bb30dfcc34f19b12c5d35475e762bbac1cc2c94aadb4"
AIRTABLE_BASE_ID = "appP0F84sv2q9AR5P"
AIRTABLE_TABLE_NAME = "Uploads"


def fetch_and_upload():
    # Start Selenium and Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Loads stuff for airtable
    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

    driver.get(UPLOAD_URL)
    time.sleep(2)

    # selenium automaton
    username = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))        
    username.send_keys("capello@clicklab.ai")
    time.sleep(0.5)

    password = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]'))
    )

    password.send_keys("CLtyo1!")
    time.sleep(0.5)

    sign_in = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
    )

    sign_in.click()
    time.sleep(0.5)

    # Get all records with that date if the checkbox is not checked
    records = table.all(formula="NOT({Processed})")

    for record in records:

        # Get everything from the attachments field
        attachments = record["fields"]["Attachments"]

        # In case there are multiple
        for file in attachments:
            try:
                # Extracts the download URL and the original filename from Airtable
                url = file["url"]
                filename = file["filename"]

                # Download the file
                response = requests.get(url)

                # save it temporaly in the laptop
                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as tmp:
                    tmp.write(response.content)
                    tmp_path = tmp.name
                    file_name = os.path.splitext(filename)[0]


                phone_book = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/campaign/phone-book']"))
                )

                phone_book.click()
                time.sleep(0.5)


                new_phone_book = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='New book']"))
                )

                new_phone_book.click()
                time.sleep(0.5)

                dropdown_open = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "react-select-2-input"))
                )

                dropdown_open.click()
                time.sleep(0.5)

                dropdown_open.send_keys("United States")
                time.sleep(0.5)


                option_us = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'react-select__option') and text()='United States']"))
                )

                option_us.click()
                time.sleep(0.5)

                file_name_input = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='phone_book_name']"))
                )

                file_name_input.send_keys(file_name)
                time.sleep(0.5)

                save_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))
                )

                save_button.click()
                time.sleep(0.5)

                import_btn = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//button[text()='Import phones']"))
                )

                import_btn.click()
                time.sleep(0.5)

                excel_csv_tab = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Excel, CSV')]"))
                )

                excel_csv_tab.click()
                time.sleep(0.5)

                file_input = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
                )

                file_input.send_keys(tmp_path)
                time.sleep(2)

                next_btn = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))
                )

                next_btn.click()
                time.sleep(0.5)

                next_btn = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))
                )

                next_btn.click()
                time.sleep(0.5)


                finish_btn = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Finish')]"))
                )

                finish_btn.click()
                time.sleep(2)


                # we remove the tmp file from our computer
                os.remove(tmp_path)


                # check the checkbox
                table.update(record["id"], {"Processed": True})

                # go back to the dashboard
                driver.get("https://i.textyou.online/campaign/phone-book")
                time.sleep(1)
            
            except Exception as e:
                print(f"Failed on file {filename}: {e}")
                driver.get("https://i.textyou.online/campaign/phone-book")
                time.sleep(1)
                continue  

if __name__ == "__main__":
    fetch_and_upload()