var express = require('express')
var bodyParser = require('body-parser')
const { exec } = require('child_process');

var app = express();

var urlencodedParser = bodyParser.urlencoded({ extended: false })

var mongoClient = require('mongodb').MongoClient;
const url = 'mongodb://localhost:27017';
let db;
mongoClient.connect(url, function(err, client) {
    db = client.db("Indexed");
});

app.route("/").get(function(req,res){
        var crawls = []
        var cursor = db.collection('crawler').find();
        cursor.forEach(function(item){
            crawls.push(item);
        }).then(function(){
            res.render("result",{'crawls':crawls,'len':crawls.length});
        })
    })

    app.route("/index").get(function(req,res){
        res.render("index");
    })

    app.post("/validate",urlencodedParser,function(req,res){
        var url = req.body.search;
        exec("scrapy runspider main.py --nolog -a url="+url,(err, stdout, stderr) => {
            if (err) {
              console.log(err)
              return;
            }
        })
        res.redirect("/")
    })
    
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.listen(3000);