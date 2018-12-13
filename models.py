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

    def get(self, **kwargs):
        '''
        查询获取数据

        :param kwargs:
        :return:
        '''
        return self.action('get', **kwargs)

    def insert(self, **kwargs):
        '''
        插入数据

        :param kwargs:
        :return:
        '''
        return self.action('insert', **kwargs)

    # def upsert(self, **kwargs):  # 暂不支持
    #     return self.action('upsert', **kwargs)

    def update(self, **kwargs):
        '''
        更新数据

        :param kwargs:
        :return:
        '''
        return self.action('update', **kwargs)

    # def delete(self, **kwargs):
    #     '''
    #     删除数据，禁用
    #
    #     '''
    #     return self.action('delete', **kwargs)

    def action(self, method=None, data=None, json=None, rtype=None, order=None, change_all_table=False):
        headers = dict()
        # 规定了客户端与服务器的数据类型都是json
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        headers['Prefer'] = 'return=representation'

        if method == 'get':
            req_data = build_req_data(data, rtype, order)
            resp = requests.get(self.target, headers=headers, params=req_data, timeout=5)
            return resp

        elif method == 'insert':

            if not json:
                raise Exception('json must be not None at post method')

            resp = requests.post(self.target, headers=headers, json=json, timeout=5)
            return resp

        # elif method == 'upsert':
        #     headers['Prefer'] = 'resolution=merge-duplicates'
        #
        #     if not json:
        #         raise Exception('json must be not None at post method')
        #
        #     print(json)
        #     resp = requests.put(self.target, headers=headers, json=json, timeout=5)
        #     print(resp.status_code)
        #     print(resp.url)
        #     return resp

        elif method == 'update':

            if not (data or change_all_table):
                raise Exception(
                    'data is None,this operating will update the whole table.'
                    'if you want to do, please set the change_all_table is true')

            req_data = build_req_data(data=data, order=order)
            resp = requests.patch(self.target, headers=headers, params=req_data, json=json, timeout=5)
            return resp

        # elif method == 'delete': # 禁用
        #
        #     if not (data or change_all_table):
        #         raise Exception(
        #             'data is None,this operating will update the whole table.'
        #             'if you want to do, please set the change_all_table is true')
        #
        #     req_data = build_req_data(data, rtype, order)
        #     resp = requests.delete(self.target, headers=headers, params=req_data, timeout=5)
        #     print(resp.url)
        #     return resp
