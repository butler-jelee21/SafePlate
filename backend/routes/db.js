const express = require('express');
const MongoClient =  require('mongodb').MongoClient;
const app = express();
const uri = "mongodb+srv://jeffrey856:cookies1234@safeplatedb-p4xjd.mongodb.net/test?retryWrites=true&w=majority";
const database_name = 'restaurants'

var database, collection;

app.get('/db', (req, res, next) => {
  console.log('In db.js');
  // Connect to database
  MongoClient.connect(uri, { useNewUrlParser: true }, (error, client) => {
    if (error) {
      throw errror;
    }
    database = client.db(database_name);
    collection = database.collection('restaurant');
    console.log("Connected to `" + database_name + "`!");
    collection.find().toArray((err, items) => {
      console.log(items);
    });
  });
}); 

const port = 3030;
app.listen(port, () => console.log(`MongoDB app listening on ${port}..`));

