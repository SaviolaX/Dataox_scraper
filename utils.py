from datetime import datetime, timedelta
from selenium.webdriver.common.by import By


def remove_duplicates(all_objects_list: list) -> list:
    """Looping list with objects and remove all duplicates"""
    res_list = []
    for i in range(len(all_objects_list)):
        if all_objects_list[i] not in all_objects_list[i + 1:]:
            res_list.append(all_objects_list[i])
    return res_list


def find_general_info(driver) -> list:
    """Collect information from html page"""
    # list for storing collected data in dicts
    lst = []
    # collecting general info like: title, price, location, date, description
    find_information = driver.find_elements(By.CLASS_NAME, 'info-container')
    # looping through objects on html page and collect needed information
    for item in find_information:
        title = item.find_element(By.CLASS_NAME, 'title').text
        price = fixing_price(item.find_element(By.CLASS_NAME, 'price').text)
        location_and_date = item.find_elements(By.CLASS_NAME, 'location')
        for elem in location_and_date:
            date = fixing_date_format(
                elem.find_element(By.CLASS_NAME, 'date-posted').text)
            if elem.find_element(By.CSS_SELECTOR, 'span').text != date:
                location = fixing_location_format(
                    elem.find_element(By.CSS_SELECTOR, 'span').text)
            else:
                location = 'unknown'
        description = item.find_element(By.CLASS_NAME, 'description').text
        # save information in dict
        inform = {
            'title': title,
            'price': price[1:],
            'currency': price[0],
            'location': location,
            'date': date,
            'description': description
        }
        # append dicts to list
        lst.append(inform)
    # return list of dicts with information
    return lst


def find_bedrooms_info(driver) -> list:
    """Collecting info about bedrooms"""
    # list for storing collected data in dicts
    lst = []
    find_bedrooms = driver.find_elements(By.CLASS_NAME, 'rental-info')
    # looping through objects on html page and collect needed information
    for obj in find_bedrooms:
        beds = obj.find_element(By.CLASS_NAME, 'bedrooms').text
        beds = beds.replace('Beds:', '')
        # save information in dict
        beds_dict = {
            'beds': beds.strip(),
        }
        # append dicts to list
        lst.append(beds_dict)
    # return list of dicts with information
    return lst


def find_image_url(driver) -> list:
    """Collect object's image url"""
    # list for storing collected data in dicts
    lst = []
    # collecting image url
    find_image_url = driver.find_elements(By.CLASS_NAME, 'left-col')
    # looping through objects on html page and collect needed information
    for elem in find_image_url:
        href = elem.find_element(By.CSS_SELECTOR,
                                 'img').get_attribute('data-src')
        if href == None:
            href = 'No photo'
        # save information in dict
        url_dict = {'href': href}
        # append dicts to list
        lst.append(url_dict)
    # return list of dicts with information
    return lst


def fixing_price(price: str) -> str:
    """Fix a price format"""
    if 'Please Contact' in price:
        return '$Please Contact'
    else:
        return price


def fixing_location_format(incorrect_location: str) -> str:
    """Fix a location format 
    removing all unnecessary words in location title"""
    splited_location = incorrect_location.split(' ')
    items_to_remove = ['City', 'of']
    for i in items_to_remove:
        if i in splited_location:
            splited_location.remove(i)
        else:
            pass
    return ''.join(splited_location)


def fixing_date_format(incorrect_date: str) -> str:
    """Fixing a date format to dd-mm-YY"""
    now = datetime.now()
    lst_date = incorrect_date.split(' ')
    if 'minute' in lst_date:
        fixec_time = now - timedelta(minutes=int(lst_date[1]))
        correct_time = fixec_time.strftime("%d-%m-%Y")

    elif 'minutes' in lst_date:
        fixec_time = now - timedelta(minutes=int(lst_date[1]))
        correct_time = fixec_time.strftime("%d-%m-%Y")

    elif 'hours' in lst_date:
        fixec_time = now - timedelta(hours=int(lst_date[1]))
        correct_time = fixec_time.strftime("%d-%m-%Y")

    elif 'Yesterday' in lst_date:
        fixec_time = now - timedelta(hours=24)
        correct_time = fixec_time.strftime("%d-%m-%Y")
    else:
        correct_time = lst_date[0].replace('/', '-')

    return correct_time


def join_dicts_from_lists(lst: list) -> list:
    """Join separeted informations in a single object by indexes 
    and append ones in list"""
    general_info = lst[0]
    bedroom_info = lst[1]
    image_url = lst[2]

    joined_dicts = []

    for i in range(len(general_info)):
        general_info_dict = general_info[i].copy()
        for key, value in bedroom_info[i].items():
            general_info_dict[key] = value
        for key, value in image_url[i].items():
            general_info_dict[key] = value
        joined_dicts.append(general_info_dict)

    return joined_dicts