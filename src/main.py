import atexit
from the_edge_bath import *
from user_input import *
from user_input_func import *


atexit.register(lambda: driver.quit())
sign_in(EMAIL, PASSWORD)
    
preset_date_list, preset_slot_list = filter_user_booking_list(USER_BOOKING_LIST)
future_date_list, _, _ = get_future_booking_list()
date_to_find_array = np.setdiff1d(preset_date_list, future_date_list)

for date_to_book in date_to_find_array:
    
    driver.get(HOME_URL)
    is_exact_desired_slot_found = False
    slot_to_book_option_list = []
    
    for desired_slot in preset_slot_list[preset_date_list.index(date_to_book)]:

        for room_key in ROOM_PREFERENCE_LIST:

            taken_slot_list = get_taken_slot_list(room_key, date_to_book)            
            possible_slot_array = get_possible_slot_array(desired_slot, taken_slot_list, MIN_BOOKING_LENGTH)
            slot_to_book = get_slot_to_book(possible_slot_array, MAX_BOOKING_LENGTH)
            if slot_to_book == desired_slot:

                is_exact_desired_slot_found = True
                break

            slot_to_book_option_list.append(slot_to_book)
        
        if not is_exact_desired_slot_found:

            slot_to_book = max_datetimerange(slot_to_book_option_list)
            
            if slot_to_book == NO_BOOKING:
                
                continue

        status = book_room(room_key, date_to_book, slot_to_book, BOOKING_DESCRIPTION)
        print([date_to_book, slot_to_book, room_key, status])