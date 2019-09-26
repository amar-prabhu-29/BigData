var express = require('express')
var app = express();
var mongoClient = require('mongodb').MongoClient;
const url = 'mongodb://localhost:27017';
let db;
mongoClient.connect(url, function(err, client) {
    db = client.db("Indexed");
});

var str = "";
app.route("/").get(function(req,res){
        var crawls = []
        var cursor = db.collection('crawler').find();
        cursor.forEach(function(item){
            crawls.push(item);
        }).then(function(){
            res.render("result",{'crawls':crawls,'len':crawls.length});
        })
    })
    
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.listen(3000);