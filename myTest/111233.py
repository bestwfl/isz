# -*- coding:utf8 -*-

from base import get_date, get_random_phone
from request import Request
from validator import Validator
from base import get_conf
import json
import time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class Run_test():
    def __init__(self, mysql, session, **kwargs):
        self.mysql = mysql
        self.session = session
        if kwargs.get('ids'):
            self.ids = kwargs['ids']
        if kwargs.get('url'):
            self.host = kwargs['host']
            self.url = kwargs['url']
            self.content_type = kwargs['content_type']
            self.user_agent = kwargs['user_agent']
            self.data = kwargs['data']
            self.method = kwargs['method'].lower()
            self.debug = kwargs['debug']
        if kwargs.get('type'):
            self.type = kwargs['type']
            self.id = kwargs['id']
        else:
            self.type = None

    def get_sql_result(self, sql, index):
        """
        根据指定sql，返回查询结果
        :param sql: 查询sql，不支持参数化
        :param index: 返回结果为list，需指定目标index
        :return:
        """
        try:
            for key, value in (self.mysql.select(sql)[0]).items():
                return (True, value)
        except Exception, e:
            logger.exception('Excetion')
            return (False, e)

    def get_layers_value(self, layer_relation, original_value):
        """
        根据链式规则，获取指定值
        :param layer_relation: 链式规则，以 . 为连接
        :param original_value: 做匹配的原始数据
        :return: 匹配完链式规则后的值
        """

        def type_convert(value):
            """
            检查是否为数字，如'obj.0'中的0，是的话则当list的index使用，不是则作dict的key使用
            :param value: 需要校验的值
            :return: 转换成int或者str返回
            """
            return int(value) if value.isdigit() else value

        if not isinstance(original_value, dict):
            original_value = json.loads(original_value)
        match_before = layer_relation.split('.')
        match_after = None
        for index in range(len(match_before)):
            # 需要多级获取的时候，先从原始数据中获取第一级为match_after，后面的数据再从match_after中获取
            # 请求响应code为非0时，会触发KeyError
            if match_after:
                try:
                    match_after = match_after[type_convert(match_before[index])]
                except KeyError:
                    return False
            else:
                try:
                    match_after = original_value[type_convert(match_before[index])]
                except KeyError:
                    return False
        return match_after

    def validator(self, validators):
        """
        根据传入的校验规则执行指定的校验器
        :param interface_id: 待执行的接口ID
        :return: 校验器的返回结果
        """
        # interface_info = \
        # self.mysql.select("SELECT * FROM test_interface WHERE interface_id = %s AND deleted = 0", interface_id)[0]
        # validators = validator_convert(interface_info['assert'], response_data)
        if not validators:
            return False
        results = []
        # 使用list不可被hash的特性，来判断是否有多个校验规则
        try:
            set(validators)
        except:
            for case in validators:
                check, method, expect = str(case[0]), str(case[1]), str(case[2])
                validator = Validator()
                if hasattr(validator, method):
                    result = getattr(validator, method)(check, expect)
                    results.append(result)
                else:
                    m_assert = 'expect %s %s %s' % (check, method, expect)
                    results.append({'assert': m_assert, 'result': 'not found function: ' + method})
        else:
            check, method, expect = str(validators[0]), str(validators[1]), str(validators[2])
            validator = Validate()
            if hasattr(validator, method):
                result = getattr(validator, method)(check, expect)
                results.append(result)
            else:
                m_assert = 'expect %s %s %s' % (check, method, expect)
                results.append({'assert': m_assert, 'result': 'not found function：%s' % method})
        finally:
            return results

    def validator_convert(self, validatorStr, response):
        """
        拆分接口返回值(字符串)并调用对应的校验方法
        :param validatorStr: 包含实际结果、预期结果、校验方法的字符串
        :param response:接口返回的值(校验的实际结果从此处匹配)
        :return:返回转换后的校验列表
        """
        if not isinstance(response, dict):
            response = json.loads(response)
        validators = []
        for x in validatorStr.split('\n'):
            # 如果有多行校验，中间不允许有空行，否则视为空行以后的校验无效不做验证
            if x == '':
                break
            # 处理掉前后不小心输入的空格以及处理校验的字符串
            x = x.strip()
            y = x.split('--')
            # 如果包含 select 则视为sql
            if '@select' in y[0]:
                y[0] = self.mysql.select(y[0][1:], type='list')[0][0]
            # 如果是多级，则链式调用
            if len(y[0].split('.')) > 1:
                check_value = self.get_layers_value(y[2], response) if y[1] == 'in' else self.get_layers_value(y[0], response)
            else:
                if y[1] == 'in':
                    check_value = response[y[2]]
                elif '@select' in x:
                    check_value = y[0]
                else:
                    check_value = response[y[0]]
            # check_value = self.get_layers_value(y[0], response) if len(y[0].split('.')) > 1 else response[y[0]]
            if check_value != 0 and not check_value:
                return False
            # 校验方式为 in 的时候， 需要调换位置并改变方法名称为 contains
            y[1] = 'contains' if y[1] == 'in' else y[1]
            if y[1] == 'contains':
                validators.append([y[0], y[1], check_value])
            else:
                validators.append([check_value, y[1], y[2]])
        return validators

    def interface_convert(self, value):
        """老方案下的转换，分别获取接口信息和执行sql语句"""
        for k, v in value.items():
            if "$" in v:
                interface = self.mysql.select("SELECT * FROM test_interface WHERE interface_id = %s",
                                              re.findall('\$(.*?)\(', v))
                data = {}
                params = re.findall("\((.*?)\)", v)[0]
                for p in params.split(','):
                    param = p.split(':')
                    if '@' in param[1]:
                        sql = param[1][1:]
                        for ke, va in self.mysql.select(sql)[0].items():
                            data[param[0]] = va
                    else:
                        data[param[0]] = param[1]

    def params_convert(self, params):
        """
        处理请求参数中的接口执行、数据库查询、日期处理
        :param params: 需要解析的接口参数
        :return: 计算或执行之后的接口参数值
        """

        def recursion_get_type(data):
            data = data if isinstance(data, dict) else json.loads(data)
            if isinstance(data, dict):
                for key, value in data.items():
                    if type(value) is dict:
                        if 'type' in value and value['type'] in ['interface','db','date','random_phone']:
                            types = value['type']
                            # type为interface时，递归调用当前函数
                            if types == 'interface':
                                # 获取拓展字典中的interface_id，得到接口信息
                                info = self.mysql.select(
                                    "select host, url, method_type, data, content_type, user_agent, assert from test_interface WHERE interface_id = %s",
                                    value['id'])[0]
                                # 如果调用其他接口的时候，传有参数，那就使用传参，如果没有，就用数据库中存的参数
                                if 'data' in value:
                                    info['data'] = value['data']
                                # 传入拓展字典中的接口参数，递归当前函数
                                if info['method_type'] != 'GET':
                                    request_data = recursion_get_type(info['data'])
                                else:
                                    request_data = {}
                                    request_data['data'] = info['data']
                                # 执行拓展字典中的接口
                                # cookies = self.session['info']['cookie'] if info['host'] != 'http://spider-app.ishangzu.com' else self.session['info']['spider_cookie']
                                if '@sql' in info['url']:
                                    param = self.mysql.select(request_data['data'], type='list')
                                    if not param:
                                        return False
                                    url_split = info['url'].split('@sql')
                                    info['url'] = url_split[0] + str(param[0][0]) + url_split[1] if len(url_split) > 1 else \
                                    url_split[0] + param[0][0]
                                req = Request(info['host'], info['url'], request_data, self.session,
                                              content_type=info['content_type'], user_agent=info['user_agent'])
                                response_data = getattr(req, info['method_type'].lower())()['response']
                                # 校验拓展字典中的接口返回值
                                validatorts = self.validator_convert(info['assert'], response_data)
                                # validation = validator(value['id'], request_data, response_data, self.mysql)
                                validator_result = self.validator(validatorts)
                                # 接口响应失败(code_status非200、code非0)时，会返回False，此处也返回
                                if not validator_result:
                                    return False
                                # 根据链式规则获取指定数据并赋值修改params
                                if 'wait' in value:
                                    time.sleep(int(value['wait']))
                                match_value = self.get_layers_value(value['match'], response_data)
                                data[key] = match_value
                                # 接口响应失败(code_status非200、code非0)时，会匹配失败并返回False，此处也返回
                                if not match_value:
                                    return False
                            # type为db时，调用数据库方法
                            elif types == 'db':
                                if value['db'] not in get_conf(self.session['info']['host'], 'db').split(','):
                                    return '参数中包含错误的数据库名: %s' % value['db']
                                db_result = self.mysql.select(value['sql'], type='list', db=value['db'])
                                if not db_result:
                                    return 'sql返回结果为空，请检查sql语句'
                                data[key] = db_result[0][0]
                            # type为date时，调用内置日期函数
                            elif types == 'date':
                                result = get_date(value['method'], value['param']) if value.get('param') else get_date(
                                    value['method'])
                                if result.contains:
                                    data[key] = result.result
                                else:
                                    return result.result
                            elif types == 'random_phone':
                                data[key] = get_random_phone()
                        else:
                            recursion_get_type(value)
                    elif type(value) is list:
                        for v in value:
                            if 'type' in v and v['type'] in ['interface', 'db', 'date', 'random_phone']:
                                types = v['type']
                                # type为interface时，递归调用当前函数
                                if types == 'interface':
                                    # 获取拓展字典中的interface_id，得到接口信息
                                    info = self.mysql.select(
                                        "select host, url, method_type, data, content_type, user_agent, assert from test_interface WHERE interface_id = %s",
                                        v['id'])[0]
                                    # 如果调用其他接口的时候，传有参数，那就使用传参，如果没有，就用数据库中存的参数
                                    if 'data' in v:
                                        info['data'] = v['data']
                                    # 传入拓展字典中的接口参数，递归当前函数
                                    request_data = recursion_get_type(info['data'])
                                    # 执行拓展字典中的接口
                                    # cookies = self.session['info']['cookie'] if info['host'] != 'http://spider-app.ishangzu.com' else self.session['info']['spider_cookie']
                                    if '@sql' in info['url']:
                                        param = self.mysql.select(request_data['data'], type='list')
                                        if not param:
                                            return False
                                        url_split = info['url'].split('@sql')
                                        info['url'] = url_split[0] + str(param[0][0]) + url_split[1] if len(
                                            url_split) > 1 else \
                                            url_split[0] + param[0][0]
                                    req = Request(info['host'], info['url'], request_data, self.session,
                                                  content_type=info['content_type'], user_agent=info['user_agent'])
                                    response_data = getattr(req, info['method_type'].lower())()['response']
                                    # 校验拓展字典中的接口返回值
                                    validatorts = self.validator_convert(info['assert'], response_data)
                                    # validation = validator(value['id'], request_data, response_data, self.mysql)
                                    validator_result = self.validator(validatorts)
                                    # 接口响应失败(code_status非200、code非0)时，会返回False，此处也返回
                                    if not validator_result:
                                        return False
                                    # 根据链式规则获取指定数据并赋值修改params
                                    if 'wait' in v:
                                        time.sleep(int(v['wait']))
                                    match_value = self.get_layers_value(v['match'], response_data)
                                    data[key] = match_value
                                    # 接口响应失败(code_status非200、code非0)时，会匹配失败并返回False，此处也返回
                                    if not match_value:
                                        return False
                                # type为db时，调用数据库方法
                                elif types == 'db':
                                    if v['db'] not in get_conf(self.session['info']['host'], 'db').split(','):
                                        return '参数中包含错误的数据库名: %s' % v['db']
                                    db_result = self.mysql.select(v['sql'], type='list', db=v['db'])
                                    if not db_result:
                                        return 'sql返回结果为空，请检查sql语句'
                                    data[key] = db_result
                                    x = []
                                    for i in range(len(data[key])):
                                        x.append(data[key][i][0])
                                    data[key] = x
                                # type为date时，调用内置日期函数
                                elif types == 'date':
                                    result = get_date(v['method'], v['param']) if v.get(
                                        'param') else get_date(
                                        v['method'])
                                    if result.contains:
                                        data[key] = result.result
                                    else:
                                        return result.result
                                elif types == 'random_phone':
                                    data[key] = get_random_phone()
                            else:
                                recursion_get_type(v)
            else:
                data = data if isinstance(data, list) else json.loads(data)
                if isinstance(data,(list, unicode)):
                    for i in range(len(data)):
                        for key, value in data[i].items():
                            if type(value) is dict:
                                if 'type' in value and value['type'] in ['interface', 'db', 'date', 'random_phone']:
                                    types = value['type']
                                    # type为interface时，递归调用当前函数
                                    if types == 'interface':
                                        # 获取拓展字典中的interface_id，得到接口信息
                                        info = self.mysql.select(
                                            "select host, url, method_type, data, content_type, user_agent, assert from test_interface WHERE interface_id = %s",
                                            value['id'])[0]
                                        # 如果调用其他接口的时候，传有参数，那就使用传参，如果没有，就用数据库中存的参数
                                        if 'data' in value:
                                            info['data'] = value['data']
                                        # 传入拓展字典中的接口参数，递归当前函数
                                        request_data = recursion_get_type(info['data'])
                                        # 执行拓展字典中的接口
                                        # cookies = self.session['info']['cookie'] if info['host'] != 'http://spider-app.ishangzu.com' else self.session['info']['spider_cookie']
                                        if '@sql' in info['url']:
                                            param = self.mysql.select(request_data['data'], type='list')
                                            if not param:
                                                return False
                                            url_split = info['url'].split('@sql')
                                            info['url'] = url_split[0] + str(param[0][0]) + url_split[1] if len(
                                                url_split) > 1 else \
                                                url_split[0] + param[0][0]
                                        req = Request(info['host'], info['url'], request_data, self.session,
                                                      content_type=info['content_type'], user_agent=info['user_agent'])
                                        response_data = getattr(req, info['method_type'].lower())()['response']
                                        # 校验拓展字典中的接口返回值
                                        validatorts = self.validator_convert(info['assert'], response_data)
                                        # validation = validator(value['id'], request_data, response_data, self.mysql)
                                        validator_result = self.validator(validatorts)
                                        # 接口响应失败(code_status非200、code非0)时，会返回False，此处也返回
                                        if not validator_result:
                                            return False
                                        # 根据链式规则获取指定数据并赋值修改params
                                        if 'wait' in value:
                                            time.sleep(int(value['wait']))
                                        match_value = self.get_layers_value(value['match'], response_data)
                                        data[key] = match_value
                                        # 接口响应失败(code_status非200、code非0)时，会匹配失败并返回False，此处也返回
                                        if not match_value:
                                            return False
                                    # type为db时，调用数据库方法
                                    elif types == 'db':
                                        if value['db'] not in get_conf(self.session['info']['host'], 'db').split(','):
                                            return '参数中包含错误的数据库名: %s' % value['db']
                                        db_result = self.mysql.select(value['sql'], type='list', db=value['db'])
                                        if not db_result:
                                            return 'sql返回结果为空，请检查sql语句'
                                        data[key] = db_result[0][0]
                                    # type为date时，调用内置日期函数
                                    elif types == 'date':
                                        result = get_date(value['method'], value['param']) if value.get('param') else get_date(
                                            value['method'])
                                        if result.contains:
                                            data[i][key] = result.result
                                        else:
                                            return result.result
                                    elif types == 'random_phone':
                                        data[i][key] = get_random_phone()
                                else:
                                    recursion_get_type(value)
                            elif type(value) is list:
                                for v in value:
                                    recursion_get_type(v)
            return data

        return recursion_get_type(params)

    def params_convert_back(self, params):
        """
        处理请求参数中的接口执行、数据库查询、日期处理
        :param params: 需要解析的接口参数
        :return: 计算或执行之后的接口参数值
        """

        def recursion_get_type(data):
            data = data if isinstance(data, dict) else json.loads(data)
            for key, value in data.items():
                if type(value) is dict:
                    if 'type' in value:
                        types = value['type']
                        # type为interface时，递归调用当前函数
                        if types == 'interface':
                            # 获取拓展字典中的interface_id，得到接口信息
                            info = self.mysql.select(
                                "select host, url, method_type, data, content_type, user_agent, assert from test_interface WHERE interface_id = %s",
                                value['id'])[0]
                            # 如果调用其他接口的时候，传有参数，那就使用传参，如果没有，就用数据库中存的参数
                            if 'data' in value:
                                info['data'] = value['data']
                            # 传入拓展字典中的接口参数，递归当前函数
                            request_data = recursion_get_type(info['data'])
                            # 执行拓展字典中的接口
                            # cookies = self.session['info']['cookie'] if info['host'] != 'http://spider-app.ishangzu.com' else self.session['info']['spider_cookie']
                            if '@sql' in info['url']:
                                param = self.mysql.select(request_data['data'], type='list')
                                if not param:
                                    return False
                                url_split = info['url'].split('@sql')
                                info['url'] = url_split[0] + str(param[0][0]) + url_split[1] if len(url_split) > 1 else url_split[0] + param[0][0]
                            req = Request(info['host'], info['url'], request_data, self.session,
                                          content_type=info['content_type'], user_agent=info['user_agent'])
                            response_data = getattr(req, info['method_type'].lower())()['response']
                            # 校验拓展字典中的接口返回值
                            validatorts = self.validator_convert(info['assert'], response_data)
                            # validation = validator(value['id'], request_data, response_data, self.mysql)
                            validator_result = self.validator(validatorts)
                            # 接口响应失败(code_status非200、code非0)时，会返回False，此处也返回
                            if not validator_result:
                                return False
                            # 根据链式规则获取指定数据并赋值修改params
                            if 'wait' in value:
                                time.sleep(int(value['wait']))
                            match_value = self.get_layers_value(value['match'], response_data)
                            data[key] = match_value
                            # 接口响应失败(code_status非200、code非0)时，会匹配失败并返回False，此处也返回
                            if not match_value:
                                return False
                        # type为db时，调用数据库方法
                        elif types == 'db':
                            if value['db'] not in get_conf(self.session['info']['host'], 'db').split(','):
                                return '参数中包含错误的数据库名: %s' % value['db']
                            db_result = self.mysql.select(value['sql'], type='list', db=value['db'])
                            if not db_result:
                                return 'sql返回结果为空，请检查sql语句'
                            data[key] = db_result[0][0]
                        # type为date时，调用内置日期函数
                        elif types == 'date':
                            result = get_date(value['method'], value['param']) if value.get('param') else get_date(
                                value['method'])
                            if result.contains:
                                data[key] = result.result
                            else:
                                return result.result
                        elif types == 'random_phone':
                            data[key] = get_random_phone()
                elif type(value) is list or type(value) is unicode:
                    for v in value:
                        recursion_get_type(v)
            return data

        return recursion_get_type(params)

    # def jont_url(self, url, join_url_sql, return_bool=False):
    #     if '@sql' in url:
    #         param = self.mysql.select(join_url_sql, type='list')
    #         if not param:
    #             return (-1, 'url中的占位符处的sql返回结果为空，请检查sql') if not return_bool else False
    #         url_split = data['url'].split('@sql')
    #         return url_split[0] + param[0][0] + url_split[1] if len(url_split)>2 else url_split[0] + param[0][0]

    # def debug_request(self, host, url, data, cookies, content_type, method, user_agent):
    #     if method == 'POST':
    #         data = data if isinstance(data, dict) else json.loads(data)
    #     response = request(host, url, data, cookies, content_type, method, user_agent)
    #     return {
    #         'status_code': response['status_code'],
    #         'm_code': response['m_code'],
    #         'duration': response['duration'],
    #         'response': response['response']
    #     }

    def run_test(self):
        from datetimes import nowTime
        create_time = nowTime()
        log_id = ''
        # 如果为项目/模块，则先在log主表插入记录，记录创建时间，然后根据创建时间将log主表ID更新至detail表
        if self.type:
            if self.type == 'project':
                sql = "insert into test_execute_log (project_id, module_id, result, create_time, create_uid) values (%s, null, null, %s, %s)"
                self.mysql.update_or_insert(sql, (self.id, create_time, self.session['info']['uid']))
            else:
                sql = "insert into test_execute_log (project_id, module_id, result, create_time, create_uid) values (null, %s, null, %s, %s)"
                self.mysql.update_or_insert(sql, (self.id, create_time, self.session['info']['uid']))
            log_id = self.mysql.select("select log_id from test_execute_log where create_time = %s", create_time)[0][
                'log_id']
        # 如果没传ids，则走调试通道，仅仅调用http请求，然后返回响应
        if not hasattr(self, 'ids'):
            # cookies = self.session['info']['cookie'] if self.host != 'http://spider-app.ishangzu.com' else self.session['info']['spider_cookie']
            if '@sql' in self.url:
                param = self.mysql.select(self.data, type='list')
                if not param:
                    return 'url中的占位符处的sql返回结果为空，请检查sql'
                url_split = self.url.split('@sql')
                self.url = url_split[0] + str(param[0][0]) + url_split[1] if len(url_split) > 1 else url_split[0] + param[0][0]
            req = Request(self.host, self.url, self.data, self.session, content_type=self.content_type,
                          user_agent=self.user_agent)
            return getattr(req, self.method)()
            # return self.debug_request(self.host, self.url, self.data, cookie, self.content_type, self.method, self.user_agent)

        result_list = []
        for id in self.ids:
            interface_info = self.mysql.select(
                "select host, url, method_type, data, content_type, user_agent, assert from test_interface WHERE interface_id = %s",
                id, type='list')[0]
            host, url, method, data, content_type, user_agent, validator_str = interface_info
            method = method.lower()
            # cookies = self.session['info']['cookie'] if host != 'http://spider-app.ishangzu.com' else self.session['info']['spider_cookie']
            # 非POST请求，参数为空，则不调用参数转换
            if data == '' or ('select' in data and '"type"' not in data):
                data_convert_after = None
            else:
                data_convert_after = self.params_convert(data)
            # data_convert_after = self.params_convert(data) if data != '' else None
            # 如果转换请求参数的过程中出现问题，会返回具体错误信息，同时记录数据库并结束当前接口的执行。数据库中status_code为-1时，为程序自身错误，关注result
            if isinstance(data_convert_after, (str, unicode)):
                if self.type:
                    sql = "insert into test_execute_log_detail (log_id, interface_id, request_data, response_data, status_code, m_code, duration, result, assert_result, create_uid, create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    self.mysql.update_or_insert(sql, (log_id, id, data, '', -1, -1, 0, data_convert_after, 'Fail', self.session['info']['uid'],nowTime()))
                else:
                    # 如果转换过程中出现错误，且是debug模式时，直接将信息返回，否则记录至数据库后再返回
                    if hasattr(self, 'debug'):
                        return data_convert_after
                    sql = "insert into test_execute_log_detail (log_id, interface_id, request_data, response_data, status_code, m_code, duration, result, assert_result, create_uid, create_time) VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    self.mysql.update_or_insert(sql, (
                    id, data, '', -1, -1, 0, data_convert_after, 'Fail', self.session['info']['uid'], nowTime()))
                    return data_convert_after
                result_list.append('Fail')
            data = data_convert_after if isinstance(data_convert_after, (dict,list)) else data
            if '@sql' in url:
                param = self.mysql.select(data, type='list')
                if not param:
                    return 'url中的占位符处的sql返回结果为空，请检查sql'
                url_split = url.split('@sql')
                url = url_split[0] + str(param[0][0]) + url_split[1] if len(url_split) > 1 else url_split[0] + param[0][0]
            if hasattr(self, 'debug'):
                req = Request(host, url, data, self.session, content_type=content_type, user_agent=user_agent, debug=True)
                return getattr(req, method)()
                # return self.debug_request(host, url, data_convert_after, cookies, content_type, method, user_agent)
            req = Request(host, url, data, self.session, content_type=content_type, user_agent=user_agent)
            res = getattr(req, method)()
            if res['result']:
                validators = self.validator_convert(validator_str, json.loads(res['response']))
                results = self.validator(validators)
                assert_result = None
                for result in results:
                    if result['result'] is True:
                        assert_result = 'Pass'
                    else:
                        assert_result = 'Fail'
                        break
                result_list.append(assert_result)
                if self.type:
                    sql = "insert into test_execute_log_detail (log_id, interface_id, request_data, response_data, status_code, m_code, duration, result, assert_result, create_uid, create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    self.mysql.update_or_insert(sql, (
                    log_id, id, json.dumps(data_convert_after).decode('unicode-escape'), res['response'],
                    res['status_code'],
                    res['m_code'], res['duration'], str(results), assert_result, self.session['info']['uid'],
                    res['execute_time']))
                else:
                    sql = "insert into test_execute_log_detail (log_id, interface_id, request_data, response_data, status_code, m_code, duration, result, assert_result, create_uid, create_time) VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    self.mysql.update_or_insert(sql, (
                    id, json.dumps(data_convert_after).decode('unicode-escape'), res['response'],
                    res['status_code'], res['m_code'], res['duration'], str(results), assert_result,
                    self.session['info']['uid'], res['execute_time']))
            else:
                result_list.append('Fail')
                if self.type:
                    sql = "insert into test_execute_log_detail (log_id, interface_id, request_data, response_data, status_code, m_code, duration, result, assert_result, create_uid, create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    self.mysql.update_or_insert(sql, (
                    log_id, id, json.dumps(data_convert_after).decode('unicode-escape'), res['response'],
                    res['status_code'], res['m_code'], res['duration'], '', 'Fail', self.session['info']['uid'],
                    res['execute_time']))
                else:
                    sql = "insert into test_execute_log_detail (log_id, interface_id, request_data, response_data, status_code, m_code, duration, result, assert_result, create_uid, create_time) VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    self.mysql.update_or_insert(sql, (
                        id, json.dumps(data_convert_after).decode('unicode-escape'), res['response'],
                        res['status_code'], res['m_code'], res['duration'], '', 'Fail',
                        self.session['info']['uid'], res['execute_time']))
        group_result = 'Fail' if 'Fail' in result_list else 'Pass'
        self.mysql.update_or_insert("update test_execute_log set result = %s where create_time =%s",
                                    (group_result, create_time))
