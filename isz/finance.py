# -*- coding:utf8 -*-

from common.base import log, consoleLog, Base
from common import sqlbase, datetimes
import time

from common.interface_wfl import myRequest
from isz.infoClass import Receivable, ApartmentContractInfo


class Finance(object):
    """财务相关接口"""

    def receipt(self, receivable_id):
        """实收"""
        url = 'isz_finance/ApartmentContractReceiptsController/saveOrUpdateNewReceipts.action'
        receivables = self.receivables()
        for receivable in receivables:
            data = {
                'alipay_card': '0011',  # 支付宝账号
                'company': self.sign_body,  # 收款公司
                'contract_id': self.apartment_contract_id,
                'operation_total': receivable.receivable_money,  # 转账总金额
                'receipts_date': datetimes.today(),  # 收款日期
                'receipts_type': 'ALIPAY',  # 收款方式：支付宝转账
                'receipts_money': receivable.receivable_money,  # 收款金额
                'receivable_id': receivable.receivable_id  # 应收ID
            }
            # 实收
            result = myRequest(url, data)

    @staticmethod
    def endReceivable(receivable_id):
        """出租实收审核"""
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
    sql = "select DISTINCT a.receivable_id from apartment_contract_receivable a inner join apartment_contract b on a.contract_id=b.contract_id and b.deleted=0 " \
          "and b.contract_status<>'CANCEL' inner join apartment_contract_receipts c on c.receivable_id=a.receivable_id and c.receipts_type='INTRANSFER' and c.deleted=0 " \
          "where a.end_status in ('HASGET') and a.deleted=0;"
    receivables = sqlbase.serach(sql, oneCount=False)
    print(len(receivables))
    for receivable_id in receivables:
        fin.endReceivable(receivable_id)

