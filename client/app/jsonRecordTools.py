from datetimerange import DateTimeRange
import json


def get_schedule_list(scheduleName):

    with open(f'app/bookingSchedules/{scheduleName}.json', 'r') as file:
        scheduleDict = json.load(file)

    return [DateTimeRange.from_range_text(dataList[0]) for _, dataList in scheduleDict.items()]


def get_schedule_data_func(indexInt):

    def get_schedule_data(scheduleName):

        with open(f'app/bookingSchedules/{scheduleName}.json', 'r') as file:

            scheduleDict = json.load(file)

        return [dataList[indexInt] for _, dataList in scheduleDict.items()]

    return get_schedule_data

get_room_list = get_schedule_data_func(1)
get_mode_list = get_schedule_data_func(2)
