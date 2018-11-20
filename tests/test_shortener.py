import requests

# import json

from expects import expect, equal, contain


class WhenShorteningAValidUrl:
    def given_that_we_have_a_valid_url(self):
        self.url = "https://www.babylonhealth.com/about"

    def because_we_request_to_shorten_the_url(self):
        # body = json.dumps({"url": self.url})
        self.response = requests.post(
            "http://localhost:8080/shorten_url", json={"url": self.url}
        )

    def the_response_should_have_a_status_code_of_201(self):
        expect(self.response.status_code).to(equal(201))

    def the_response_should_have_json_content_type(self):
        content_encoding = self.response.headers["content-encoding"]
        expect(content_encoding).to(equal("application/json"))

    def the_response_should_contain_the_shortened_url(self):
        expect(self.response.json).to(contain("shortened_url"))


# class WhenRequestingAShortenedUrl:
#     def given_that_we_have_shortened_a_url(self):
#         self.url = "https://www.babylonhealth.com/blog"
#         post_response = requests.post(
#             "http://localhost:8080/shorten_url", json={"url": self.url}
#         )
#         self.shortened_url = post_response.json["shortened_url"]

#     def because_we_request_the_shortened_url(self):
#         self.response = requests.get(self.shortened_url)

#     def the_response_should_have_a_status_code_of_301(self):
#         status_code = self.response.status_code
#         expect(status_code).to(equal(301))
# TODO test the content? or at least the redirect target
