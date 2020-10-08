import requests

from django.conf import settings

data = {
    'daemonHost': settings.COIN_DAEMON_HOST,
    'daemonPort': int(settings.COIN_DAEMON_PORT),
    'filename': settings.WALLET_FILENAME,
    'password': settings.WALLET_PASSWORD
}


class ApiWrapper(object):
    wallet_is_open = False

    def get_request_function(self, req_method):
        if req_method == 'POST':
            return requests.post
        if req_method == 'DELETE':
            return requests.delete
        if req_method == 'PUT':
            return requests.put
        return requests.get

    def get_api_response(self, req_method, api_endpoint, data=None):
        url = settings.WALLET_API_URL + api_endpoint
        headers = {
            'X-API-KEY': settings.WALLET_API_KEY
        }
        request_function = self.get_request_function(req_method)
        if data:
            return request_function(url, headers=headers, json=data)
        return request_function(url, headers=headers)

    def get_wallet_status(self):
        return self.get_api_response('GET', '/status')

    def open_wallet(self):
        return self.get_api_response('POST', '/wallet/open', data)

    def create_wallet(self):
        return self.get_api_response('POST', '/wallet/create', data)

    def close_wallet(self):
        return self.get_api_response('DELETE', '/wallet')

    def save_wallet(self):
        return self.get_api_response('PUT', '/save')

    def get_wallet_address(self):
        return self.get_api_response('GET', '/addresses/primary')

    def get_wallet_transactions(self):
        if self.wallet_is_open:
            return self.get_api_response('GET', '/transactions')
