import requests
from requests.exceptions import HTTPError
import hashlib
import datetime
import os
import json


class MarvelAPI():

    def __init__(self):
        # Get public key from os environment
        self.public_key = os.getenv("MARVEL_PUBLIC_KEY")
        # Get private key from os environment
        self.private_key = os.getenv("MARVEL_PRIVATE_KEY")
        # Set base URL
        self.baseURL = "http://gateway.marvel.com/v1/public"
        # Get Timestamp and hash_string
        self.hashed_string, self.timestamp = self.get_hash()
        # Set basic URL params
        self.url_params = {
            'ts': self.timestamp,
            'apikey': self.public_key,
            'hash': self.hashed_string
        }

    def get_hash(self):
        # Set timestamp for web request
        self.timestamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
        self.hashed_input = self.timestamp + self.private_key + self.public_key
        self.hashed_string = hashlib.md5(self.hashed_input.encode("utf-8")).hexdigest()
        return self.hashed_string, self.timestamp

    def get_characters(self, request_limit=20, request_offset=0):
        # Define base URL for characters
        self.baseURL = "%s/%s" % (self.baseURL, "characters")
        try:
            # Configure request params
            self.url_params['limit'] = request_limit
            self.url_params['offset'] = request_offset
            response = requests.get(self.baseURL, params=self.url_params)
            # Validate request result
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error : {http_err}')
        except Exception as err:
            print(f'Generic exception : {err}')
        else:
            # Return JSON payload
            return response.json()

    def save_characters_data(self, outfile, request_limit=20, request_offset=0):
        json_characters = self.get_characters(request_limit=request_limit,
                                              request_offset=request_offset)
        with open(outfile, 'w', encoding='utf-8') as _file:
            _file.write(json.dumps(json_characters, indent=4))


if __name__ == '__main__':
    """
    MarvelAPI Class Test
    """
    marvel_api = MarvelAPI()
    marvel_api.save_characters_data('characters.json')
