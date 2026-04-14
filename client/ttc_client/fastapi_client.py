import requests


class FastAPIClient:
    """
    Light wrapper around `requests` that uses session and timeouts to avoid
    leaving behind zombie sockets.
    """

    def __init__(self, base_url, timeout=20):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method, endpoint, **kwargs) -> requests.Response:
        """
        Note: may raise `requests.exceptions.Timeout` or `requests.exceptions.RequestException`
        """
        # Automatically inject the default timeout if not specified
        kwargs.setdefault("timeout", self.timeout)
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def get(self, endpoint, params=None, **kwargs) -> requests.Response:
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs) -> requests.Response:
        return self._request("POST", endpoint, data=data, json=json, **kwargs)
