var express = require('express');
var app = express();
var url = require("url")

app.get('/*', function (req, res) {
  
  var u = url.parse(req.url.toString())
  var path = decodeURIComponent(u.path).replace('/','')
  var d = new Date(path)
  if (isNaN(d)){
      var i = parseInt(path)
      if (!isNaN(i)) d = new Date(i*1000)
  }
  if (!isNaN(d)) {
    var monthNames = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"
    ];
    var j = {}
    j["unix"] = d.getTime()/1000;
    j["natural"] = monthNames[d.getMonth()]+" "+d.getDate()+", " +d.getFullYear();
    var json =JSON.stringify(j)
    res.end(json)
  }
  else{
    var j = {}
    j["unix"] = "null";
    j["natural"] = "null";
    var json =JSON.stringify(j)
    res.end(json)
  }
    

});

app.listen(process.env.PORT, function () {
  console.log('Timestamp microservice listening on port '+process.env.PORT+'!');
});