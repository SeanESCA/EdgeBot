import dayjs from 'dayjs'
import { useState } from 'react'
import Select from 'react-select'
import makeAnimated from 'react-select/animated'
import 'dayjs/locale/en-gb'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { TimePicker } from '@mui/x-date-pickers/TimePicker'

const roomOptionList = [
    {'value': 'room 1', 'label': 'Music Practice Room 1'},
    {'value': 'room 2', 'label': 'Music Practice Room 2'},
    {'value': 'buchan', 'label': 'Buchan Solo Practice Room'},
    {'value': 'choral', 'label': 'Choral Practice Room'}
]

const timeList = [
    {'day': 'Monday', 'openingTime': '09:00', 'closingTime': '22:00'}, 
    {'day': 'Tuesday', 'openingTime': '09:00', 'closingTime': '22:00'}, 
    {'day': 'Wednesday', 'openingTime': '09:00', 'closingTime': '22:00'}, 
    {'day': 'Thursday', 'openingTime': '09:00', 'closingTime': '22:00'}, 
    {'day': 'Friday', 'openingTime': '09:00', 'closingTime': '22:00'}, 
    {'day': 'Saturday', 'openingTime': '10:00', 'closingTime': '20:00'}, 
    {'day': 'Sunday', 'openingTime': '10:00', 'closingTime': '18:00'}
]

function PreferenceForm() {

    const animatedComponents = makeAnimated()
    const [startTime, setStartTime] = useState(null)
    const minStartTime = dayjs('09:00', 'HH:mm')
    const maxStartTime = dayjs('22:00', 'HH:mm')

    return(
        <form method="POST" id="credential_form">
            <label for="room_preference_list">
                <h3>Room Preferences</h3>
                <p>Please list the rooms you would like to use in order of preference. If a room is not selected, it will not be considered by EdgeBot.</p>
            </label>
            <Select
                closeMenuOnSelect={false}
                components={animatedComponents} 
                id="room_preference_list"
                isMulti
                makeAnimated
                options={roomOptionList}
                name='room_preference_list' 
                required 
            />

                <h3>Slot Preferences</h3>
                <p>Please list the slots you would like EdgeBot to check for every time you visit. If you leave a day empty, EdgeBot will consider that you usually do not want to book a room on that day.</p>
                <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="en-gb">
                    <TimePicker
                        label="Start Time"
                        minTime={minStartTime}
                        maxTime={maxStartTime}
                        minutesStep={15} 
                        onChange={(newStartTime) => {setStartTime(newStartTime)}}
                        onError={(error) => {
                            error == 'minTime'
                                ? setStartTime(minStartTime)
                                : error == 'maxTime'
                                    && setStartTime(maxStartTime)
                        }}
                        value={startTime}
                    />
                </LocalizationProvider>
            {/* {timeList.map(({dayStr}) =>  */}
                <div>
                    {/* <h4>{dayStr}</h4> */}
                    
                    {/* <TimePicker disableClock format="hh:mm" minTime="09:00" maxTime="22:00" onChange={setStartTime} value={startTime}/> */}
                </div>
            {/* )} */}
        </form>
        // // 
        //     {/* If UoB username submitted, do not display booking description field. */}
        // // 
    )
}

export default PreferenceForm