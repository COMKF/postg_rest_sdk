try:
    from .RESTSdkException import WrongDataException, WrongRtypeException
except:
    from RESTSdkException import WrongDataException, WrongRtypeException


def build_req_data(data=None):
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

    for key, value in data.items():
        if key == 'select':
            if isinstance(value, str):
                req_data['select'] = value
            elif isinstance(value, (list, tuple)):
                req_data['select'] = ','.join(value)
            else:
                raise WrongDataException('{} data type wrong'.format('select'))

        elif key in ('or', 'and'):
            if isinstance(value, dict):
                l = [k + '.' + transform_value(vv) for k, v in value.items() for vv in v.split('&')]
                req_data[key] = '{}{}{}'.format('(', ','.join(l), ')')
            else:
                raise WrongDataException('{} data type wrong'.format(key))

        elif key == 'order':
            if isinstance(value, str):
                req_data['order'] = value
            elif isinstance(value, (list, tuple)):
                req_data['order'] = ','.join(value)
            elif isinstance(value, dict):
                l = [k + '.' + v for k, v in value.items()]
                req_data['order'] = ','.join(l)
            else:
                raise WrongDataException('{} data type wrong'.format('order'))
        else:
            req_data[key] = transform_value(value)
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
