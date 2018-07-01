# -*- coding:utf8 -*-
from common import sqlbase
from common.base import consoleLog
from common.interface_wfl import myRequest, delNull
from common.mysql import Mysql

class ContractBase(object):
    """合同基础方法"""

    @staticmethod
    def getRentStrategys(rentStrategysData):
        """生成租金策略"""
        url = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/getHouseRentStrategyVo'
        return myRequest(url, rentStrategysData)['obj']

    @staticmethod
    def createContractPayable(contractPayableData):
        """生成委托合同应付"""
        url = 'http://erp.ishangzu.com/isz_finance/HouseContractPayableController/createContractPayable'
        return myRequest(url, contractPayableData)['obj']

    @staticmethod
    def saveHouseContract(houseContractInfo):
        """生成委托合同"""
        url = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/saveHouseContract'
        return myRequest(url, houseContractInfo, shutdownFlag=True)

    @staticmethod
    class FileType(object):
        """获取需要传的合同附件id"""
        _type_id_dict = {}

        def __init__(self):
            self.type_id_list = ContractBase.FileType.__get_list()

        @staticmethod
        def __get_list():
            if not ContractBase.FileType._type_id_dict:
                sql = "select file_type, file_type_id from contract_file_type where deleted=0"
                dicts = Mysql().query(sql)
                for dict in dicts:
                    ContractBase.FileType._type_id_dict[dict['file_type']] = dict['file_type_id']
            return ContractBase.FileType._type_id_dict

        def getFileIdByTpye(self, file_type):
            return self._type_id_dict[file_type]

    @staticmethod
    def createReceivables(apartmentContractRentInfoList):
        """生成实收"""
        url = '/isz_contract/ApartmentContractController/createApartmentContractReceivable.action'
        result = myRequest(url, apartmentContractRentInfoList)
        if result:
            data = delNull(result['obj'])
            index = 0
            for x in data:
                x['edit'] = False
                x['rowIndex'] = index
                index += 1
            return data

    @staticmethod
    def gethouseContractList(entrust_type, hosueInfo):
        """出租合同房屋信息"""
        url = 'isz_contract/ApartmentContractController/getHouseContractByHouseId.action'
        if entrust_type == 'ENTIRE':
            del hosueInfo['room_id']
        result = myRequest(url, hosueInfo)
        if result:
            data = delNull(result['obj'])
            return data

    @staticmethod
    def createApartmentContract(data):
        """生成出租合同"""
        url = 'isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action'
        result = myRequest(url, data)
        if result:
            consoleLog(u'承租合同 %s 已创建完成' % data['contract_num'])
            apartmentContractInfo = {'contractID': sqlbase.serach(
                "select contract_id from apartment_contract where contract_num = '%s'" % data['contract_num'])[0],
                                     'contractNum': data['contract_num']}
            return apartmentContractInfo['contractID']
