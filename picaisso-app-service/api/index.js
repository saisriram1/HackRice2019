// const express = require('express');
// const cors = require('cors');
// const mysql = require('mysql');
// const bodyParser = require('body-parser');
//
// const app = express()
// app.use(cors())
//
// app.use(bodyParser.json() );       // to support JSON-encoded bodies
// app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
//   extended: true
// }));
//
// app.use(express.json());       // to support JSON-encoded bodies
// app.use(express.urlencoded());       // to support JSON-encoded bodies
//
//
//
// var epoch = null;
// var accuracy = null;
//
// var download_model= '';
// var download_images= '';
//
// app.post('/download', (req, res) => {
//         console.log("Download posted");
//         download_model = req.body.model_dl_link;
//         download_images = req.body.dataset_dl_link;
//         res.send("Received POST request");
// })
//
// app.get('/generations', (_req, res) => {
//   res.json({"epoch": epoch, "accuracy": accuracy});
// });
//
// app.post('/', (req, res) => {
//   epoch = req.body.epoch;
//   accuracy = req.body.accuracy;
//
//   console.log("Epoch: "+epoch);
//   console.log("Accuracy: "+accuracy);
//   res.send("");
// });
//
//
// app.listen(4000);

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = process.env.PORT || 4000;
const cors = require('cors');

const app = express();
app.use(cors());

app.use(bodyParser.json() );       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
}));

app.use(express.json());       // to support JSON-encoded bodies
app.use(express.urlencoded());       // to support JSON-encoded bodies

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  socket.on('generations', function(msg){
    io.emit('generations', msg);
  });
});

http.listen(port, function(){
  console.log('listening on *:' + port);
});
