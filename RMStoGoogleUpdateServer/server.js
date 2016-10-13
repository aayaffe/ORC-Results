
var express = require('express');
var app = express();

var PythonShell = require('python-shell');



app.get('/update', function (req, res) {
     var options = {
        mode: 'text',
        pythonPath: 'python3'
    };
     console.log("Running update.")
     res.write("Running update.\n")
     PythonShell.run("parseRMS.py", options, function (err, results) {
        if (err) {
            console.log(err);
            res.end(err);
        }
        else{
            res.end("Update done")
            console.log(results)
            console.log('finished');
        }
        
     });
});

app.listen(process.env.PORT, function () {
  console.log('RMStoGoogleUpdateServer microservice listening on port '+ process.env.PORT+'!');
});