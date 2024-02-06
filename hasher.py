import hashlib

class Hasher:
    """
    Hasher class to easily call to hash a given string (usually an URL).

    :author: Sabri MOUSSA
    """
    def __init__(self):
        self.hash = hashlib.shake_128()

    def hashString(self, inputString: str, size: int) -> str:
        """
        Hash a given input string and return the hash value
        :param inputString: The string to hash
        :param size: The size of the resulting hash

        :return hash: The hash value
        :author: Sabri MOUSSA
        """
        self.hash.update(bytes(inputString, 'utf8'))
        return self.hash.hexdigest(size)
