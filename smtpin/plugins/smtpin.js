// SMTP in plugin for PEPS
// Copyright (c) MLstate, 2015
//
// Contains code from https://github.com/jplock/haraka-http-forward
// Copyright (c) 2013 Justin Plock
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

var request = require('request');
var host, domain;

exports.register = function () {
    var config = this.config.get('/usr/local/haraka/config/smtpin.ini');
    if (config.main.host) {
        // check validity
        var match = /^([^: ]+)(?::(\d+))?$/.exec(config.main.host);
        if (match) {
            host = config.main.host;
            request('http://' + host + '/domain',
                function (error, response, body) {
                    if (!error && response.statusCode == 200) {
                        domain = body;
                    } else { throw new Error('could not get domain from ' + host); }
                }
            );
        } else { throw new Error('could not parse host value: ' + config.main.host) }
    } else { throw new Error('configuration file missing') }
};

exports.hook_data_post = function (next, connection) {
    var transaction = connection.transaction;
    // TODO: check that recipients (transaction.rcpt_to) matches domain name?
    var options = {
        'uri': 'http://' + host,
        'headers': {
            'Content-Type': 'text/plain; charset=utf-8'
        },
        'method': 'post',
        'timeout': 1000,
        'pool': false,
        'jar': false
    };

    var forward = request.post(options);
    forward.on('error', function (err) {
        connection.logerror('unable to connect to ' + host + ' (' + err + ')');
        return next();
    });
    forward.on('end', function () {
        return next();
    });

    var pipe_options = {'dot_stuffing': true, 'ending_dot': true};
    transaction.message_stream.pipe(forward, pipe_options);
};
