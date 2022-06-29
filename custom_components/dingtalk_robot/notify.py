'''  https://open.dingtalk.com/document/group/custom-robot-access '''

import logging
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json
import os
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_MESSAGE,
    ATTR_TITLE,
    ATTR_DATA,
    ATTR_TARGET,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCE
CONF_SECRET = 'secret'

headers = {"Content-Type": "application/json"}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_RESOURCE): cv.url,
    vol.Optional(CONF_SECRET, default= ""): cv.string,
})

_LOGGER = logging.getLogger(__name__)
DIVIDER = "———————————"

def get_service(hass, config, discovery_info=None):
 
    resource = config.get(CONF_RESOURCE)
    secret = config.get(CONF_SECRET)

    return DingtalkNotificationService(resource,secret)


class DingtalkNotificationService(BaseNotificationService):
    

    def __init__(self, resource, secret):
      
        self._resource = resource
        self._secret = secret
        
    def _sign(self, timestamp, secret):
        #secret = 'this is secret'
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_message(self, message="", **kwargs):
        send_url = self._resource
        timestamp = str(round(time.time() * 1000))
        
        title = kwargs.get(ATTR_TITLE)
        data = kwargs.get(ATTR_DATA) or {}
        msgtype = data.get("type", "text")
        url = data.get("url")
        picurl = data.get("picurl")
        atmoblies = kwargs.get(ATTR_TARGET)
        #touser = ','.join(touser)
       
        if msgtype == "text":
            content = ""
            if title is not None:
                content += f"{title}\n{DIVIDER}\n"
            content += message
            msg = {"content": content}
        elif msgtype == "markdown":
            msg = {"title": title, "text": message}
        elif msgtype == "link":
            msg = {"title": title, "text": message, "picUrl": picurl, "messageUrl": url }
        elif msgtype == "actionCard":
            msg = {"title": title, "text": message, "btnOrientation": "0",  "singleTitle" : "阅读全文", "singleURL" : url } 
        else:
            raise TypeError("消息类型输入错误，请输入：text/link/markdown/actionCard")            
  
        send_values = {
            "at": {
                "atMobiles": atmoblies,
                "atUserIds": [],
                "isAtAll": "false"
            },
            "msgtype": msgtype,
			msgtype: msg,
        }
        
        if self._secret:            
            send_url = send_url + "&timestamp=" + timestamp + "&sign=" + self._sign(timestamp, self._secret)
        
        # if response.status_code not in (200, 201):
            # _LOGGER.exception(
                # "Error sending message. Response %d: %s:",
                # response.status_code, response.reason)
        _LOGGER.debug(send_values)
        send_msges = bytes(json.dumps(send_values), "utf-8")
        response = requests.post(send_url, data=send_msges, headers = headers).json()
        if response["errcode"] != 0:
            _LOGGER.error(response)
        else:
            _LOGGER.debug(response)