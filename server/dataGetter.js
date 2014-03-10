function parsePercentFile(output) {
	var fs = require('fs');
	var array = fs.readFileSync('/home/axel/PycharmProjects/CS4240Project/predictioneaglesredskins.txt').toString().split("\n");
	for(i in array) {
	    values = array[i].split(" ");
	    name = values[0];
	    percentage = values[1];
	    output[name] = percentage;
	}
}
exports.parsePercentFile = parsePercentFile;