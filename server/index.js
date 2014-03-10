var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["/"] = requestHandlers.getData;
handle["/getData"] = requestHandlers.getData;

server.start(router.route, handle);