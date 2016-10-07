var express = require('express');
var app = express();
var url = require("url")

app.get('/*', function (req, res) {
  
  var u = url.parse(req.url.toString())
  var path = decodeURIComponent(u.path).replace('/','')
  console.log(path.toString())
  var d = Date.parse(path)
  if (isNaN(d)) res.end('Not a date!')
  else res.end (d.toDateString())
});

app.listen(process.env.PORT, function () {
  console.log('Example app listening on port '+process.env.PORT+'!');
});