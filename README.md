## PostgREST-SDK

### github地址：
* [PostgREST-SDK](https://github.com/COMKF/postg_rest_sdk)


### 相关资料：
* [PostgREST官方文档](http://postgrest.org/en/stable/index.html)
* [PostgREST-API中文翻译对照](http://note.youdao.com/noteshare?id=d9ebb39ad8084901e7c04fb329ac3535)

### 使用说明
该SDK针对官方API进行了封装，简化了url后面附带的查询条件，使用者可以把更多的精力放在python代码的编写上。

### 查询（方法为get）
PostgREST示例url地址为：http://127.0.0.1:3000/   
PostgREST示例数据库表为：cl

根据官方文档，PostgREST最大的特点是它将查询分为行查询和列查询：（以下是个人理解）

* 行查询：通过对数值的判断，对数据进行过滤，但是必须查全表
* 列查询：只查询某一些列，而不需要查全表，还可以进行外键关联查询，无法对数据进行条件过滤
* 单表混合查询
* 多表联合查询，待定

#### 简单查询  

根据上面这个规则，以及现有的官方文档，PostgREST-SDK制定了以下规则：  

* data为查询条件，data类型为None时，代表查全表，示例如下：

      DBURL = 'http://127.0.0.1:3000/'
      DBNAME = 'cl'
      
      if __name__ == '__main__':
        from postg_rest_sdk import SqlRequest
        # 构建
        sr = SqlRequest(DBURL, DBNAME)
        result = sr.get()
        
    结果如下：
    
        [{"glbm":"4101","glbmmc":"郑州","zsdwnm":"0"}, 
        {"glbm":"4101","glbmmc":"二大队","zsdwnm":"05"}, 
        {"glbm":"4101","glbmmc":"三大队","zsdwnm":"0"}]

* data为dict类型时，为条件查询，遵循以下规则：
    * 当data的其中一个键值对的键为select时，它的值类型必须为str、list、tuple，示例如下：
    
          data['select'] = ('glbm', 'glbmmc')
          result = sr.get(data=data)

      结果如下：
      
            [{"glbm":"4101","glbmmc":"郑州"}, 
             {"glbm":"4101","glbmmc":"二队"}, 
             {"glbm":"4101","glbmmc":"三队"}]
             
        注意：select只做列查询，至于能否执行过滤条件，需要待定。
    
    * 当data的其中一个键值对的键为or或者and时，它的值类型必须为dict，示例如下：
        
          data['or'] = {'glbm': 'like 4103*&like 4104*'}
          result = sr.get(data=data)
          
        结果如下：
            
            [{"glbm":"410300","glbmmc":"洛阳","zsdwnm":"0"},
            {"glbm":"4103","glbmmc":"洛阳","zsdwnm":"0"}, 
            {"glbm":"4103","glbmmc":"轻工队","zsdwnm":"0"},
            {"glbm":"410439","glbmmc":"姚队","zsdwnm":"000"}]
        
        注意：data必须是dict，当需要为一个字段做多个条件查询时，每个条件通过&连接，&连接符前后不能有空格。
    
    * 排序的关键字是order，当data的其中一个键值对的键为order时，它的值类型支持str、list、tuple、dict，示例如下：  
    
          data['order'] = 'glbm.desc'
          data['order'] = ['glbm.desc', 'glbmmc']
          data['order'] = {'glbm': 'desc', 'glbmmc': 'asc'}
          result = sr.get(data=data)
    
        结果如下：
        
            [{"glbm":"410","glbmmc":"焦作"}, 
            {"glbm":"410","glbmmc":"焦作"}, 
            {"glbm":"410","glbmmc":"焦作"}]
        
        注意：order如果是一个dict，键为字段，值为 desc 或 asc。
        
    * 当data的键值对不属于以上关键字，则它的键必须是表中的字段，值必须是字符串，示例如下：
    
          data = {'glbm': 'like 4103*', 'glbmmc': '= 洛阳市'}
          result = sr.get(data=data) 
          
      结果如下：
            
          [{'glbm': '410300', 'glbmmc': '洛阳市', 'zsdwnm': '000'}]  
          
      注意：这一部分的键可以有多个，而且键必须是表中的字段，表字段查询为行查询；值分为两部分，第一部分是运算符，第二部分是数值，可使用的运算符见[PostgREST-API中文翻译对照](http://note.youdao.com/noteshare?id=d9ebb39ad8084901e7c04fb329ac3535)，数值可以使用*作为通配符，运算符和数值之间必须有一个空格。
      
#### 单表混合查询  

单表混合查询是单表简单查询的复合使用，以上关键字（select、or、and、order、表字段）是同级的，可以共同作为data的参数，进行混合查询。

### 复杂查询

* 能否把简单查询进行混合，待定
* 支持创建视图，创建后可自动生成url访问端点
* 支持过程函数


### 插入数据（方法为insert）
根据官方文档，新增json字段，作为传数据的字段。插入数据时，主键和不为Null的字段为必传字段，需要放在json字段中，而未赋值的字段将会被置为默认值。
* 单条数据插入，示例如下：
        
      json = dict(glbm='00', zsdwnm='11', glbmmc='22')  # 单个
      result = sr.insert(json=json)

    结果如下：
    
        [{'glbm': '00', 'glbmmc': '22', 'zsdwnm': '11'}]
    
    注意：单条数据插入的时候，json是一个dict。
    
* 批量插入，示例如下：

      json = [dict(glbm='55', zsdwnm='11', glbmmc='22'), dict(glbm='66', zsdwnm='11', glbmmc='22')]  # 批量插入
      result = sr.insert(json=json)

    结果如下：
    
      [{"glbm":"55","glbmmc":"22","zsdwnm":"11"}, 
      {"glbm":"66","glbmmc":"22","zsdwnm":"11"}]
    
    注意：批量插入的时候，json是一个包含多个dict的list。

### 修改数据（方法为update）
如上所示，data字段为查询条件，json字段为数据字段。当我们需要进行update的时候，建议data不为空，如果data为空，则将会更新表中所有的字段值；为防止这种情况发生，sdk加入change_all_table字段，只有该字段为True时，才允许更新表中所有的字段值。

* 示例代码：
        
      data = dict(glbm='= 00')  # 查询条件
      json = dict(zsdwnm='1243124', glbmmc='12421342345')  # 更新数据
      result = sr.update(data=data, json=json)

    结果如下：
    
        [{"glbm":"00","glbmmc":"12421342345","zsdwnm":"1243124"}]

    
* 强行更新表中所有字段值的方法：

      json = dict(zsdwnm='1243124', glbmmc='12421342345')  # 更新数据
      result = sr.update(json=json, change_all_table=True)
    
### 删除数据（方法为delete）
sdk禁用该方法


## 特殊：获取实例

当需要获取一条具体的实例数据，而不是一个list的时候，可以加上return_instance参数并将其赋值为True，示例如下:

    data = {'glbm': 'like 4103*', 'glbmmc': '= 洛阳市'}
    result = sr.get(data=data,return_instance=True) 
  
结果如下：

    {'glbm': '410300', 'glbmmc': '洛阳市', 'zsdwnm': '000'}
  
注意：
* 若get方法获取到了多个数据，会取第一个数据构造实例。
* 该实例支持.运算符，即可以通过 result.glbm 取得410300这个值。

## 特殊：获取查询url
通过 get_query 方法和 query 属性，可以获得构造的 PostgREST 的url，方便大家学习，示例如下：

    data = {'xzqh': '= 4103'}
    sr.get_query(data)
    sr.query
    result = sr.get(data=data)
    sr.query
    
结果如下：

    http://118.89.236.99:3000/xzqh_status?xzqh=eq.4103

注意：
* get_query方法需要传入参数data（查询条件）。
* 每次使用 get_query 或其他方法后，都会保存查询url为query属性值，方便下次直接使用。

### 更新日志

* 2018-12-12 初版
* 2018-12-13 增加插入数据、更新数据方法
* 2018-12-26 更新查询方法，更新test示例，更新获取实例和PostgREST的url的方法
