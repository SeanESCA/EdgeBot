import atexit
from datetime import time
from the_edge_bath import *
from user_input import *
from user_input_func import *


atexit.register(lambda: driver.quit())
sign_in(EMAIL, PASSWORD)
    
preset_date_list, preset_slot_list = filter_user_booking_list(USER_BOOKING_LIST)
future_date_list, _, _ = get_future_booking_list()
date_to_find_array = np.setdiff1d(preset_date_list, future_date_list)

for date_to_book in date_to_find_array:
    
    print(f'Looking for {date_to_book}...')
    driver.get(HOME_URL)
    is_exact_desired_slot_found = False
    slot_to_book_option_list = []
    
    for desired_slot in preset_slot_list[preset_date_list.index(date_to_book)]:
        
        print(f'Looking for {desired_slot}...')
        # Checks whether a booking is being placed today and if the desired slot starts less than 2 hours and 15 minutes from now.
        # If so, the desired slot is invalid.
        
        if all([
            date_to_book == date.today(),
            desired_slot.start_datetime.time() <= (datetime.now() + timedelta(hours=2, minutes=15)).time()
        ]):
            
            print(f'{desired_slot} is not far enough into the future to be booked.')
            continue

        for room_key in ROOM_PREFERENCE_LIST:
            
            print(f'Checking {room_key}...')
            taken_slot_list = get_taken_slot_list(room_key, date_to_book)            
            possible_slot_array = get_possible_slot_array(desired_slot, taken_slot_list, MIN_BOOKING_LENGTH)
            slot_to_book = get_slot_to_book(possible_slot_array, MAX_BOOKING_LENGTH)
            slot_to_book_option_list.append(slot_to_book)
            print(f'{room_key} is free for {slot_to_book}.')

            if slot_to_book == desired_slot:
                
                print('This is an exact match.')
                is_exact_desired_slot_found = True
                break
        
        if not is_exact_desired_slot_found:
            
            slot_to_book = max_datetimerange(slot_to_book_option_list)
            print(f'The best alternative is {slot_to_book}.')

            if slot_to_book == NO_BOOKING:
                
                continue
        
        room_to_book_key = ROOM_PREFERENCE_LIST[slot_to_book_option_list.index(slot_to_book)]
        print(f'Booking {slot_to_book} for {room_to_book_key} on {date_to_book}...')
        status = book_room(room_to_book_key, date_to_book, slot_to_book, BOOKING_DESCRIPTION)
        print(f'Booking placed: {status}')
        break