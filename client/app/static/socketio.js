const socket = io({
    'reconnection': true,
    'reconnectionAttempts': 5,
    'reconnectionDelay': 1000,
    'reconnectionDelayMax': 5000,
    });

socket.on('connect', function() {

    socket.emit('socket id', socket.id)
    console.log('Socket ' + socket.id + ' connected!')

})