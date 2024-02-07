from datetime import date, timedelta
from datetimerange import DateTimeRange
from user_input import NO_BOOKING

def filter_user_booking_list(user_booking_list):
    
    date_to_find_list = []
    slots_to_find_list = []
    
    for i in range(1, 8):
        
        date_to_find = date.today() + timedelta(days=i)
        desired_slot_list = user_booking_list[date_to_find.weekday()]
        
        # Check if a booking should be made on date_to_book.
        if desired_slot_list[0] != NO_BOOKING:
            
            date_to_find_list.append(date_to_find)
            slots_to_find_list.append(desired_slot_list)
    
    return [date_to_find_list, slots_to_find_list]