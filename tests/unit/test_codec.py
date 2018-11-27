from expects import expect, equal
from shortener.codec import Codec


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class WhenEncodingInteger:
    def examples():
        yield {"input": 200, "expected": "3e"}
        yield {"input": 125, "expected": "21"}
        yield {"input": 74679, "expected": "jqv"}

    def given_i_have_an_integer(self, example):
        self.codec = Codec(ALPHABET)
        self.input = example["input"]

    def because_its_encoded(self):
        self.output = self.codec.encode(self.input)

    def it_should_return_the_correct_value(self, example):
        expect(self.output).to(equal(example['expected']))


class WhenDecodingInteger:
    def examples():
        yield {"input": "3e", "expected": 200}
        yield {"input": "21", "expected": 125}
        yield {"input": "jqv", "expected": 74679}
        yield {"input": "MUDmLAbN", "expected": 172254379891059}

    def given_i_have_an_encoded_string(self, example):
        self.codec = Codec(ALPHABET)
        self.input = example["input"]

    def because_its_decoded(self):
        self.output = self.codec.decode(self.input)

    def it_should_return_the_correct_value(self, example):
        expect(self.output).to(equal(example['expected']))
