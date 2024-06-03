from datetime import datetime, timedelta
from pprint import pprint

pprint([{"startTime": (datetime(year=1900, month=1, day=1, hour=9) + timedelta(minutes=i)).strftime("%H:%M"), "username": None} for i in [30*j for j in range(25)]])
