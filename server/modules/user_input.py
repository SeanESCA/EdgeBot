from datetime import timedelta
from datetimerange import DateTimeRange


# PRESET_BOOKING_LIST is ordered Mon - Sun.
# Do not change the dates from 1900-01-01.
# If you have multiple preferred slots in a day, list them from most to least preferred.
NO_BOOKING = DateTimeRange('1900-01-01T00:00:00', '1900-01-01T00:00:00')
USER_BOOKING_LIST = [
    [
        NO_BOOKING
    ],
    [
        DateTimeRange('1900-01-01T09:00:00', '1900-01-01T11:00:00'),
        DateTimeRange('1900-01-01T12:00:00', '1900-01-01T14:00:00')
    ],
    [
        DateTimeRange('1900-01-01T09:00:00', '1900-01-01T11:00:00')
    ],
    [
        DateTimeRange('1900-01-01T09:00:00', '1900-01-01T11:00:00')
    ],
    [
        NO_BOOKING
    ],
    [
        DateTimeRange('1900-01-01T09:00:00', '1900-01-01T11:00:00')
    ],
    [
        NO_BOOKING
    ],
]

# ROOM_PREFERENCE_LIST is ordered from most preferred to least. Options: ['room 2', 'room 1', 'buchan', 'choral']
# If you do not want to use a specific room, do not include it in the list.
ROOM_PREFERENCE_LIST = ['room 2', 'room 1', 'buchan', 'choral']

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