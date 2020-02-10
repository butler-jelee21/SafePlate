const express = require('express');
const router = express.Router();
const http = require('http');
const request = require('request');
const qs = require('querystring');
const db_request = require('../util/db_request.js');

/* GET query */
router.get('/query', function(req, res, next) {
  var search;
  try {
      console.log('trying to find parameter..');
      search = req.query.search || '';
  }
  catch (err) {
      console.log('..cannot find parameter');
      console.log(err);
      search = '';
  }

  if (search != '') {
    /* FORWARD query to database */
    var url = 'http://localhost:3030';
    var path = '/db';
    var properties = {
      search: search
    };
    var full = url + path + '?' + qs.encode(properties);
    db_request.getMongoQuery(full).then(function(data) {
      console.log('Generating a response to client..');
      if (data === '[]') {
        res.status(500);
        res.json({error: 'Error making MongoDB query.', message: `${search} does not exist in DB.`});
      } else {
        // res.json({message: 'Received query.', params: search, data: JSON.parse(JSON.stringify(data))});
        res.json({message: 'Received query.', params: search, data: data});
      }
    }).catch(function(err) {
      console.log(err);
      res.status(500);
      res.json({error: 'Error making MongoDB query.', message: `${search} does not exist in DB.`});
    });
  } else {
    res.json({message: 'Received query.', params: search});
  }

});

module.exports = router;
