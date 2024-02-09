from datetime import timedelta
from datetimerange import DateTimeRange


# PRESET_BOOKING_LIST is ordered Mon - Sun.
# Do not change the dates from 0001-01-01.
# If you have multiple preferred slots in a day, list them from most to least preferred.
# If you are booking for today, please ensure that the slot chosen is at least 2 hours and 15 minutes from now.
NO_BOOKING = DateTimeRange('0001-01-01T00:00:00', '0001-01-01T00:00:00')
USER_BOOKING_LIST = [
    [
        NO_BOOKING
    ],
    [
        NO_BOOKING
    ],
    [
        NO_BOOKING
    ],
    [
        DateTimeRange('0001-01-01T10:15:00', '0001-01-01T11:45:00')
    ],
    [
        NO_BOOKING
    ],
    [
        NO_BOOKING
    ],
    [
        NO_BOOKING
    ],
]

# ROOM_PREFERENCE_LIST is ordered from most preferred to least. Options: ['room 2', 'room 1', 'buchan', 'choral']
# If you do not want to use a specific room, do not include it in the list.
ROOM_PREFERENCE_LIST = ['choral', 'room 2', 'room 1', 'buchan']

# Your UoB username.
USERNAME = ''

# If you have registered with the Edge using an email other than your UoB email, enter it below.
EMAIL = f'{USERNAME}@bath.ac.uk'

# The password for your Edge account.
PASSWORD = ''

# As per the booking form, this will be your UoB username by default.
BOOKING_DESCRIPTION = USERNAME

# The minimum and maximum length you would like your bookings to be.
MIN_BOOKING_LENGTH = timedelta(hours=0, minutes=30)
MAX_BOOKING_LENGTH = timedelta(hours=2, minutes=0)