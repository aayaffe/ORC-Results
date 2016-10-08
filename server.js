var express = require('express');
var app = express();
var url = require("url")

app.get('/*', function (req, res) {
  
  var h = req.headers;
  if (h){
    var j = {}
    j["ipaddress"] = req.get("x-forwarded-for");
    
    var regExp = /\w\w-\w\w/g;
    var matches = regExp.exec(req.get("accept-language"));
    j["language"] = matches[0];
    regExp = /\(([^)]+)\)/;
    matches = regExp.exec(req.get("user-agent"));
    j["software"] = matches[1];
    var json =JSON.stringify(j)
    res.end(json)
  }
});

app.listen(process.env.PORT, function () {
  console.log('Request Header Parser Microservice listening on port '+process.env.PORT+'!');
});