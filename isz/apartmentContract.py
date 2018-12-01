# -*- coding:utf8 -*-
import time
from common import datetimes
from common.base import consoleLog
from common.datetimes import today, addDays, addMonths
from common.dict import AUDIT_STATUS
from common.interface_wfl import myRequest, delNull, upLoadPhoto
from isz.contractBase import ContractBase
from isz.infoClass import ApartmentContractInfo, ApartmentContractEndInfo, HouseContractInfo


class ApartmentContract(ContractBase, ApartmentContractInfo):
    """
    出租合同对应操作
    :param contractIdOrNum 出租合同id或者num
    """
    uploadPhotoURL = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/uploadImageFile'  # 委托合同上传图片地址

    def audit(self):
        """审核
        初审25
        复审 22
        反审 24
        驳回 23
        """

        def audit(activityId):
            url = 'isz_contract/ApartmentContractController/apartmentContractAudit.action'
            data = {
                "achieveid": self.apartment_contract_id,
                "activityId": activityId,
                "content": "同意"
            }
            if myRequest(url, data):
                if activityId == '25':
                    consoleLog('出租合同已初审')
                    time.sleep(1)
                elif activityId == '22':
                    consoleLog('出租合同已复审')

        if 'AUDIT' == self.audit_status_now:
            audit('25')
            time.sleep(1)
            audit('22')
        if 'PASS' == self.audit_status_now:
            audit('22')

    def receiptAndAudit(self):
        """
        出租合同实收及实收的审核
        :return: 完成所有实收和审核
        """
        url = 'isz_finance/ApartmentContractReceiptsController/saveOrUpdateNewReceipts.action'
        receivables = self.receivables()
        i = 0
        consoleLog("共有%s条应收待实收" % len(receivables))
        for receivable in receivables:
            i = i + 1
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
            if result:
                # 审核
                consoleLog("实收第%s条完成" % i)
                myRequest(url='isz_finance/ApartmentContractReceiptsController/endReceivable.action',
                          data={'receivable_id': receivable.receivable_id})
                consoleLog("审核第%s条完成" % i)
            else:
                break

    def resign(self, contract_num=None, sign_date=None, rent_end_date=None, money_cycle=None, payment_date=None, ):
        """续签"""

        # self.receiptAndAudit()
        contract_num = 'RS-%s' % self.apartment_contract_num if not contract_num else contract_num
        sign_date = today() if not sign_date else sign_date
        rent_start_date = addDays(1, self.rent_end_date)
        rent_end_date = addMonths(12, self.rent_end_date) if not rent_end_date else rent_end_date
        start_date = rent_start_date
        end_date = rent_end_date
        money = self.rental_price if not self.rental_price == 'None' else 2030
        deposit = self.deposit
        month_server_fee = self.month_server_fee
        payment_date = rent_start_date if not payment_date else payment_date
        money_cycle = self.payment_cycle if not money_cycle else money_cycle
        data = {
            "apartmentContractRentInfoList": [{
                "firstRow": True,
                "money": money,
                "start_date": start_date,
                "rowIndex": 0,
                "end_date": end_date,
                "money_cycle": money_cycle,
                "payment_date": payment_date,
                "deposit": deposit,
                "agencyFeeMoney": "0.00",
                "money_type": "RENT",
                "rent_start_date": rent_start_date,
                "rent_end_date": rent_end_date,
                "sign_date": sign_date,
                "month_server_fee": month_server_fee
            }],

            "apartment_id": self.apartment_id,
            "apartment_rent_price": money,
            "sign_date": sign_date,
            "rent_end_date": rent_end_date,
            "payment_date": payment_date,
            "deposit_type": "ONE",
            "payment_type": "NORMAL",
            "payment_cycle": money_cycle,
            "cash_rent": str(float(money) * 0.1),
            "deposit": deposit,
            "agency_fee": "0.00",
            "month_server_fee": month_server_fee,
            "month_server_fee_discount": "100%",
            "dispostIn": 1,
            "contract_num": contract_num,
            "person": {},
            "model": "4"
        }
        url = 'isz_contract/ApartmentContractController/searchApartmentContractDetail.action'
        requestPayload = {
            "parent_id": self.apartment_contract_id,
            "contract_type": "RENEWSIGN"
        }
        result = myRequest(url, requestPayload)
        if result:
            apartmentContract = delNull(result['obj']['apartmentContract'])
            for x, y in apartmentContract.items():
                data[x] = y

            customerPerson = delNull(result['obj']['customerPerson'])
            for x, y in customerPerson.items():
                data['person'][x] = y

        data['receivables'] = self.createReceivables(data['apartmentContractRentInfoList'])

        hosueInfo = {
            "rent_start_date": rent_start_date,
            "rent_end_date": rent_end_date,
            "houseId": self.house_id,
            "apartment_id": self.apartment_id,
            "room_id": self.room_id
        }
        data['houseContractList'] = self.gethouseContractList(self.entrust_type, hosueInfo)
        contract_id = self.createApartmentContract(data)
        return ApartmentContract(contract_id)

    def end(self, end_date=today(), end_type=None):
        """终止结算"""
        self.audit()

        endImg = upLoadPhoto(url=self.uploadPhotoURL, filename='idCardPhotos.png', filepath=r"C:\Users\user\Desktop\Image\\")
        url = '/isz_contract/ContractEndController/saveOrUpdateApartmentContractEnd'
        endInfo = self.getEndInfo()
        endInfo['apartmentContractEndReceivableList'] = [
            {
                "balance_amount": 0,
                "create_time": None,
                "create_uid": None,
                "deleted": None,
                "end_amount": 0,
                "end_id": None,
                "receipts_amount": 0,
                "receivable_amount": self.deposit,
                "receivable_id": None,
                "receivable_type": "DEPOSIT",
                "receivable_type_cn": "押金",
                "should_amount": 0,
                "update_time": None,
                "update_uid": None
            }, {
                "balance_amount": 0,
                "create_time": None,
                "create_uid": None,
                "deleted": None,
                "end_amount": 0,
                "end_id": None,
                "receipts_amount": 0,
                "receivable_amount": 0,
                "receivable_id": None,
                "receivable_type": "RENT",
                "receivable_type_cn": "租金",
                "should_amount": 0,
                "update_time": None,
                "update_uid": None
            }, {
                "balance_amount": 0,
                "create_time": None,
                "create_uid": None,
                "deleted": None,
                "end_amount": 140,
                "end_id": None,
                "receipts_amount": 0,
                "receivable_amount": 1680,
                "receivable_id": None,
                "receivable_type": "MANAGE_SERVER_FEE",
                "receivable_type_cn": "管家服务费",
                "should_amount": 140,
                "update_time": None,
                "update_uid": None
            }, {
                "balance_amount": 0,
                "create_time": None,
                "create_uid": None,
                "deleted": None,
                "end_amount": 0,
                "end_id": None,
                "receipts_amount": 0,
                "receivable_amount": 0,
                "receivable_id": None,
                "receivable_type": "ADVANCE",
                "receivable_type_cn": "代垫费用",
                "should_amount": 0,
                "update_time": None,
                "update_uid": None
            }, {
                "balance_amount": 0,
                "create_time": None,
                "create_uid": None,
                "deleted": None,
                "end_amount": 0,
                "end_id": None,
                "receipts_amount": 0,
                "receivable_amount": 0,
                "receivable_id": None,
                "receivable_type": "LOAN_RENT",
                "receivable_type_cn": "分期租金",
                "should_amount": 0,
                "update_time": None,
                "update_uid": None
            }, {
                "balance_amount": 0,
                "create_time": None,
                "create_uid": None,
                "deleted": None,
                "end_amount": 0,
                "end_id": None,
                "receipts_amount": 0,
                "receivable_amount": 0,
                "receivable_id": None,
                "receivable_type": "LOAN_SERVER",
                "receivable_type_cn": "分期管家服务费",
                "should_amount": 0,
                "update_time": None,
                "update_uid": None
            }, {
                "balance_amount": 0,
                "create_time": None,
                "create_uid": None,
                "deleted": None,
                "end_amount": 0,
                "end_id": None,
                "receipts_amount": 0,
                "receivable_amount": 0,
                "receivable_id": None,
                "receivable_type": "LOAN_LIQUIDATED",
                "receivable_type_cn": "分期违约金",
                "should_amount": 0,
                "update_time": None,
                "update_uid": None
            }, {
                "balance_amount": 0,
                "create_time": None,
                "create_uid": None,
                "deleted": None,
                "end_amount": 0,
                "end_id": None,
                "receipts_amount": 0,
                "receivable_amount": 0,
                "receivable_id": None,
                "receivable_type": "LATE_FEE",
                "receivable_type_cn": "逾期费用",
                "should_amount": 0,
                "update_time": None,
                "update_uid": None
            }, {
                "balance_amount": 0,
                "create_time": None,
                "create_uid": None,
                "deleted": None,
                "end_amount": 0,
                "end_id": None,
                "receipts_amount": 0,
                "receivable_amount": 0,
                "receivable_id": None,
                "receivable_type": "CASH_RENT",
                "receivable_type_cn": "保证金",
                "should_amount": 0,
                "update_time": None,
                "update_uid": None
            }
        ]
        endInfo['endBasicInfo']['contract_id'] = self.apartment_contract_id
        endInfo['endBasicInfo']['end_contract_num'] = 'End-%s' % self.apartment_contract_num
        endInfo['endBasicInfo']['end_date'] = end_date
        endInfo['endBasicInfo']['end_reason'] = "HOUSE_PROBLEM"
        endInfo['endBasicInfo']['end_type'] = "OWNER_DEFAULT" if not end_type else end_type
        endInfo['endBasicInfo']['end_type_detail'] = "CUSTOMER_BREAK_CONTRACT"
        endInfo['endBasicInfo']['house_contract_num'] = HouseContractInfo(self.house_contract_id).house_contract_num
        endInfo['endBasicInfo']['is_old_data'] = "N"
        endInfo['endBasicInfo']['payable_totle'] = 0
        endInfo['endBasicInfo']['receivable_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        endInfo['imgList'] = [{
            "attachment_type": None,
            "img_id": endImg.id,
            "src": endImg.url
        }]
        receivable = 0
        for i in endInfo['apartmentContractEndReceivableList']:
            receivable = receivable + float(i['receivable_amount'])
        for j in endInfo['detailList']:
            receivable = receivable + float(j['payable_money'] if j['payable_money'] else 0)
        endInfo['liquidatedOrTurnFee'] = {
            "liquidated_receivable": receivable,
            "discount_liquidated_receivable": receivable,
            "liquidated_discount_scale": "100.00%",
            "turn_receivable": 0,
            "discount_turn_receivable": 0,
            "turn_discount_scale": 0,
            "liquidated_return": 0,
            "fileList": [],
            "discount_img_id": None,
            "discountImgList": [],
            "discount_img_src": None
        }
        endInfo['endBasicInfo']['receivable_total'] = str(receivable)
        endInfo['receiverInfo'] = {
            "contractEndPayerAgintType": "PAYER",
            "receipt_name": self.sign_name,
            "pay_object": "PERSONAL",
            "receipt_bank_no": "123456123465",
            "bank": "未知发卡银行",
            "receipt_bank_location": "海创支行"
        }
        if myRequest(url, endInfo):
            consoleLog('出租终止新增成功')

    def getEndInfo(self):
        """获取终止结算基础信息，终止结算前动作"""
        url = '/isz_contract/ContractEndController/searchContractEndInfo'
        data = {
            "contract_id": self.apartment_contract_id,
            "is_old_data": "N"
        }
        return myRequest(url, data)['obj']

    def endAudit(self):
        """终止结算审核"""
        endInfo = ApartmentContractEndInfo(self.apartment_contract_id)

        def audit(afterStatus):
            """审核
            :param afterStatus 审核操作后的状态
            """

            url = '/isz_contract/ContractEndController/auditApartmrntContractEnd'
            data = {
                "endBasicInfo": {
                    "audit_status": afterStatus,
                    "content": "同意！",
                    "contract_id": self.apartment_contract_id,
                    "end_contract_num": endInfo.end_contract_num,
                    "end_date": endInfo.end_date,
                    "update_time": time.strftime('%Y-%m-%d %H:%M:%S.0'),
                    "end_id": endInfo.end_id,
                    "end_type": endInfo.end_type,
                    "ins_result": "",
                    "payment_type": endInfo.contract_end_type
                },
                "liquidatedOrTurnFee": {
                    "discount_liquidated_receivable": endInfo.liquidated_receivable,
                    "liquidated_receivable": endInfo.liquidated_receivable,
                    "discountImgList": [],
                    "discount_img_id": None
                },
                "receiverInfo": {
                    "bank": endInfo.bank,
                    "contractEndPayerAgintType": "PAYER",
                    "pay_object": endInfo.pay_object,
                    "receipt_bank_location": endInfo.payer_bank_location,
                    "receipt_bank_no": endInfo.payer_bank_no,
                    "receipt_name": endInfo.payer
                }
            }
            if myRequest(url, data):
                if AUDIT_STATUS.APARTMETN_CONTRACT_END.AUDITED == afterStatus:
                    consoleLog('出租终止已初审')
                    time.sleep(1)
                elif AUDIT_STATUS.APARTMETN_CONTRACT_END.APPROVED == afterStatus:
                    consoleLog('出租终止已复审')

        if AUDIT_STATUS.APARTMETN_CONTRACT_END.WAIT_AUDIT == endInfo.end_audit_status or AUDIT_STATUS.APARTMETN_CONTRACT_END.REJECT == endInfo.end_audit_status:
            audit(AUDIT_STATUS.APARTMETN_CONTRACT_END.AUDITED)  # 初审
            audit(AUDIT_STATUS.APARTMETN_CONTRACT_END.APPROVED)  # 复审
        elif AUDIT_STATUS.APARTMETN_CONTRACT_END.AUDITED == endInfo.end_audit_status:
            audit(AUDIT_STATUS.APARTMETN_CONTRACT_END.APPROVED)  # 复审
        else:
            return

class ApartmentContractEnd(ApartmentContractEndInfo):


    def endAudit(self):
        """终止结算审核"""
        endInfo = ApartmentContractEndInfo(self.apartment_contract_id)

        def audit(action):
            """审核
            :param action 审核操作后的状态 """

            url = '/isz_contract/ContractEndController/auditApartmrntContractEnd'
            data = {
                "endBasicInfo": {
                    "audit_status": action,
                    "content": "同意！",
                    "contract_id": self.apartment_contract_id,
                    "end_contract_num": endInfo.end_contract_num,
                    "end_date": endInfo.end_date,
                    "update_time": time.strftime('%Y-%m-%d %H:%M:%S.0'),
                    "end_id": endInfo.end_id,
                    "end_type": endInfo.end_type,
                    "ins_result": "",
                    "payment_type": endInfo.contract_end_type
                },
                "liquidatedOrTurnFee": {
                    "discount_liquidated_receivable": endInfo.liquidated_receivable,
                    "liquidated_receivable": endInfo.liquidated_receivable,
                    "discountImgList": [],
                    "discount_img_id": None
                },
                "receiverInfo": {
                    "bank": endInfo.bank,
                    "contractEndPayerAgintType": "PAYER",
                    "pay_object": endInfo.pay_object,
                    "receipt_bank_location": endInfo.payer_bank_location,
                    "receipt_bank_no": endInfo.payer_bank_no,
                    "receipt_name": endInfo.payer
                }
            }
            if myRequest(url, data):
                if AUDIT_STATUS.APARTMETN_CONTRACT_END.AUDITED == action:
                    consoleLog('出租终止已初审')
                    time.sleep(1)
                elif AUDIT_STATUS.APARTMETN_CONTRACT_END.APPROVED == action:
                    consoleLog('出租终止已复审')

        audit_status = AUDIT_STATUS.APARTMETN_CONTRACT_END
        if audit_status.WAIT_AUDIT == endInfo.end_audit_status or audit_status.REJECT == endInfo.end_audit_status:
            audit(audit_status.AUDITED)  # 初审
            audit(audit_status.APPROVED)  # 复审
        elif AUDIT_STATUS.APARTMETN_CONTRACT_END.AUDITED == endInfo.end_audit_status:
            audit(audit_status.APPROVED)  # 复审
        else:
            return


if __name__ == '__main__':
    contract = ApartmentContract('预发20180929006')
    contract.audit()
    contract.receiptAndAudit()
    # contract.resign()
    # contract.end(end_date='2018-08-30')
    # contract.endAudit()
    # print AuditStatus.APARTMETN_CONTRACT_END_STATUS_WAIT_AUDIT
