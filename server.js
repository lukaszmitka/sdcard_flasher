'use strict';

var app = require('express')();
var express = require('express');
var http = require('http').createServer(app);
var io = require('socket.io')(http);

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});

app.use(express.static('public'))

function emit_progress(progress) {
  io.emit('progress_update', progress);
}

io.on('connection', function (socket) {
  console.log('a user connected');
  socket.on('disconnect', function () {
    console.log('user disconnected');
  });

  socket.on('flash-update', function (progress) {
    emit_progress(progress)
    console.log(progress);
  });

});

http.listen(3000, function () {
  console.log('listening on *:3000');
});
