const express = require('express');
const router = express.Router();
const http = require('http');
const request = require('request');

/* GET query */
router.get('/query', function(req, res, next) {
  var search;
  try {
      console.log('trying to find parameter');
      search = req.query.search || '';
  }
  catch (err) {
      console.log(err);
      search = ''
  }

  if (search != '') {
    /* FORWARD query to database */
    url = 'http://localhost:3030/db';
    param = '?search=' + search;
    full = url + param;
    request.get(full, (err, res, body) => {
      if (err) {
        console.log('Error');
      } else {
        console.log(body);
      }
    });
  }

  res.json({message: 'Received query.', params: search});
});

module.exports = router;
