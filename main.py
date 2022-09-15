from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime

from utils import (join_dicts_from_lists, find_bedrooms_info,
                   find_general_info, find_image_url, remove_duplicates)
from db import (check_whether_postgres_exists, check_whether_table_exists,
                create_table, insert_data_into_database)


def get_data():
    """Main function of collecting, cleaning and saving information to db"""

    start_time = datetime.datetime.now()

    # database and table checking
    if check_whether_postgres_exists() == True:
        print('Connection to db exists')

        if check_whether_table_exists() == True:
            print('Table exists')
        else:
            create_table()
            print('Created table')

        # website url to scrape
        url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'

        # lists with unjoined and uncleaned data
        general_info = []
        bedrooms_info = []
        image_url = []

        # drivers paths depends of browser to use
        # driver = webdriver.Chrome(executable_path="D:\\task\\chromedriver.exe")
        driver = webdriver.Firefox(executable_path="D:\\task\\geckodriver.exe")

        try:
            # open browser
            driver.get(url=url)
            # waiting time for page loading
            time.sleep(3)

            # flag
            next_button_exist = True
            counter = 1
            # start a cycle of visiting pages and collecting information
            # check for button 'next', if button does not exist - collect last page and break
            while next_button_exist:
                try:
                    # waiting time for page loading
                    time.sleep(3)
                    # collect information from page and save to lists
                    list_items_from_page = find_general_info(driver)
                    for item in list_items_from_page:
                        general_info.append(item)
                    list_beds_from_page = find_bedrooms_info(driver)
                    for item in list_beds_from_page:
                        bedrooms_info.append(item)
                    list_image_urls_from_page = find_image_url(driver)
                    for item in list_image_urls_from_page:
                        image_url.append(item)
                    # click on the 'next' button
                    driver.find_element(
                        By.XPATH,
                        '//div[@class="pagination"]//a[@title="Next"]').click(
                        )
                    print(f'[INFO] {counter} pages collected')
                    print(len(bedrooms_info))
                    counter += 1
                except:
                    # waiting time for page loading
                    time.sleep(3)
                    list_items_from_page = find_general_info(driver)
                    for item in list_items_from_page:
                        general_info.append(item)
                    list_beds_from_page = find_bedrooms_info(driver)
                    for item in list_beds_from_page:
                        bedrooms_info.append(item)
                    list_image_urls_from_page = find_image_url(driver)
                    for item in list_image_urls_from_page:
                        image_url.append(item)
                    print(f'Last page {counter} is collected.')
                    counter += 1
                    # change flag that breaks cycle
                    next_button_exist = False
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

        # create a list with joined tables
        all_objects = join_dicts_from_lists(
            [general_info, bedrooms_info, image_url])
        # remove duplicates
        no_duplicates_list = remove_duplicates(all_objects)
        # add cleaned data to db
        insert_data_into_database(no_duplicates_list)
    else:
        print('No connection to db')

    # checking wasted time
    finish_time = datetime.datetime.now()
    total_time = finish_time - start_time
    print('Waisted time: ', total_time)


def main():
    get_data()


if __name__ == '__main__':
    main()