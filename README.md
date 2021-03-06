# Getting started

## Requirements

 - make
 - docker
 - docker-compose

To run the service simply execute `make up`. This will build two docker containers (database and app) and run them both. The containers will print some logging to stdout. The default service address is `http://localhost:5000`.

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
The response contains the shortened url in its json payload, e.g.
```
{"shortened_url":"http://localhost:5000/A0wJDGtT"}
```

## Lookup

To lookup a shortened url, simply make a GET request to the shortened__url. Example in curl;
```
curl "http://localhost:5000/CIkn8Fn6"
```
The response is a standard 301 redirect, with the `Location` header pointing at the target resource, e.g.
```
< HTTP/1.0 301 MOVED PERMANENTLY
< Content-Type: text/html; charset=utf-8
< Content-Length: 241
< Location: http://google.com
< Server: Werkzeug/0.14.1 Python/3.7.1
< Date: Tue, 27 Nov 2018 16:48:05 GMT
```

# Testing

## Acceptance
To run acceptance tests, start the service as normal using `make up`, then trigger the tests from another terminal using `make acceptance`. The tests run inside the app container.

## Unit
To run the unit tests you need a python environment (virtual environment is recommended). Once you have a suitable python3 environment, install the application and it's dependencies with `pip3 install -e .`. `make unit` will then execute the unit tests.

# Implementation notes
In order to avoid using sequential ids (which would make it trivial for people to a) know how many urls we have shortened and b) scan them all) and for the sake of performance, we choose a random id to use for each entry in the url repository. If we collide with an existing row, we simply try again. This should work well until the service contains a large number of urls, at which point we could start clearing old entries (e.g. add a 'date_added' field and clean regularly) or just increase the address space (make slightly longer shortened urls).

# Performance
I have done a very crude benchmark of the system running locally on my laptop, and seen a throughput of around 100 posts/second for both the GET and POST requests.

## App tier

This app is built on top of the lightweight 'flask' framework, so the request handling is entirely synchronous. As such, the app would need to be horizontally scaled in order to achieve any significant level of performance. One way to do this would be to use gunicorn to marshal requests across a group of workers, another would be to use a load balancer (e.g. ElasticLoadBalancer on AWS) above a bunch of docker containers. Lots of ways to skin this cat!
At the point where we have parallelised the request handling, the bottleneck would become the database....

## DB tier

Read-only replicas of the database can be used to scale the read side of the application, at the expense of write-latency (e.g. a shortened url will not be immediately available on all nodes) however this can be tuned to a low, and probably negligible value (e.g. < 1 second).

Finally the write side of the database, which is the hardest to scale in this case. I would like to test the performance of the system running on production infrastructure, including the tweaks detailed above. I believe simply throwing some hardware at this would achieve a reasonable level of performance.
If more throughout is required at this point we could start to look at vertically sharding the DB, where we use some criteria to break the data apart. For example you might run 5 DB nodes and `modulo 5` the url database id to determine which database it should be put into. Conversely during the read we decode the shortened url string into the db id and use this to determine where we look for the data.
