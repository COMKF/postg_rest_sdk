from postg_rest_sdk import SqlRequest

DBURL = 'http://127.0.0.1:3000/'
DBNAME = 'cl'


class T():
    def __init__(self):
        self.sr = None

    def get_sr(self):
        if not self.sr:
            self.sr = SqlRequest(DBURL, DBNAME)
        return self.sr

    def t1(self):
        sr = self.get_sr()
        result = sr.get()
        self.print_result(result)

    def t2(self):
        sr = self.get_sr()
        data = {'glbm': 'like 4103*', 'glbmmc': '= 洛阳市公安局交通管理支队'}
        result = sr.get(data)
        self.print_result(result)

    def t3(self):
        sr = self.get_sr()
        data = {'glbm': 'like 4103*&like 4104*'}
        rtype = 'or'
        result = sr.get(data, rtype=rtype)
        self.print_result(result)

    def t4(self):
        sr = self.get_sr()
        data = ('glbm', 'glbmmc')
        rtype = 'select'
        result = sr.get(data, rtype=rtype)
        self.print_result(result)

    def t5(self):
        sr = self.get_sr()
        data = ('glbm', 'glbmmc')
        rtype = 'select'
        order = {'glbm': 'desc', 'glbmmc': 'desc'}
        result = sr.get(data, rtype=rtype, order=order)
        self.print_result(result)

    def print_result(self, result):
        print('------')
        print(result.text)
        print('------')
        print('------')
        print(result.json())
        print('------')


if __name__ == '__main__':
    t = T()
    t.t1()
    t.t2()
    t.t3()
    t.t4()
    t.t5()

    pass
