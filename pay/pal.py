#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests as req

PAL_BASE_URL = 'http://panel.20pall.com/'
# APP_SERVER_ADDR = 'http://185.105.186.81'
PAL_API_URL = PAL_BASE_URL + 'api/'
PAL_VERIFY_URL = PAL_API_URL + 'verify/'
PAL_CREATE_URL = PAL_API_URL + 'create/'
PAL_PAY_URL = PAL_BASE_URL + 'startpay/'
# verify_url = 'http://panel.20pall.com/api/verify/'
# create_url = 'http://panel.20pall.com/api/create/'
# pay_base_url = 'http://panel.20pall.com/startpay/' # + TRANSID
PIN = '18DDAC3F64458EAD800D'
amount = 5000
description = 'عضویت طلایی روان‌یار'
callback = 'https://web.telegram.org/#/im?p=@RavanYaarBot'
TIMEOUT = 6


def create_transaction():
    code = 1  # 1: successful, 2: timeout, 3: other reasons
    params = {'amount': amount, 'pin': PIN, 'callback': callback, 'description': description}
    try:
        r = req.get(PAL_CREATE_URL, data=params, timeout=TIMEOUT)
        new_transid = r.text
        return code, new_transid
    except req.exceptions.Timeout:
        code = 2
        dummy = 'blah blah'
        return code, dummy
    except:
        code = 3
        dummy = 'blah blah'
        return code, dummy


def verify_transaction(transid):
    # return values --> 1: successful, 2: timeout, 3: other reasons
    params = {'transid': transid, 'pin': PIN, 'amount': amount}
    try:
        r = req.get(PAL_VERIFY_URL, data=params, timeout=TIMEOUT)
        return r.text
    except req.exceptions.Timeout:
        return 2
    except:
        return 3


def get_pay_link(transid):
    return PAL_PAY_URL + transid

