import requests
from expects import expect, equal, have_key


class WhenShorteningAValidUrl:
    def given_that_we_have_a_valid_url(self):
        self.url = "https://www.babylonhealth.com/about"

    def because_we_request_to_shorten_the_url(self):
        self.response = requests.post(
            "http://localhost:5000/shorten_url", json={"url": self.url}
        )

    def the_response_should_have_a_status_code_of_201(self):
        expect(self.response.status_code).to(equal(201))

    def the_response_should_have_json_content_type(self):
        content_type = self.response.headers["content-type"]
        expect(content_type).to(equal("application/json"))

    def the_response_should_contain_the_shortened_url(self):
        body = self.response.json()
        expect(body).to(have_key("shortened_url"))


class WhenShorteningAnInvalidUrl:
    def given_that_we_have_an_invalid_url(self):
        self.url = "httttp///this.does.not.look.correct@"

    def because_we_request_to_shorten_the_url(self):
        self.response = requests.post(
            "http://localhost:5000/shorten_url", json={"url": self.url}
        )

    def the_response_should_have_a_status_code_of_400(self):
        expect(self.response.status_code).to(equal(400))

    def the_response_should_have_json_content_type(self):
        content_type = self.response.headers["content-type"]
        expect(content_type).to(equal("application/json"))

    def the_response_should_contain_a_sensible_error(self):
        body = self.response.json()
        expect(body).to(equal({"error": "url failed validation"}))


class WhenRequestingAShortenedUrl:
    def given_that_we_have_shortened_a_url(self):
        self.url = "https://www.babylonhealth.com/blog"
        post_response = requests.post(
            "http://localhost:5000/shorten_url", json={"url": self.url}
        ).json()
        self.shortened_url = post_response["shortened_url"]

    def because_we_request_the_shortened_url(self):
        self.response = requests.get(self.shortened_url, allow_redirects=False)

    def the_response_should_have_a_status_code_of_301(self):
        status_code = self.response.status_code
        expect(status_code).to(equal(301))

    def the_response_should_redirect_to_the_correct_url(self):
        redirected_url = self.response.headers['Location']
        expect(redirected_url).to(equal(self.url))
