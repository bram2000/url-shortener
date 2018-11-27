### Getting started

To run the service simply execute `make up`. This should build two docker containers (database and app) and run them both. Once complete you should see some logs, and the service should be available at `http://localhost:5000`.

### Usage

# Shorten

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

# Lookup

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
I have done a very crude benchmark of the system running locally on my laptop, and seen a url creation (e.g. POST) throughput of just over 100 posts/second.
