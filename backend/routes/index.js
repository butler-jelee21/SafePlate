const express = require('express');
const router = express.Router();

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
	res.json({message: 'Received query.', params: search});
});

module.exports = router;
