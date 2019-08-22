var socket;

window.onload = function () {
    socket = io();

    var dev_sdb = document.getElementById('/dev/sdb');
    var dev_sdc = document.getElementById('/dev/sdc');

    socket.on('progress_update', function (progress) {
        console.log(progress);
        if (progress.device == '/dev/sdb') {
            dev_sdb.innerHTML = progress.progress.toFixed(2);
        }
        if (progress.device == '/dev/sdc') {
            dev_sdc.innerHTML = progress.progress.toFixed(2);
        }
    });
};