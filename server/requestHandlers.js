var querystring = require("querystring");
var dataGetter = require("./dataGetter");
var exec = require('child_process').exec;

function getData(response, postData) {
  exec('python ApprovalPredictor.py redskins eagles', function callback(error, stdout, stderr){
    console.log(error)
  });

  console.log("Request handler 'getData' was called.");
  response.writeHead(200, {"Content-Type": "application/json"});

  var values = {}
  dataGetter.parsePercentFile(values);

  var json = JSON.stringify({ 
    keysAndPercents: values
  });
  response.end(json);
}

exports.getData =getData;