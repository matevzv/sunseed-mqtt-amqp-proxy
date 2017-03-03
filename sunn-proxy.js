var amqp = require('amqplib/callback_api');

var host = "amqp://bpl-sunrabbit1.ts.telekom.si"
var exchange = "wams_exchange"
var routing_key = "wams.spm"

var publish = function (mqtt) {
  amqp.connect(host, function(err, conn) {
    conn.createChannel(function(err, ch) {
      ch.assertExchange(exchange, 'topic', {durable: true});
      mqtt.on('message', function(topic, data) {
        ch.publish(exchange, routing_key, new Buffer(data));
      });
    });
  });
}

exports.publish = publish;
