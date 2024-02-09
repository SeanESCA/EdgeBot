from datetime import date, datetime, timedelta
from datetimerange import DateTimeRange
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from user_input import NO_BOOKING
from webdriver_manager.chrome import ChromeDriverManager


HOME_URL = 'https://bath10.artifaxagora.com/room-bookings'
BOOKING_URL = f'{HOME_URL}/venue-hire'
HISTORY_URL = f'{HOME_URL}/booking-history'
ERROR_CLASS_NAME = 'sweet-alert'
MIN_SLOT_LENGTH = timedelta(minutes=30)
MAX_SLOT_LENGTH = timedelta(hours=2)
ROOM_DICT = {
    'room 1': 17,
    'room 2': 18,
    'buchan': 19,
    'choral': 23
}


chrome_options=webdriver.ChromeOptions()
driver=webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
driver.implicitly_wait(3)

def sign_in(email:str, password:str):
    
    driver.get(HOME_URL)
    
    # Click on login button.
    driver.find_element(By.LINK_TEXT, 'Sign In').click()
    
    # Clear email field and enter email.
    email_field = driver.find_element(By.CSS_SELECTOR, '#login_form #email')
    email_field.clear()
    email_field.send_keys(email)
    
    # Clear password field and enter password.
    password_field = driver.find_element(By.CSS_SELECTOR, '#login_form #password')
    password_field.clear()
    password_field.send_keys(password)
    
    # Click submit button.
    driver.find_element(By.CSS_SELECTOR, '#login_form button[type="submit"]').click()
    
    # Check if the login failed.
    if driver.find_elements(By.CLASS_NAME, ERROR_CLASS_NAME):
        
        driver.quit()
        raise Exception('Your email or password is incorrect. Please check your details in user_input.py')
    
    else:

        WebDriverWait(driver, 15).until(EC.invisibility_of_element_located((By.ID, 'login_form')))

def get_future_booking_list():
    '''
    Returns a list of future bookings as a 2D array.
    '''
    driver.get(HISTORY_URL)
    
    # Wait until table loads.
    WebDriverWait(driver, 20).until(EC.any_of(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#future tbody > tr[role="row"]')),
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#future tbody'), 'No bookings found')
    ))
    
    # Filter out cancelled bookings.
    status_element_list = driver.find_elements(By.CSS_SELECTOR, '#future td[class^="status"]')
    
    if status_element_list:
        
        status_str_array = np.array([status.text for status in status_element_list])
        index_array = status_str_array == 'Confirmed'

        date_element_list = driver.find_elements(By.CSS_SELECTOR, '#future .sorting_1')
        date_array = np.array([datetime.strptime(date_element.text, '%d/%m/%Y').date() 
                                   for date_element in date_element_list])[index_array]

        time_element_list = driver.find_elements(By.CSS_SELECTOR, '#future .sorting_2')
        slot_array = np.array([timerange_to_datetimerange(time_element.text) 
                                   for time_element in time_element_list])[index_array]

        room_element_list = driver.find_elements(By.CSS_SELECTOR, '#future .sorting_2 + td')
        room_str_array = np.array([room.text for room in room_element_list])[index_array]

        return [date_array, slot_array, room_str_array]
    
    return [[], [], []]    
        
def apply_room_filter(room_key:str):
    
    # Clears all room filters and selects one.
    # Must be in HOME_URL first.
    # Expand the general location list if it is closed.
    if not driver.find_element(By.ID, 'ftal_room').get_attribute('aria-expanded'):
        
        driver.find_element(By.CSS_SELECTOR, 'span[aria-labelledby="ftal_room"]').click()

    # Expand the location list for the Edge if it is closed.
    if not driver.find_element(By.ID, 'ftal_venue[1]').get_attribute('aria-expanded'):

        driver.find_element(By.CSS_SELECTOR, 'span[aria-labelledby="ftal_venue[1]"] > span[role="button"]').click()
        
    # Find all selected location checkboxes.
    checked_location_list = driver.find_elements(
        By.CSS_SELECTOR, 
        f'span[role="checkbox"]:has(+ span[aria-selected="true"])'
    )
    
    # Clear all selected location checkboxes.
    for checkbox in checked_location_list:
        
        checkbox.click()

    # Select desired location.
    driver.find_element(
        By.CSS_SELECTOR, 
        f'span[aria-labelledby="ftal_room[{ROOM_DICT[room_key]}]"] > span[role="checkbox"]'
    ).click()
    
def apply_date_filter(date_to_check:date):
    
    # Must be in HOME_URL first.
    for date_field_id in ['date_from', 'date_to']:

        date_field = driver.find_element(By.ID, date_field_id)
        date_field.clear()
        date_field.send_keys(date_to_check.strftime('%d/%m/%Y'))

def timerange_to_datetimerange(timerange_str): 
    
    time_range = DateTimeRange.from_range_text(
        timerange_str, 
        separator=r' – ',
        start_time_format='%H:%M', 
        end_time_format='%H:%M'
    )
    
    start_datetime = datetime.combine(date.min, time_range.start_datetime.time())
    end_datetime = datetime.combine(date.min, time_range.end_datetime.time())
    
    return DateTimeRange(start_datetime, end_datetime)

def get_taken_slot_list(room_key:str, date_to_book: date):
    
    attempt_int = 0
    
    while attempt_int < 3:
    
        apply_room_filter(room_key)
        apply_date_filter(date_to_book)
        WebDriverWait(driver, 10).until(EC.any_of(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.jscroll > *')),
            EC.visibility_of_element_located((By.CLASS_NAME, 'sorry_no_content_text'))
        ))
    
        # Refreshing the page is the most consistent method to ensure that schedule has correctly rendered.
        driver.refresh()
        taken_room_list = [taken_room.text for taken_room in driver.find_elements(By.CLASS_NAME, 'room')]
        taken_slot_str_list = [taken_time.text for taken_time in driver.find_elements(By.CLASS_NAME, 'date_time')]
        #     booking_title_list = [booking_text.text for booking_text in driver.find_elements(By.CSS_SELECTOR, '.title')]

        for taken_room in taken_room_list:

            if not re.search(room_key, taken_room, re.I):
                
                attempt_int += 1                    
                continue
        
        return [timerange_to_datetimerange(taken_slot_str) for taken_slot_str in taken_slot_str_list]

def get_possible_slot_array(desired_slot, taken_slot_list, min_booking_length: timedelta):
    
    '''
    Returns a list with all the free slots that are at least the minimum booking length
    '''
    possible_slot_array = np.array([desired_slot])

    for taken_slot in taken_slot_list:
        
        possible_slot_array = np.array([
            possible_slot.subtract(taken_slot) for possible_slot in possible_slot_array
        ])
        
        if possible_slot_array.size == 0:
            
            return []
            
        possible_slot_array = np.concatenate(possible_slot_array)
    
    min_timedelta = max(MIN_SLOT_LENGTH, min_booking_length)
    slot_timedelta_array = np.array([slot.timedelta for slot in possible_slot_array])

    return possible_slot_array[slot_timedelta_array >= min_timedelta]

def get_slot_to_book(possible_slot_array, max_booking_length: timedelta):
    
    '''
    Find slots that are at least the maximum booking length and return the earliest slot to book.
    If none are found, return the longest possible slot to book. 
    If the earliest slot is longer than max_duration, the function will return an interval of length
    max_duration with the same start time.
    '''
    
    slot_to_book = NO_BOOKING
    
    if possible_slot_array:
        
        slot_timedelta_array = np.array([slot.timedelta for slot in possible_slot_array])
        max_timedelta = min(
            max_booking_length, 
            max(slot_timedelta_array),
            MAX_SLOT_LENGTH
        )
        filtered_slot_list = possible_slot_array[slot_timedelta_array >= max_timedelta]
    
        if filtered_slot_list:

            slot_to_book = filtered_slot_list[0]

            if slot_to_book.timedelta > max_timedelta:

                slot_to_book = DateTimeRange(
                    slot_to_book.start_datetime, 
                    slot_to_book.start_datetime + max_timedelta
                )

    return slot_to_book
    
def max_datetimerange(datetimerange_list):
    
    '''
    Returns the longest slot from a list of DateTimeRange objects.
    '''
    timedelta_array = np.array([slot.timedelta for slot in datetimerange_list])
    return np.array(datetimerange_list)[timedelta_array == np.max(timedelta_array)][0]

def book_room(room_key, date_to_book:date, slot_to_book: DateTimeRange, booking_description):

    driver.get(BOOKING_URL)
    next_button_list = driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"]')

    # Choose Rehearsal(Solo).
    driver.find_element(By.CSS_SELECTOR, f'input[value="30"]').click()
    driver.find_element(By.LINK_TEXT, 'Next').click()

    # Choose room.
    driver.find_element(By.CSS_SELECTOR, f'span[aria-labelledby="ftal_room[{ROOM_DICT[room_key]}]"] > span[role="checkbox"]').click()
    next_button_list[2].click()

    # Enter date.
    date_field = driver.find_element(By.CSS_SELECTOR, 'input[id="date_from_once"]')
    date_field.clear()
    date_field.send_keys(date_to_book.strftime('%d/%m/%Y'))

    # Enter start time
    start_time_field = driver.find_element(By.CSS_SELECTOR, 'input[id="between_which_times_from"]')
    start_time_field.clear()
    start_time_field.send_keys(slot_to_book.start_datetime.strftime('%H:%M'))

    # Enter end time.
    end_time_field = driver.find_element(By.CSS_SELECTOR, 'input[id="between_which_times_to"]')
    end_time_field.clear()
    end_time_field.send_keys(slot_to_book.end_datetime.strftime('%H:%M'))
    date_field.send_keys(Keys.ENTER)
    next_button_list[3].click() 
    
    # Wait until the site gives an error or the final booking page is displayed.
    WebDriverWait(driver, 20).until(EC.any_of(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="arrangement_description"]')),
        EC.visibility_of_element_located((By.CLASS_NAME, 'sweet-alert'))
    ))
    
    # Check if the site gives an error.
    if driver.find_elements(By.CLASS_NAME, ERROR_CLASS_NAME):
        
        error_str = driver.find_element(By.CSS_SELECTOR, f'.{ERROR_CLASS_NAME} > p').text
        driver.find_element(By.CLASS_NAME, 'confirm').click()
        driver.get(HOME_URL)
        return error_str
           
    driver.find_element(By.CSS_SELECTOR, 'input[name="arrangement_description"]').send_keys(booking_description)
    driver.find_element(By.CSS_SELECTOR, 'input[id="terms_checkbox_user"]').click()

    # Final submit button only appears on last page.
    driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"]')[-1].click()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'confirm')))
    return True