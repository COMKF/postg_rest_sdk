import requests

try:
    from .utils import build_req_data
except:
    from utils import build_req_data


class SqlRequest():

    def __init__(self, DBURL, DBNAME):
        self.DBURL = ('' if 'http://' in DBURL or 'https://' in DBURL else 'http://') + DBURL + (
            '' if DBURL.endswith('/') else '/')
        self.DBNAME = DBNAME.rstrip('/')
        self.target = self.DBURL + self.DBNAME

    def get(self, data=None, **kwargs):
        return self.action('get', data, **kwargs)

    def post(self, data=None, **kwargs):
        return self.action('post', data, **kwargs)

    def delete(self, data=None, **kwargs):
        return self.action('delete', data, **kwargs)

    def patch(self, data=None, **kwargs):
        return self.action('patch', data, **kwargs)

    def action(self, method=None, data=None, rtype=None, order=None):
        headers = dict()
        # 规定了客户端与服务器的数据类型都是json
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'

        if method == 'get':
            req_data = build_req_data(data, rtype, order)
            resp = requests.get(self.target, headers=headers, params=req_data, timeout=5)
            return resp
        elif method == 'post':
            headers['Prefer'] = 'return=representation'
            return requests.post(self.target, headers=headers, json=data, timeout=5)
        elif method == 'delete':
            headers['Prefer'] = 'return=representation'
            req_data = {k: 'eq.' + v for k, v in data.items()}
            return requests.delete(self.target, headers=headers, params=req_data, timeout=5)
        elif method == 'patch':
            return requests.patch(self.target, headers=headers, data=data, timeout=5)
