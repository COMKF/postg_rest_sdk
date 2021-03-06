import requests
from requests import PreparedRequest

from postg_rest_sdk.RESTSdkException import WrongDataException, WrongJsonException, WrongDataBaseException
from postg_rest_sdk.models import PublicModel
from postg_rest_sdk.utils import build_req_data


class SqlRequest():

    def __init__(self, DBURL, DBNAME):
        self.DBURL = ('' if 'http://' in DBURL or 'https://' in DBURL else 'http://') + DBURL + (
            '' if DBURL.endswith('/') else '/')
        self.DBNAME = DBNAME.rstrip('/')
        self.target = self.DBURL + self.DBNAME
        self.query = None

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

    def action(self, method=None, data=None, json=None, change_all_table=False, return_instance=False):
        headers = dict()
        # 规定了客户端与服务器的数据类型都是json
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        headers['Prefer'] = 'return=representation'

        if method == 'get':
            req_data = build_req_data(data)
            resp = requests.get(self.target, headers=headers, params=req_data, timeout=5)

        elif method == 'insert':

            if not json:
                raise WrongJsonException('json must be not None at post method')

            resp = requests.post(self.target, headers=headers, json=json, timeout=5)

        # elif method == 'upsert':
        #     headers['Prefer'] = 'resolution=merge-duplicates'
        #
        #     if not json:
        #         raise WrongJsonException('json must be not None at post method')
        #
        #     print(json)
        #     resp = requests.put(self.target, headers=headers, json=json, timeout=5)
        #     print(resp.status_code)
        #     print(resp.url)
        #     return resp

        elif method == 'update':

            if not (data or change_all_table):
                raise WrongDataException(
                    'data is None,this operating will update the whole table.'
                    'if you want to do, please set the change_all_table is true')

            req_data = build_req_data(data)
            resp = requests.patch(self.target, headers=headers, params=req_data, json=json, timeout=5)

        # elif method == 'delete': # 禁用
        #
        #     if not (data or change_all_table):
        #         raise WrongDataException(
        #             'data is None,this operating will update the whole table.'
        #             'if you want to do, please set the change_all_table is true')
        #
        #     req_data = build_req_data(data)
        #     resp = requests.delete(self.target, headers=headers, params=req_data, timeout=5)
        #     print(resp.url)
        #     return resp
        else:
            raise WrongDataException(
                'method({}) is not allowed.'.format(method))

        self.query = resp.url

        code = resp.status_code
        if str(code).startswith('2'):
            response_data = resp.json()
            if return_instance and len(response_data) >= 1:
                instance_dict = response_data[0]
                instance = PublicModel(instance_dict)
                return instance
            else:
                return response_data
        else:
            raise WrongDataBaseException(resp.text)

    def get_query(self, data=None):
        p = PreparedRequest()
        req_data = build_req_data(data)
        p.prepare_url(self.target, req_data)  # 该方法只是其中一个方法，这个方法就是专门拼接params与url的，生成 EncodeUrl。
        self.query = p.url
        return self.query
