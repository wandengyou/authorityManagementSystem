import requests


def request_api(server, url, method, params):
    url = '{}/{}'.format(server, url)
    try:
        if method == 'get':
            res = requests.get(url, params)
        elif method == 'put':
            res = requests.put(url, params)
        elif method == 'post':
            res = requests.post(url, params)
        elif method == 'delete':
            res = requests.delete(url, data=params)
    except requests.exceptions.RequestException:
        raise
    return res.json()
