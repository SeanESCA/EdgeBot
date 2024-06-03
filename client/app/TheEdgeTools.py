import atexit
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from datetimerange import DateTimeRange
import numpy as np
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
import time


homeUrl = 'https://bath10.artifaxagora.com/room-bookings'
bookingUrl = f'{homeUrl}/venue-hire'
historyUrl = f'{homeUrl}/booking-history'

# Dates are in datetime.
# openingHoursList is Mon - Sun.
openingHoursList = [

    DateTimeRange('1900-01-01T09:00:00', '1900-01-01T21:00:00'),
    DateTimeRange('1900-01-01T09:00:00', '1900-01-01T21:00:00'),
    DateTimeRange('1900-01-01T09:00:00', '1900-01-01T21:00:00'),
    DateTimeRange('1900-01-01T09:00:00', '1900-01-01T21:00:00'),
    DateTimeRange('1900-01-01T09:00:00', '1900-01-01T21:00:00'),
    DateTimeRange('1900-01-01T10:00:00', '1900-01-01T20:00:00'),
    DateTimeRange('1900-01-01T10:00:00', '1900-01-01T18:00:00'),

]

# openingHoursList is Mon - Sun.
presetBookingList = [

    DateTimeRange('1900-01-01T09:00:00', '1900-01-01T11:00:00'),
    DateTimeRange('1900-01-01T09:00:00', '1900-01-01T11:00:00'),
    DateTimeRange('1900-01-01T09:00:00', '1900-01-01T11:00:00'),
    DateTimeRange('1900-01-01T09:00:00', '1900-01-01T11:00:00'),
    DateTimeRange('1900-01-01T09:00:00', '1900-01-01T11:00:00'),
    DateTimeRange('1900-01-01T10:00:00', '1900-01-01T12:00:00'),
    DateTimeRange('1900-01-01T10:00:00', '1900-01-01T12:00:00'),

]

# Room Identifiers
roomIDDict = {

    'buchan': 19,
    'room2': 18,
    'room1': 17,
    'choral': 23

}

edgeOptions = Options()
edgeOptions.use_chromium = True
# edgeOptions.add_argument('--headless')
driver = webdriver.Edge(options=edgeOptions)
action = ActionChains(driver)
atexit.register(driver.quit)

def sign_in(username, password):

    if driver.current_url != homeUrl:

        driver.get(homeUrl)
        
    signInElementList = driver.find_elements(By.LINK_TEXT, 'Sign In')

    if signInElementList:
        action.move_to_element(signInElementList[0]).click().perform()

        emailField = driver.find_element(By.CSS_SELECTOR, '#login_form #email')
        emailField.clear()
        emailField.send_keys(f'{username}@bath.ac.uk')

        passwordField = driver.find_element(By.CSS_SELECTOR, '#login_form #password')
        passwordField.clear()
        passwordField.send_keys(password)

        signInButton = driver.find_element(By.CSS_SELECTOR, '#login_form button[type="submit"]')
        action.move_to_element(signInButton).click().perform()

    for i in range(0, 5):

        if driver.find_elements(By.CSS_SELECTOR, 'div.sweet-alert.showSweetAlert.visible'):

            action.move_to_element(driver.find_element(By.CSS_SELECTOR, '.confirm')).click().perform()

            return False

        elif not driver.find_elements(By.LINK_TEXT, 'Sign In'):

            return True

        time.sleep(1)

def get_week_booking_details():

    # Obtains bookings for current user from 'My Bookings' page, which can be unreliable.

    driver.get(historyUrl)

    while driver.find_elements(By.CSS_SELECTOR, '.dataTables_empty'):
        time.sleep(1)

    soup = BeautifulSoup(driver.execute_script('return document.documentElement.innerHTML'), 'html.parser')
    bookingList = soup.select_one('#future tbody').find_all('tr')
    weekDict = {(datetime.fromisoformat(str(date.today())) + timedelta(days=i)): '' for i in range(0, 8)}

    for booking in bookingList:

        bookingData = booking.find_all('td')

        try:

            bookingStatus = bookingData[-2].get_text()

        except IndexError:
            # No bookings found.

            break

        else:

            if bookingStatus == 'Cancelled':

                continue

            bookedDate = datetime.strptime(bookingData[2].get_text(), '%d/%m/%Y')
            weekDict[bookedDate] = f'{bookingData[4].get_text()}, ' \
                                   f'{bookingData[5].get_text().replace(" (The Edge)", "")}'

    return weekDict

def filter_taken_slots(roomStr, dateToBook: date):

    if driver.current_url != homeUrl:

        driver.get(homeUrl)

    # Clear all previous room filters.
    if not driver.find_element(By.CSS_SELECTOR, '#ftal_room').get_attribute('aria-expanded'):
        
        locationFilterExpanderElement = driver.find_element(By.CSS_SELECTOR, 'span[aria-labelledby="ftal_room"]')
        action.move_to_element(locationFilterExpanderElement).click().perform()

    checkedBoxList = driver.find_elements(By.CSS_SELECTOR, f'span[role="checkbox"]:has(+ span[aria-selected="true"])')

    for checkbox in checkedBoxList:
        
        action.move_to_element(checkbox).click().perform()

    # Apply filters.
    checkboxToTick = driver.find_element(
        By.CSS_SELECTOR, 
        f'span[aria-labelledby="ftal_room[{roomIDDict[roomStr]}]"] span[role="checkbox"]'
    )
    action.move_to_element(checkboxToTick).click().perform()

    for dateID in ['#date_from', '#date_to']:

        dateField = driver.find_element(By.CSS_SELECTOR, dateID)
        dateField.clear()
        dateField.send_keys(dateToBook.strftime('%d/%m/%Y'))
        
    # Check that schedule has been rendered
    noContentElement = driver.find_element(By.CSS_SELECTOR, '.sorry_no_content_text')
    
    while all([
        noContentElement.get_attribute('style') == 'display: none;',
        driver.find_elements(By.CSS_SELECTOR, '.jscroll > *') == []
    ]):
        
        time.sleep(1)

    soup = BeautifulSoup(driver.execute_script('return document.documentElement.innerHTML'), 'html.parser')
    takenSlotList = soup.select('.date_time')

    return [slot.get_text() for slot in takenSlotList], bookedStr

def find_free_slots(takenSlotList, bookingTimeRange: DateTimeRange):

    freeRangeList = [bookingTimeRange]
    
    for slot in takenSlotList:
        
        timeList = slot.split(' – ')
        startTime = datetime.strptime(timeList[0], '%H:%M')
        endTime = datetime.strptime(timeList[1], '%H:%M')
        takenRange = DateTimeRange(startTime, endTime, '%H:%M', '%H:%M')
        newFreeRangeList = []

        for freeRange in freeRangeList:

            newFreeRangeList += freeRange.subtract(takenRange)
        
        freeRangeList = newFreeRangeList

    return freeRangeList

def summarise_week_free_slots():

    weekDict = {(datetime.fromisoformat(str(date.today())) + timedelta(days=i)): {} for i in range(0, 8)}

    for dateToCheck, freeSlotDict in weekDict.items():

        dayInt = dateToCheck.weekday()

        for roomStr in roomIDDict:

            takenSlotList, bookedStr = filter_taken_slots(roomStr, dateToCheck)
            freeSlotDict[roomStr] = find_free_slots(takenSlotList, openingHoursList[dayInt])

    return weekDict

def get_booking_range(weekDict):

    dateBookedList = list(filter(lambda x: x[1] != '', weekDict.items()))
    weekList = list(weekDict.keys())

    if dateBookedList:

        startDate, _ = dateBookedList[-1]

    else:

        # No bookings found.
        startDate = weekList[0]

    startDate += timedelta(days=1)

    return DateTimeRange(startDate, weekList[-1])

def select_single_preset_slot(presetRange:DateTimeRange, freeSlotList, minLength=60):

    possibleSlotList = [presetRange.intersection(slot, timedelta(minutes=minLength)) for slot in freeSlotList]

    for slot in possibleSlotList:

        if all([isinstance(slot, DateTimeRange), slot.get_timedelta_second() >= minLength]):

            suggestedSlot = slot
            suggestedSlot.start_time_format = '%H:%M'
            suggestedSlot.end_time_format = '%H:%M'

    return suggestedSlot

def select_preset_slot_week(weekFreeSlotDict, minLength=60):

    toBookWeekDict = {}

    for dateToBook, bookedDetailStr in get_week_booking_details().items():

        if bookedDetailStr:

            continue

        dayInt = dateToBook.weekday()
        freeSlotForDayDict = weekFreeSlotDict[dateToBook]

        for roomStr in roomIDDict:

            suggestedSlot = select_single_preset_slot(
                presetBookingList[dayInt],
                freeSlotForDayDict[roomStr],
                minLength
            )

            if suggestedSlot:

                toBookWeekDict[dateToBook] = {'roomStr': roomStr, 'slotRange': suggestedSlot}

    return toBookWeekDict

def book_room(roomStr, bookingDate:datetime, bookingRange: DateTimeRange):

    driver.get(bookingUrl)
    nextButtonList = driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"]')

    # Choose Rehearsal(Solo).
    driver.find_element(By.CSS_SELECTOR, f'input[value="30"]').click()
    driver.find_element(By.LINK_TEXT, 'Next').click()
    time.sleep(1)

    # Choose room.
    driver.find_element(By.CSS_SELECTOR, f'span[aria-labelledby="ftal_room[{roomIDDict["buchan"]}]"] > span[role="checkbox"]').click()
    nextButtonList[2].click()
    time.sleep(1)

    # Enter date.
    dateField = driver.find_element(By.CSS_SELECTOR, 'input[id="date_from_once"]')
    dateField.clear()
    dateField.send_keys(bookingDate.strftime('%d/%m/%Y'))

    # Enter start time
    startTimeField = driver.find_element(By.CSS_SELECTOR, 'input[id="between_which_times_from"]')
    startTimeField.clear()
    bookingRange.start_time_format = '%H:%M'
    startTimeField.send_keys(bookingRange.get_start_time_str())

    # Enter end time.
    endTimeField = driver.find_element(By.CSS_SELECTOR, 'input[id="between_which_times_to"]')
    endTimeField.clear()
    bookingRange.end_time_format = '%H:%M'
    endTimeField.send_keys(bookingRange.get_end_time_str())
    dateField.send_keys(Keys.ENTER)
    nextButtonList[3].click()
    time.sleep(10)

    # Confirm booking.
    driver.find_element(By.CSS_SELECTOR, 'input[name="arrangement_description"]').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input[id="terms_checkbox_user"]').click()

    # Final submit button only appears on last page.
    driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"]')[-1].click()
    time.sleep(3)

def book_for_week(weekFreeSlotDict, minLength=60):

    toBookWeekDict = select_preset_slot_week(weekFreeSlotDict, minLength)

    for dateToBook, bookingDetailDict in toBookWeekDict.items():

        roomStr, bookingRange = bookingDetailDict.values()

        try:

            status = book_room(roomStr, dateToBook, bookingRange)

        except:

            bookingDetailDict['status'] = 'fail'

        else:

            bookingDetailDict['status'] = 'pass'

    return toBookWeekDict
