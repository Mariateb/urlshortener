import hashlib


def hash_password(input_password: str) -> str:
    """
    Hash a given password and return the hashed one
    :param input_password: The string to hash
    :param size: The size of the resulting hash

    :return hash: The hash value
    :author: Sabri MOUSSA
    """
    computed_hash = hashlib.md5(bytes(input_password, 'utf8'))
    return computed_hash.hexdigest()


class Hasher:
    """
    Hasher class to easily call to hash a given string (usually an URL).

    :author: Sabri MOUSSA
    """

    def __init__(self):
        self.hash = hashlib.shake_128()

    def hash_string(self, input_string: str, size: int = 4) -> str:
        """
        Hash a given input string and return the hash value
        :param input_string: The string to hash
        :param size: The size of the resulting hash

        :return hash: The hash value
        :author: Sabri MOUSSA
        """
        self.hash.update(bytes(input_string, 'utf8'))
        return self.hash.hexdigest(64)[:size]
