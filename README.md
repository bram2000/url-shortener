# Getting started

## Requirements

 - make
 - docker
 - docker-compose

To run the service simply execute `make up`. This should build two docker containers (database and app) and run them both. Once complete you should see some logs, and the service should be available at `http://localhost:5000`.

# Usage

## Shorten

To shorten a url using the service, post a request to `http://localhost:5000/shorten_url` with a json payload containing the url to shorten, e.g.
```
{
    "url": "https://www.amnesty.org.uk/"
}
```
Here is an example using curl:
```
curl -H "Content-Type: application/json" -X POST http://localhost:5000/shorten_url -d '
{"url": "http://google.com"}
'
```
The response should contain the shortened url in it's json payload, e.g.
```
{"shortened_url":"http://localhost:5000/A0wJDGtT"}
```

## Lookup

To lookup a shortened url, simply make a GET request to the shortened__url. Example in curl;
```
curl "http://localhost:5000/CIkn8Fn6"
```
The response should be a 301 redirect, with the `Location` header pointing at the target resource, e.g.
```
< HTTP/1.0 301 MOVED PERMANENTLY
< Content-Type: text/html; charset=utf-8
< Content-Length: 241
< Location: http://google.com
< Server: Werkzeug/0.14.1 Python/3.7.1
< Date: Tue, 27 Nov 2018 16:48:05 GMT
```

# Performance
I have done a very crude benchmark of the system running locally on my laptop, and seen a throughput of around 100 posts/second for both the GET and POST requests.

## App tier

The implementation allows for horizontal scaling of the application tier, that is, we could run many python flask 'app' nodes behind a load-balancer, and trivially deal with many requests in parallel. At this point, the bottleneck becomes the database.

## DB tier

Read-only replicas of the database can be used to scale the read side of the application, at the expense of write-latency (e.g. a shortened url will not be immediately available on all nodes) however this can be tuned to a low, and probably negligable value (e.g. < 1 second).

Finally the write side of the database, which is the hardest to scale in this case. I would like to test the performance of the system running on production infrastructure, including the tweaks detailed above. I believe simply throwing some hardware at this would achieve a reasonable level of performance.
If more throughout is required at this point then we could start to look at vertically sharding the DB, where we use some criteria to break the datappart. For example you might run 5 DB nodes and `modulo 5` the url database id to detemine which database it should be put into. Conversely during the read we decode the shortened url string into the db id and use this to determine where we look for the data.
