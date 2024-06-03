// Updates loading bar.
var loadingCount = 1

socket.on('home:update_loading_bar', function() {

    console.log('Updating loading bar.');
    document.getElementById(`loadingSegment${loadingCount}`).className = 'currentLoadingSegment';

    loadingCount += 1;
    if(loadingCount <= 8) {

        nextLoadingSegment = document.getElementById(`loadingSegment${loadingCount}`);
        nextLoadingSegment.className = 'currentLoadingSegment';
        nextLoadingSegment.className = 'inactiveLoadingSegment';

    };
});

function update_free_slots() {

    socket.emit('home:update_free_slots');
    console.log(`Socket ${socket.id} requesting new free slots.`);

};

// Send request to update the slots available every 5 minutes (300,000 ms)
socket.on('connect', function() {

    console.log(`Socket ${socket.id} connected to homepage.`);
    socket.emit('home:connect');
    update_free_slots();
    loadingCount = 1;

});

//setInterval(update_free_slots, 300000);
//console.log('Update timer set for 5 minutes.');

socket.on('home:update_loading_bar', function() {

    console.log('Updating loading bar.');
    currentLoadingSegment = document.getElementById(`loadingSegment${loadingCount}`);
    currentLoadingSegment.classList.remove('currentLoadingSegment');

    loadingCount += 1;
    nextLoadingSegment = document.getElementById(`loadingSegment${loadingCount}`);
    nextLoadingSegment.classList.add('currentLoadingSegment');
    nextLoadingSegment.classList.remove('inactiveLoadingSegment');

});

socket.on('home:update_week_summary_html', function(weekSummaryHTML) {

    console.log(`New week summary HTML received by socket ${socket.id}`);
    document.getElementById('weekSummary').innerHTML = weekSummaryHTML;
//    document.getElementById('autobookerIndex').innerHTML = slotsToBookHTML;
//    document.getElementById('autobookerDiv').style.display = 'block';
//
//    console.log('Starting countdown.');
//
//    // Start countdown for autobooker.
//    var secLeft = 10;
//    var countdownTimer = setInterval(function () {
//
//        if (secLeft <= 0) {
//
//            clearInterval(countdownTimer);
//            socket.emit('home:proceed')
//            console.log('Autobooker activated.')
//
//        };
//
//        document.getElementById('countdown').textContent = secLeft;
//        secLeft -= 1;
//
//    }, 1000);

});
