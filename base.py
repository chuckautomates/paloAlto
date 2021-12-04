#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2021 Chuck McLaine
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import, division, print_function
import requests
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree as ET
__metaclass__ = type


DOCUMENTATION = '''
---
module: caPaloAlto
short_description: Library of funcations for palo alto network devices.
author:
    - Chuck McLaine (@chuckautomates)
version_added: "0.1"
requirements:
    - requests can be obtained from PyPI U(https://pypi.org/project/requests/)
'''


class Base(object):

    def __init__(self, **kwargs):
        self._xpath = kwargs['basePath']    # IP Address or FQDN
        self._username = kwargs['username']
        self._password = kwargs['password']
        self._ssl_verify = kwargs['sslVerify']
        # Format the base url ex: https://firewall.aceme.com/api 
        self._base = '{0}{1}{2}'.format('https://', self._xpath, '/api')
    
    def __string__(self):
        print(self._xpath)

    def generate_token(self):
        xpath = '{0}{1}{2}{3}{4}'.format(self._base, '/?type=keygen&user=', self._username, '&password=', self._password)
        try:
            response = requests.request("GET", xpath, verify = self._ssl_verify)
        except:
            response = requests.request("GET", xpath)
        tree = ET.XML(response.text)
        token = tree[0][0].text
        return(token)

    def headers(self):
        try:
            if '_username' in dir(self) and '_password' in dir(self):
                token = self.generate_token()
            else:
                pass
                #token = kwargs['token']
            headers = {  'Content-Type': 'application/xml',
                        'X-PAN-KEY': token}
            # Returns formatted headers
            return(headers)
        # Format and create request to address tags
        except:
            # Returns formatted headers
            return('Error')

    def get_error(self, response):
        if int(response.status_code) == 200:
            return(response.text)
        else:
            return(response.status_code)

    def get_request(self, xpath, headers, sslVerify):     
        try:
            response = requests.request("GET", xpath, headers = headers, verify = sslVerify)
        except:
            response = requests.request("GET", xpath, headers = headers)
        return(response)








