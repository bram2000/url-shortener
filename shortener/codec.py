class Codec:

    def __init__(self, alphabet):
        # Allow the client to pass the alphabet to use for encoding
        self.alphabet = alphabet

    @property
    def base(self):
        return len(self.alphabet)

    def encode(self, number):
        if number == 0:
            return self.alphabet[0]

        encoded = []
        while number > 0:
            number, remainder = divmod(number, self.base)
            encoded.append(self.alphabet[remainder])

        encoded.reverse()
        return "".join(encoded)

    def decode(self, encoded_string):
        acc = 0
        encoded = list(encoded_string)
        encoded.reverse()
        for index, value in enumerate(encoded):
            acc += self.alphabet.index(value) * (self.base ** index)
        return acc
