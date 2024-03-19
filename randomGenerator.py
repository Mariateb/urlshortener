import hashlib

from fastapi import HTTPException
import random

class RandomGenerator:
    """
    Generator class to generate a string of characters randomly

    :author: Sabri MOUSSA
    """

    def __init__(self):
        self.lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                          't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                          'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.digits = ['0', '1', '2', '3', '4', '5', '6', "7", "8", "9"]
        self.specialCharacters = ['_', '-']

    def generate(self, size: int = 6, useLowercase: bool = True, useUppercase: bool = True, useDigits: bool = True, useSpecial: bool = True) -> str:
        availableCharacters = []
        if useLowercase:
            availableCharacters.extend(self.lowercase)
        if useUppercase:
            availableCharacters.extend(self.uppercase)
        if useDigits:
            availableCharacters.extend(self.digits)
        if useSpecial:
            availableCharacters.extend(self.specialCharacters)
        try:
            toReturn = ""
            for _ in range(size):
                toReturn += random.choice(availableCharacters)
            return toReturn
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))
