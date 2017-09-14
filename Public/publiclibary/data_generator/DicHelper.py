# coding: utf-8
import json
import types
import string


# 获取字典中的objkey对应的值，适用于字典嵌套
# dict:字典
# objkey:目标key
# default:找不到时返回的默认值


def dict_get(dict, objkey, index):
    indexnum = int(index)
    tmp = dict
    for k, v in tmp.items():
        if k == objkey:
            return v
        else:
            ret = None
            if type(v) is types.DictType:
                ret = dict_get(v, objkey, indexnum)
            if type(v) is types.TupleType or type(v) is types.ListType:
                if len(v) > 0:
                    ret = dict_get(v[indexnum - 1], objkey, indexnum)
            if type(v) is types.StringType:
                if len(v.split(":")) > 1 or len(v.split(",")) > 1:
                    return getStringValue(v, objkey)
            if ret is not None:
                return ret
    return None


def getStringValue(str, key):
    for substr in str.split(","):
        if substr.find(key) != -1:
            return substr.split(":")[1].replace("'", "").replace("}", "")


def main():
    # jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}';
    jsonobj = {
        "body": {
            "totalCount": 0,
            "moneyBoxOrderList": [],
            "class": "cn.memedai.wallet.facade.vo.MoneyBoxOrderAdditionAllVO"
        },
        "respMsg": "成功!",
        "respCode": "1000"
    }

    json = {
        "body": {
            "pageResponse": {
                "rows": [
                    {
                        "alliesCode": "100932_14",
                        "merchantNo": "None",
                        "invoiceStatus": "NORMAL",
                        "year": 2016,
                        "month": 11,
                        "invoiceAmtApply": 144.0,
                        "issuingName": "上海元玺商业保理有限公司",
                        "issuingType": "INVOICE_YUANXI",
                        "actualInvoiceAmt": "None",
                        "class": "cn.memedai.loan.facade.response.invoice.DubboInvoiceInfo"
                    },
                    {
                        "alliesCode": "100932_14",
                        "merchantNo": "None",
                        "invoiceStatus": "NORMAL",
                        "year": 2016,
                        "month": 7,
                        "invoiceAmtApply": 320.0,
                        "issuingName": "上海米么金融信息服务有限公司",
                        "issuingType": "INVOICE_MIME",
                        "actualInvoiceAmt": "None",
                        "class": "cn.memedai.loan.facade.response.invoice.DubboInvoiceInfo"
                    }
                ],
                "total": 2,
                "class": "cn.memedai.loan.facade.response.PageResponse"
            },
            "class": "cn.memedai.loan.facade.response.invoice.DubboInvoiceInfoResponse"
        },
        "respMsg": "成功!",
        "respCode": "1000"
    }

    test = {
    "code": "000",
    "accessToken": "C76B9EF37E4FE808414DD48A1CE63DF911721589EE6A3046C3CA556F42705635",
    "timestamp": 1492503387593,
    "sign": "02838aa9fb5a8f6a6838f85142fe3e2c",
    "content": "{'serialNo':'2017041849235221'}",
    "desc": "成功!"
}
    print dict_get(test, 'serialNo', '1')
    # str = "{'serialNo':'2017041767764543','dfgd':'2017'}"
    # print getStringValue(str, "dfgd").replace("'", "").replace("}", "")


if __name__ == '__main__':
    main()