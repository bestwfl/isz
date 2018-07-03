# -*- coding:utf8 -*-
import time

from isz.contractBase import ContractBase
from common import sqlbase
from common.base import consoleLog
from common.datetimes import today, addDays, addMonths, addMonthExDay
from common.dict import house_contract_dict, free_date_par, userInfo, AUDIT_STATUS
from common.interface_wfl import myRequest
from isz.infoClass import HouseContractInfo, HouseContractEndInfo


class HouseContract(ContractBase, HouseContractInfo):
    """
    委托合同相关，包括初审复审续签，终止及审核...
    """

    # 合同照片
    def contractPhotos(self):

        def photos(photoType, oneCount=True):
            sql = "select a.img_id,b.src from  house_contract_attachment a inner join image b on a.img_id=b.img_id " \
                  "where contract_id='%s'and attachment_type='%s' and a.deleted=0" % (self.contract_id, photoType)
            return sqlbase.serach(sql, oneCount)

        # payeeIdPhotoSql = sqlbase.serach("select a.img_id,b.src from  house_contract_attachment a inner join image b on a.img_id=b.img_id where contract_id='%s' "
        #                                  "and attachment_type='PAYEEIDPHOTO' and a.deleted=0" % self.contract_id)
        # contractAttachmentsSql = sqlbase.serach("select a.img_id,b.src from  house_contract_attachment a inner join image b on a.img_id=b.img_id where contract_id='%s' "
        #                                  "and attachment_type='HOUSECONTRACT_ATTACHMENT' and a.deleted=0" % self.contract_id)
        payeeIdPhotos = photos('PAYEEIDPHOTO')
        contractAttachments = photos('HOUSECONTRACT_ATTACHMENT')
        payeeIdPhotos = payeeIdPhotos if payeeIdPhotos else ['', '']
        contractAttachments = contractAttachments if contractAttachments else ['', '']
        contractPhotos = {
            'payeeIdPhotos': {'img_id': payeeIdPhotos[0], 'src': payeeIdPhotos[1]},  # 收款人证件照片
            'contractAttachments': {'img_id': contractAttachments[0], 'src': contractAttachments[1]}  # 合同附件
        }
        return contractPhotos

    def getHouseContractInfo(self):
        """合同详情"""
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfo/%s" % self.house_contract_id
        return myRequest(url, needCookie=True, method='get')['obj']

    def auditPayable(self):
        """审核应付"""
        consoleLog(u'开始审核委托合同应付')
        url = 'http://erp.ishangzu.com/isz_finance/HouseContractPayableController/updatePayableAuditStatusById'
        payableIds = sqlbase.serach(
            "select payable_id from house_contract_payable where contract_id='%s' and audit_status = 'NOTAUDIT' and deleted = 0 "
            "and money_type = 'RENT' " % self.house_contract_id, oneCount=False, research=True, nullLog=False)
        if len(payableIds) > 0:
            data = {
                "audit_status": "AUDITED",
                "payableIds": payableIds
            }
            result = myRequest(url, data, method='put')
            if not result:
                consoleLog('委托合同"%s"应付审核失败！' % self.house_contract_num)
                quit()
            else:
                consoleLog('委托合同"%s"应付审核通过' % self.house_contract_num)
        else:
            consoleLog('委托合同"%s"没有待审核应付' % self.house_contract_num)

    def audit(self, auditAction='fushen'):
        """审核"""
        step_Par = house_contract_dict['step_Par']
        auditStatus_Par = house_contract_dict['auditStatus_Par']
        contractInfo = self.getHouseContractInfo()

        def auditBase(page, auditAction):
            url = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/saveOrUpdateHouseContractDetailByPart'
            url_audit = 'http://erp.ishangzu.com/isz_housecontract/houseContractController/houseContractAudit'
            page_Data = {
                'auditForm': {
                    'audit_status': auditStatus_Par[auditAction],
                    'content': '同意!'
                },
                'action_type': 'AUDIT',
                step_Par[page]: contractInfo[step_Par[page]],
                'save_part': page,
                'contract_id': self.house_contract_id
            }
            data_FIVE = {
                "audit_status": auditStatus_Par[auditAction],
                "content": "合同内容、资料、备件无误，正常审核通过。同意!",
                "contract_id": self.house_contract_id,
                "is_normal_approved": "0"

            }
            page_Data = data_FIVE if page == 'FIVE' else page_Data
            url = url_audit if page == 'FIVE' else url
            method = 'put' if page == 'FIVE' else 'post'
            result = myRequest(url, page_Data, method=method)
            if result:
                # consoleLog(u'HOUSE CONTRACT STEP *%s* %s SUCCESS' % (page, auditAction))
                return
            else:
                consoleLog(u'HOUSE CONTRACT STEP *%s* %s FAIL!!!' % (page, auditAction))
                quit()

        if 'chushen' == auditAction or 'fushen' == auditAction:
            self.auditPayable()
            if AUDIT_STATUS.HOUSE_CONTRACT.WAIT_AUDIT == self.audit_status_now:
                for step in step_Par.keys():
                    if AUDIT_STATUS.HOUSE_CONTRACT.WAIT_AUDIT == self.step_status(step):
                        auditBase(step, 'chushen')
                if AUDIT_STATUS.HOUSE_CONTRACT.AUDITED == self.audit_status_now:
                    consoleLog('委托合同已初审')
            if 'fushen' == auditAction and AUDIT_STATUS.HOUSE_CONTRACT.AUDITED == self.audit_status_now:
                for step in step_Par.keys():
                    if AUDIT_STATUS.HOUSE_CONTRACT.AUDITED == self.step_status(step):
                        auditBase(step, auditAction)
                if AUDIT_STATUS.HOUSE_CONTRACT.APPROVED == self.audit_status_now:
                    consoleLog('委托合同已复审')

    def resign(self, contract_num, apartment_type=None, entrust_type=None, sign_date=today(), owner_sign_date=today(),
               entrust_start_date=None, entrust_year=None, payment_cycle=None, fitment_start_date=None,
               fitment_end_date=None,
               rent_money=None):
        """续签"""

        def getcontractInfo():
            """获取合同续签信息"""
            url = "http://erp.ishangzu.com/isz_housecontract/houseContractController/searchHouseContractInfoBase?contract_type=RENEWSIGN&house_id=%s&parent_id=%s" % (
                self.house_id, self.house_contract_id)
            return myRequest(url, method='get')['obj']

        # 基础字段
        contract_type = 'RENEWSIGN'
        apartment_type = apartment_type if apartment_type else self.apartment_type  # 默认原合同的公寓类型
        entrust_type = entrust_type if entrust_type else self.entrust_type  # 默认原合同的出租方式
        # 品牌公寓的装修开始和结束都默认在原合同之后一天，服务公寓没有装修期
        if apartment_type == 'BRAND':
            fitment_start_date = fitment_start_date if fitment_start_date else addDays(1, self.entrust_end_date)
            fitment_end_date = fitment_end_date if fitment_end_date else fitment_start_date
        else:
            fitment_start_date = None
            fitment_end_date = None
        entrust_start_date = entrust_start_date if entrust_start_date else (
            addDays(1, fitment_end_date) if fitment_end_date else addDays(1,
                                                                          self.entrust_end_date))  # 续签开始日期默认为装修期结束日后一天，没有装修期的话就是原合同到期日的后一天
        entrust_year = entrust_year if entrust_year else (
            self.entrust_year if self.entrust_year else 3)  # 委托年限默认原合同年限，原合同没有的话3年
        payment_cycle = payment_cycle if payment_cycle else self.payment_cycle  # 付款周期默认与原合同相同
        entrust_year_after = addDays(-1, addMonths(12 * int(entrust_year), entrust_start_date))
        entrust_end_date = addDays(free_date_par[payment_cycle] * int(entrust_year), entrust_year_after)  # 委托到期日
        rent_money = rent_money if rent_money else self.rental_price  # 委托金额默认与原合同相同
        first_pay_date = addMonthExDay(30, months=0, date=entrust_start_date)  # 付款日 默认委托下个月30号为第一次
        second_pay_date = addMonthExDay(30, months=2, date=entrust_start_date)  # 目前不影响第二次应付的时间，实际为第一次付款日加付款周期后的时间
        contractInfo = getcontractInfo()
        landlordInfo = self.landlord()
        contractPhotos = self.contractPhotos()
        houseContractFirst = contractInfo['houseContractFrist']  # 房源信息
        houseContractSecond = {
            'agreedRentOriginalStatements': [],
            'any_agent': '0',  # 有无代理人 （默认无代理人）
            'assetsOfLessor': [{
                'landlord_name': landlordInfo.landlord_name,
                'phone': landlordInfo.phone,
                'email': landlordInfo.email,
                'mailing_address': landlordInfo.mailing_address
            }],  # 资产出租人
            'contract_id': None,
            'houseContractSign': {
                'address': '',
                'agent_type': '',
                'attachments': [],
                'card_type': '',
                'email': '',
                'id_card': '',
                'phone': '',
                'sign_name': ''
            },
            'is_new_data': None,
            'originalAgentDataRelations': [],
            'originalLessorHasDied': []
        }  # 出租人
        houseContractThird = {
            'account_bank': self.account_bank,  # 收款行支行（默认）
            'account_name': self.account_name,  # 收款人姓名
            'account_num': self.account_num,  # 收款账号 （默认）
            'bank': self.bank,  # 收款银行 （默认）
            'contract_id': None,
            'is_new_data': None,
            'notPropertyOwnerGrantReceipts': [],
            'pay_object': self.pay_object,  # 收款账号类型 （默认个人）
            'payeeIdPhotos': [{
                'src': 'http://img.ishangzu.com/' + str(contractPhotos['payeeIdPhotos']['src']),  # 默认
                'url': 'http://img.ishangzu.com/' + str(contractPhotos['payeeIdPhotos']['src']),  # 默认
                'remark': '',
                'img_id': contractPhotos['payeeIdPhotos']['img_id']  # 默认
            }],  # 证件照片
            'payee_card_type': self.payee_card_type,  # 证件类型
            'payee_card_type_cn': '',
            'payee_emergency_name': landlordInfo.emergency_name,  # 紧急人姓名（默认）
            'payee_emergency_phone': landlordInfo.emergency_phone,  # 紧急人手机号码（默认）
            'payee_id_card': self.payee_id_card,  # 证件号
            'payee_type': self.payee_type,  # 收款人类型 （默认产权人）
            'payee_type_cn': ''
        }  # 收款人&紧急联系人
        rentStrategysData = {
            "apartment_type": apartment_type,
            "contract_type": contract_type,
            "entrust_start_date": entrust_start_date,
            "entrust_end_date": entrust_end_date,
            "free_end_date": "",
            "free_start_date": "",
            "parking": "",
            "payment_cycle": payment_cycle,
            "rent_money": str(rent_money),
            "sign_date": sign_date,
            "city_code": self.city_code,
            "entrust_year": entrust_year,
            "free_days": free_date_par[payment_cycle],
            "version": "V_TWO"}  # 传到合同信息中
        rentStrategys = self.getRentStrategys(rentStrategysData)  # 租金策略
        houseContractFour = {
            'apartment_type': apartment_type,  # 公寓类型
            'apartment_type_cn': '',
            'area_code': self.area_code,  # 城区
            'audit_status': None,
            'audit_time': None,
            'audit_uid': None,
            'building_id': self.building_id,
            'city_code': self.city_code,  # 城市
            'contractAttachments': [{
                "src": 'http://img.ishangzu.com/' + str(contractPhotos['contractAttachments']['src']),
                "url": 'http://img.ishangzu.com/' + str(contractPhotos['contractAttachments']['src']),
                "img_id": contractPhotos['contractAttachments']['img_id']
            }],
            'contract_id': None,
            'contract_num': contract_num,
            'contract_status': None,
            'contract_type': contract_type,
            'contract_type_cn': u'新签' if contract_type == 'NEWSIGN' else u'续签',
            'delay_date': None,  # 延长到期日
            "free_days": free_date_par[payment_cycle],
            'electron_file_src': None,
            'energy_company': None,
            "entrust_year": entrust_year,
            "entrust_year_cn": "",
            'energy_fee': None,
            'entrust_end_date': entrust_end_date,  # 委托到期日
            'entrust_start_date': entrust_start_date,  # 委托开始日期
            'entrust_type': entrust_type,  # 合同类型
            'entrust_type_cn': '',
            'first_pay_date': first_pay_date,  # 首次付款日
            'fitment_end_date': fitment_end_date,  # 装修到期日
            'fitment_start_date': fitment_start_date,  # 装修起算日
            'freeType_cn': '',
            'have_parking': 'Y',  # 是否有停车位 （默认有）
            'house_id': self.house_id,
            'housekeep_mange_dep': None,
            'housekeep_mange_dep_user': '-',
            'housekeep_mange_did': None,
            'housekeep_mange_uid': None,
            'housekeep_mange_user_name': None,
            'is_electron': None,
            'is_new_data': None,
            'owner_sign_date': owner_sign_date,  # 签约日期
            'parent_id': self.house_contract_id,
            'parking': "",  # 车位费（默认）
            'payment_cycle': payment_cycle,  # 付款方式
            'payment_cycle_cn': '',
            'property': None,
            'property_company': None,
            'reform_way': 'OLDRESTYLE' if apartment_type == 'BRAND' else 'UNRRESTYLE',  # 改造方式
            'reform_way_cn': '',
            'remark': None,
            'rentMoney': str(rent_money),  # 租金
            'rentStrategys': rentStrategys,
            'rental_price': str(float(rent_money)),  # 总租金
            'reset_finance': 'false',
            'residential_id': self.residential_id,
            'second_pay_date': second_pay_date,  # 第二次付款日
            'server_manage_dep_user': '',
            'server_manage_did': None,
            'server_manage_did_name': None,
            'server_manage_uid': None,
            'server_manage_uid_name': None,
            'service_fee_factor': 0.01,  # 年服务费 （默认）
            'sign_body': 'ISZPRO',  # 签约公司 （默认）
            'sign_date': sign_date,
            'sign_dep_name': userInfo['dep_name'],  # 签约部门
            'sign_did': userInfo['did'],
            'sign_uid': userInfo['uid'],
            'sign_user_name': userInfo['user_name'],  # 签约人
            'year_service_fee': None
        }  # 合同信息
        rentStrategysData = {
            "apartment_type": apartment_type,
            "contract_type": contract_type,
            "entrust_start_date": entrust_start_date,
            "entrust_end_date": entrust_end_date,
            "free_end_date": None,
            "free_start_date": None,
            "parking": None,
            "payment_cycle": payment_cycle,
            "rent_money": rent_money,
            "property": None,
            "energy_fee": None,
            "sign_date": sign_date,
            "city_code": self.city_code,
            "entrust_year": entrust_year,
            "free_days": free_date_par[payment_cycle],
            "version": "V_TWO"
        }
        rentStrategys = self.getRentStrategys(rentStrategysData)
        contractPayableData = {
            'contractId': None,
            'firstPayDate': first_pay_date,
            'secondPayDate': second_pay_date,
            'rentInfoList': rentStrategys,
            'version': 'V_TWO'
        }
        houseContractFive = self.createContractPayable(contractPayableData)
        houseContract = {
            'houseContractFrist': houseContractFirst,
            'houseContractSecond': houseContractSecond,
            'houseContractThird': houseContractThird,
            'houseContractFour': houseContractFour,
            'houseContractFive': houseContractFive
        }
        result = self.saveHouseContract(houseContract)
        if result:
            houseContractInfo = sqlbase.serach(
                "select contract_id from house_contract where house_id = '%s' and deleted = 0 and contract_type='RENEWSIGN' and contract_num='%s' order by create_time desc limit 1" %
                (self.house_id, contract_num))
            consoleLog(u'委托续签合同成功！')
            consoleLog(u'合同编号 : %s 合同ID : %s' % (contract_num, houseContractInfo[0]))
            return houseContractInfo[0]

    def __getEndBase(self):
        """获取终止结算基础数据"""
        url = "http://erp.ishangzu.com/isz_housecontract/houseContractEndController/searchHouseContractEndMsg/%s" % self.house_contract_id
        return myRequest(url, method='get')['obj']

    def end(self):
        """提交终止结算"""
        if not HouseContractEndInfo(self.house_contract_id).house_contract_end_info:
            self.audit('fushen')
            url = "http://erp.ishangzu.com/isz_housecontract/houseContractEndController/saveHouseContractEnd"
            end_contract_num = 'End-%s' % self.house_contract_num
            endBase = self.__getEndBase()
            endBase['end_contract_num'] = end_contract_num
            endBase['end_date'] = '%s 00:00:00' % time.strftime('%Y-%m-%d')
            endBase['contractImgList'] = [{
                "src": "http://img.ishangzu.com/erp/2018/4/19/17/ceed711b-aa91-4516-90be-71ea08eaafd3.png",
                "url": "http://img.ishangzu.com/erp/2018/4/19/17/ceed711b-aa91-4516-90be-71ea08eaafd3.png",
                "type": "",
                "img_id": "FF80808162D81DCB0162DD4C8B3500DD"
            }]
            endBase['pay_bank'] = self.account_bank
            endBase['pay_bank_no'] = self.account_num
            endBase['pay_object'] = self.pay_object
            endBase['payable_date'] = '%s 00:00:00' % time.strftime('%Y-%m-%d')
            endBase['receivable_date'] = '%s 00:00:00' % time.strftime('%Y-%m-%d')
            endBase['pay_name'] = self.account_name
            endBase['pay_type'] = 'OWNER'
            endBase['end_type'] = 'OWNER_DEFAULT'  # CORPORATE_DEFAULT
            result = myRequest(url, endBase)
            if result:
                consoleLog('委托合同 "%s" 已提交终止结算' % self.house_contract_num)
        else:
            consoleLog('委托合同 "%s"，已经终止' % self.house_contract_num)
        return HouseContractEnd(self.house_contract_id)


class HouseContractEnd(HouseContractEndInfo):
    """终止结算"""

    def end_audit(self):
        """终止结算审核"""

        def audit(activityId):
            """审核
            :param activityId 审核步骤ID
            """
            url = "http://erp.ishangzu.com/isz_contract/endAgreementControl/houseContractEndAudit.action"
            data = {
                "achieveid": self.end_id,
                "activityId": activityId,
                "content": "同意"
            }
            if myRequest(url, data):
                return True

        if AUDIT_STATUS.HOUSE_CONTRACT_END.WAIT_AUDIT == self.end_audit_status:
            if audit('18'):
                consoleLog('委托终止编号：%s,终止结算已初审' % self.house_contract_num)
        if AUDIT_STATUS.HOUSE_CONTRACT_END.AUDITED == self.end_audit_status_now:
            if audit('19'):
                consoleLog('委托终止编号：%s,终止结算已复审' % self.house_contract_num)
        if AUDIT_STATUS.HOUSE_CONTRACT_END.APPROVED == self.end_audit_status_now:
            consoleLog('委托终止编号：%s，终止结算状态为已复审' % self.house_contract_num)


if __name__ == '__main__':
    # login()
    contract = HouseContract('zll2018-07-02wjx011')
    # contract_num = 'RS-%s' % contract.contract_num
    # contract.resign(contract_num)
    contract.end()
    # print(landlord)
