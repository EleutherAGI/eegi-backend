from jwt import JWT, jwk_from_pem
from jwt.utils import get_int_from_datetime

from datetime import timedelta, datetime
from pathlib import Path
import os

from typing import Dict

def get_root() -> str:
    return str(Path(__file__).parent.parent) + os.sep

class AccessToken:

    def __init__(self):

        self.__token = JWT()
        self.__algorithm = 'RS256'

        with open(get_root() + 'rsa_private.pem', 'rb') as private_key:
            self.__signing_key = jwk_from_pem(private_key.read())

        with open(get_root() + 'rsa_public.pem', 'rb') as public_key:
            self.__verifying_key = jwk_from_pem(public_key.read())

    def create_access_token(self, 
                            data: dict, 
                            expiration: timedelta = timedelta(minutes=15)) -> str:
        expiry = datetime.utcnow() + expiration
        to_encode = data.copy()
        to_encode.update({
            "ist": get_int_from_datetime(datetime.utcnow()),
            "exp": get_int_from_datetime(expiry)
        })
        return self.__token.encode(to_encode, self.__signing_key, self.__algorithm)

    def decode_access_token(self, token: str) -> Dict:
        return self.__instance.decode(token, self.__verifying_key,
                                      do_time_check=False)

access_token = AccessToken()