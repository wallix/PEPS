// SMTP out plugin for PEPS
// Copyright (c) MLstate, 2015

exports.hook_mail = function (next, connection, params) {
  connection.relaying = true;
  next();
}

