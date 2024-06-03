from .extensions import socketio, emit
from flask import request, session
from TheEdgeTools import driver, sign_in
from EdgeBookingAppV1.app.extensions import socketio, emit
from EdgeBookingAppV1.app.TheEdgeTools import *

username = 'secas20'
password = 'AlwaysonEdge345!'
roomNameDict = {
    'buchan': 'Buchan Solo Practice Room',
    'room2' : 'Music Practice Room 2',
    'room1' : 'Music Practice Room 1',
    'choral': 'Choral Practice Room'
}

def get_date_free_slots_html(dateToCheck: datetime, dateFreeSlotDict):

    dateSummaryHTML = ''

    for roomStr, freeSlotList in dateFreeSlotDict.items():

        slotsForRoomHTML = ''

        # Create HTML to show free slots.
        for slot in freeSlotList:

            slot.start_time_format = '%H:%M'
            slot.end_time_format = '%H:%M'
            slotsForRoomHTML = f'{slotsForRoomHTML}<div><p>{slot}</p></div>'

        dateSummaryHTML = (
            f'{dateSummaryHTML}<div class="roomSummary">'
            f'<span><h3>{roomNameDict[roomStr]}</h3></span>'
            f'<span>{slotsForRoomHTML}</span>'
            f'</div>'
        )

    if bookingDetailsStr:

        dateSummaryDisplay = 'none'

    else:

        dateSummaryDisplay = 'block'

    dayID = f'{dateToCheck.strftime("%a").lower()}Summary'

    return (f'<div>'
            f'<span class="dateSummaryHeader"><h1>{dateToCheck.strftime("%A, %d %b %Y")}</h1></span>'
            f'<span class="bookingDetails"><p>{bookingDetailsStr}</p></span></div>'
            f'<div style="display: {freeSlotSummaryDisplay};">{dateSummaryHTML}</div>'
            f'</div>')

def get_booking_suggestion_html(dateToCheck: datetime):

    if all([roomStr == presetMainRoomList[dayInt],
            dateKey in bookingRange]):
        slotToBook = select_preset_slot(
            presetMainRangeList[dayInt],
            freeSlotList,
            presetMainModeList[dayInt]
        )
        slotsToBookHTML = (f'{slotsToBookHTML}' \
                           f'<input type="checkbox" name="slotToBookIndex[]" checked>' \
                           f'{dateKey.strftime("%A (%d %b %Y)")}, {slotToBook}, {roomNameDict[roomStr]}<br>')
        slotToBookList.append((dateKey.strftime('%d %m %Y'), str(slotToBook), roomStr))

    slotsForRoomHTML = ''
@socketio.on('home:connect')
def on_connect():

    print(f'Socket {request.sid} connected to homepage.')

@socketio.on('home:disconnect')
def on_disconnect():

    # Stop any active processes.
    print(f'Socket {request.sid} disconnected from homepage.')

@socketio.on('home:update_slots')
def update_week_free_slots():

    print('Signing in!')
    sign_in(username, password)
    print('Getting HTML!')
    weekFreeSlotDict = summarise_week_free_slots()
    weekSummaryHTML = ''

    for dateKey, dateFreeSlotDict in weekFreeSlotDict.items():

        weekSummaryHTML = f'{weekSummaryHTML}{get_date_free_slots_html(dateKey, dateFreeSlotDict)}'

    emit('home:update_week_summary_html', weekSummaryHTML, broadcast=True)