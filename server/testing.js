var fs = require('fs');
var array = fs.readFileSync('/home/axel/PycharmProjects/CS4240Project/redskinsValues.txt').toString().split("\n");
for(i in array) {
    console.log(array[i]);
}