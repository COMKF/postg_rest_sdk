from postg_rest_sdk import SqlRequest

DBURL = 'http://118.89.236.99:3001/'
DBNAME = 'alipay_OpenUser'


class T():
    def __init__(self):
        self.sr = None

    def get_sr(self):
        if not self.sr:
            self.sr = SqlRequest(DBURL, DBNAME)
        return self.sr

    def t1(self):
        '''
        获取全表数据，不建议使用

        :return:
        '''
        sr = self.get_sr()
        result = sr.get()
        self.print_result(result)

    def t2(self):
        '''
        行查询，rtype 关键字 default

        :return:
        '''
        sr = self.get_sr()
        data = {'alipay_user_id': '= 2088102169075850'}
        result = sr.get(data=data)
        self.print_result(result)

    def t21(self):
        '''
        行查询，rtype 关键字 default

        :return:
        '''
        sr = self.get_sr()
        data = {'alipay_user_id': '= 2088102169075850'}
        result = sr.get_instance(data=data)
        self.print_result(result)

    def t3(self):
        '''
        行查询，rtype 关键字 or

        :return:
        '''
        sr = self.get_sr()
        data = {'glbm': 'like 4103*&like 4104*'}
        rtype = 'or'
        result = sr.get(data=data, rtype=rtype)
        self.print_result(result)

    def t4(self):
        '''
        列查询，rtype 关键字 select

        :return:
        '''
        sr = self.get_sr()
        data = ('glbm', 'glbmmc')
        rtype = 'select'
        result = sr.get(data=data, rtype=rtype)
        self.print_result(result)

    def t5(self):
        '''
        排序，order

        :return:
        '''
        sr = self.get_sr()
        data = ('glbm', 'glbmmc')
        rtype = 'select'
        order = {'glbm': 'desc', 'glbmmc': 'desc'}
        result = sr.get(data=data, rtype=rtype, order=order)
        self.print_result(result)

    def t6(self):
        '''
        插人

        :return:
        '''
        sr = self.get_sr()
        json = dict(glbm='00', zsdwnm='11', glbmmc='22')  # 单个
        # json = dict(glbm='01')  # 未赋值的属性将会被置为默认值
        json = [dict(glbm='55', zsdwnm='11', glbmmc='22'), dict(glbm='66', zsdwnm='11', glbmmc='22')]  # 批量插入
        # json = None
        result = sr.insert(json=json)
        self.print_result(result)

    # def t7(self):
    #     '''
    #     插人或更新
    #
    #     :return:
    #     '''
    #     sr = self.get_sr()
    #     data = dict(glbm='00', zsdwnm='11', glbmmc='22')  # 单个
    #     result = sr.upsert(json=data)
    #     self.print_result(result)

    def t8(self):
        '''
        更新

        :return:
        '''
        sr = self.get_sr()
        data = dict(alipay_user_id='= 2088102169075850')  # 查询条件
        json = dict(name='叶孟豪', id_card='411330199405223118', phone='18338216907')  # 更新数据
        result = sr.update(data=data, json=json)
        self.print_result(result)

    # def t9(self):
    #     '''
    #     删除
    #
    #     :return:
    #     '''
    #     sr = self.get_sr()
    #     data = dict(glbm='= 55')
    #     result = sr.delete(data=data)
    #     self.print_result(result)

    def print_result(self, result):
        print('------')
        print(result)
        print('------')


if __name__ == '__main__':
    t = T()
    # t.t1()
    # t.t2()
    t.t21()
    # t.t3()
    # t.t4()
    # t.t5()
    # t.t6()
    # t.t7()
    # t.t8()
    # t.t9()
    pass
