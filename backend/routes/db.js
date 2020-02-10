const express = require('express');
const MongoClient =  require('mongodb').MongoClient;
const app = express();
const uri = "mongodb+srv://jeffrey856:{}@safeplatedb-p4xjd.mongodb.net/test?retryWrites=true&w=majority";
const database_name = 'restaurants'
const logger = require('morgan');


app.use(logger('dev'));
app.use(express.json());

var database, collection;

app.get('/db', (req, res, next) => {
  console.log('In db.js');
  var projection = {business_name:req.query.search};
  // Connect to database
  MongoClient.connect(uri, { useNewUrlParser: true }, (error, client) => {
    if (error) {
      throw error;
    }
    database = client.db(database_name);
    collection = database.collection('restaurant');
    console.log("Connected to `" + database_name + "`!");
    collection.find().limit(4).toArray((err, items) => {
      console.log(items);
      res.send({express: items})

//    collection.find(projection).toArray((err, items) => {
//      console.log('Retrieved items');
      // res.type('json');
//      res.send(items);
    });
  });
}); 

const port = 3030;
app.listen(port, () => console.log(`MongoDB app listening on ${port}..`));

