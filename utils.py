try:
    from .RESTSdkException import WrongDataException, WrongRtypeException
except:
    from RESTSdkException import WrongDataException, WrongRtypeException


def build_req_data(data=None, rtype=None, order=None):
    '''
    构造请求数据

    :param data:
    :param rtype:
    :param order:
    :return:
    '''
    req_data = dict()
    if not data:
        return None

    if rtype in ('default', None):
        if isinstance(data, dict):
            for k, v in data.items():
                req_data[k] = transform_value(v)
        else:
            raise WrongDataException('{} data type wrong'.format(rtype))

    elif rtype in ('or', 'and'):
        if isinstance(data, dict):
            l = [k + '.' + transform_value(vv) for k, v in data.items() for vv in v.split('&')]
            req_data[rtype] = '{}{}{}'.format('(', ','.join(l), ')')
        else:
            raise WrongDataException('{} data type wrong'.format(rtype))

    elif rtype == 'select':
        if isinstance(data, str):
            req_data['select'] = data
        elif isinstance(data, (list, tuple)):
            req_data['select'] = ','.join(data)
        # elif isinstance(data, dict):
        #     l = [k + '.' + self.transform_value(v) for k, v in data.items()]
        #     req_data['select'] = ','.join(l)
        else:
            raise WrongDataException('{} data type wrong'.format(rtype))
    else:
        raise WrongRtypeException('rtype({}) is not allowd'.format(rtype))

    if order:
        if isinstance(order, dict):
            l = [k + '.' + v for k, v in order.items()]
            req_data['order'] = ','.join(l)
        else:
            raise WrongDataException('{} data type wrong'.format('order'))
    return req_data


def transform_value(value_str):
    '''
    对运算符进行转换

    :param value_str:
    :return:
    '''
    v1, v2 = value_str.split(' ')
    if v1 in ('=', 'eq'):
        operator = 'eq.'
    elif v1 in ('>', 'gt'):
        operator = 'gt.'
    elif v1 in ('>=', 'gte'):
        operator = 'gte.'
    elif v1 in ('<', 'lt'):
        operator = 'lt.'
    elif v1 in ('<=', 'lte'):
        operator = 'lte.'
    elif v1 in ('<>', '!=', 'neq'):
        operator = 'neq.'
    elif v1 == 'like':
        operator = 'like.'
    elif v1 == 'ilike':
        operator = 'ilike.'
    elif v1 == 'in':
        operator = 'in.'
    elif v1 == 'is':
        operator = 'is.'
    elif v1 == 'not':
        operator = 'not.'
    elif v1 in ('sl', '<<'):
        operator = '<<.'
    elif v1 in ('sr', '>>'):
        operator = '>>.'
    else:
        raise Exception('wrong operator')
    return operator + v2
