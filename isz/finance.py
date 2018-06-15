# -*- coding:utf8 -*-

from common.base import log, consoleLog, Base
from common import sqlbase
import time

from common.interface_wfl import myRequest
from isz.infoClass import Receivable, ApartmentContractInfo


class Finance():
    """财务相关接口"""

    # 应收对应合同
    @staticmethod
    def __receivableContract(receivable_id):
        sql = "select a.receivable_id,b.contract_num from apartment_contract_receivable a inner join apartment_contract b on a.contract_id=b.contract_id where receivable_id='%s' " % receivable_id
        return sqlbase.serach(sql)

    # 检查应收状态
    @staticmethod
    def __receivableStatus(receivable_id):
        sql = "select end_status from apartment_contract_receivable where receivable_id='%s'" % receivable_id
        return sqlbase.serach(sql)[0]

    # 出租实收审核
    @staticmethod
    def endReceivable(receivable_id):
        url = "/isz_finance/ApartmentContractReceiptsController/endReceivable.action"
        data = {"receivable_id": receivable_id}
        receivable = Receivable(receivable_id)
        contract_num = ApartmentContractInfo(receivable.contract_id).apartment_contract_num
        result = myRequest(url, data)
        if result and 'AUDITED' == receivable.end_status_now:
            consoleLog(u'出租合同 %s 实收 %s 审核完成' % (contract_num, receivable_id))
            time.sleep(1)
        else:
            consoleLog(u'出租合同 %s 实收 %s 审核失败' % (contract_num, receivable_id))

if __name__ == '__main__':
    fin = Finance()
    # sql = "select DISTINCT a.receivable_id from apartment_contract_receivable a inner join apartment_contract b on a.contract_id=b.contract_id and b.deleted=0 and b.contract_status<>'CANCEL' inner join apartment_contract_receipts c on c.receivable_id=a.receivable_id and c.receipts_date <= CONCAT('2015-12-31', ' 23:59:59') and c.deleted=0 where a.end_status in ('HASGET','PARTGET') and a.deleted=0 and b.contract_num NOT in ('WB1-0070791','ISZWY(CZ)-0000269','ISZWY(CZ)-0001288','ISZWY(CZ)-0001288','WB1-0071977','WB1-0068237','WB1-0069391','WB1-0069391','WB1-0069391','WB1-0073856','WB1-0068392','WB1-0074356','WB1-0068438','WB1-0072831','WB1-0067046','WB1-0061284','WB1-0068236','ISZWY(CZ)-0000683','WB1-0069433','WB1-0068429','WB1-0064325','WB1-0062904','WJ1-0001114','新科C-H0000986')"
    sql = "select DISTINCT a.receivable_id from apartment_contract_receivable a inner join apartment_contract b on a.contract_id=b.contract_id and b.deleted=0 and b.contract_status<>'CANCEL' inner join apartment_contract_receipts c on c.receivable_id=a.receivable_id and c.receipts_type='INTRANSFER' and c.deleted=0 where a.end_status in ('HASGET') and a.deleted=0;"
    receivables = sqlbase.serach(sql, oneCount=False)
    print(len(receivables))
    for receivable_id in receivables:
        fin.endReceivable(receivable_id)

