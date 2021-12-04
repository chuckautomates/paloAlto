#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2021 Chuck Automates
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
from requests.auth import HTTPBasicAuth
from base import Base as Base
from xml.etree import ElementTree as ET
import time


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


class DeviceController(Base):
    def __init__(self, **kwargs):
        self._xpath = kwargs['basePath']    # IP Address or FQDN
        self._username = kwargs['username']
        self._password = kwargs['password']
        self._sslVerify = kwargs['sslVerify']
        # Format the base url ex: https://firewall.aceme.com/api 
        self._base = '{0}{1}{2}'.format('https://', self._xpath, '/api')

    def __str__(self):
        print('Convert to string')
        return self._xpath        

    def deviceSaveBackup(self):
        # This function will send a request to save the Configuration Snapshot locally to the FW
        # Format XPath
        xpath = '{0}{1}'.format(self._base, '?type=op&action=save&cmd=<save><config><to>PM-Backup.xml</to></config></save>')
        # Print XPath to confirm it's correct
        print(xpath)
        # Retrieve Proper headers from base file
        headers = self.headers()
        # Check if you are using SSL Verify flag or not
        if self._sslVerify == False:
            response = self.get_request(xpath, headers, self._sslVerify)
        else:
            response = self.get_request(xpath, headers)
        # Send response to get_error function
        _response_ = self.get_error(response)
        return(_response_)



    def deviceExportBackup(self):
        # This function will download a copy of the backup
        # Format XPath
        xpath = '{0}{1}'.format(self._base, '?type=export&action=save&cmd=<save><config><to>PM-Backup.xml</to></config></save>&category=configuration')
        # Print XPath to confirm it's correct
        print(xpath)
        # Retrieve Proper headers from base file
        headers = self.headers()
        # Check if you are using SSL Verify flag or not
        if self._sslVerify == False:
            response = self.get_request(xpath, headers, self._sslVerify)
        else:
            response = self.get_request(xpath, headers)
        _response_ = self.get_error(response)
        with open("PM-Backup.xml", "w") as f:
            f.write(_response_)
        return(_response_)


    def deviceDownloadContentUpdate(self):
        # This function will download latest content update to Firewall
        # Format XPath
        xpath = '{0}{1}'.format(self._base, '?type=op&action=cmd&cmd=<request><content><upgrade><download><latest/></download></upgrade></content></request>')
        # Print XPath to confirm it's correct
        print(xpath)
        # Retrieve Proper headers from base file
        headers = self.headers()
        # Check if you are using SSL Verify flag or not
        if self._sslVerify == False:
            response = self.get_request(xpath, headers, self._sslVerify)
        else:
            response = self.get_request(xpath, headers)
        _response_ = self.get_error(response)
        # Load response into XML
        tree = ET.XML(_response_)
        ET.dump(tree)
        # Grab the XML position of job id
        jobId = tree[0][1].text
        return(jobId)


    def deviceJobStatus(self, jobId):
        xpath = '{0}{1}{2}{3}'.format(self._base, '?type=op&action=cmd&cmd=<show><jobs><id>', jobId, '</id></jobs></show>')
        print(xpath)
        headers = self.headers()
        if self._sslVerify == False:
            response = self.get_request(xpath, headers, self._sslVerify)
        else:
            response = self.get_request(xpath, headers)
        _response_ = self.get_error(response)
        # Load XML response into XML Tree
        tree = ET.XML(_response_)
        # Check XML position for Job Status
        # Task will only wait if Pending, if job is completed, or failed it will exit the while loop
        while tree[0][0][8].text == 'PEND':
            print('Job still pending, waiting 90 seconds')
            # Wait 90 seconds if job was in a Pending State
            time.sleep(90)
            # Go retrieve the latest job status
            if self._sslVerify == False:
                response = self.get_request(xpath, headers, self._sslVerify)
            else:
                response = self.get_request(xpath, headers)
            _response_ = self.get_error(response)
            # Load latest response into tree to check status on next while loop
            tree = ET.XML(_response_)
        else:
            return(_response_)


    def deviceInstallLatestContentUpdate(self):
        # This function will install the latest Content Update
        xpath = '{0}{1}'.format(self._base, '?type=op&action=cmd&cmd=<request><content><upgrade><install><version>latest</version></install></upgrade></content></request>')
        # Print XPath to confirm it's correct
        print(xpath)
        # Retrieve Proper headers from base file
        headers = self.headers()
        # Check if you are using SSL Verify flag or not
        if self._sslVerify == False:
            response = self.get_request(xpath, headers, self._sslVerify)
        else:
            response = self.get_request(xpath, headers)
        _response_ = self.get_error(response)
        tree = ET.XML(_response_)
        ET.dump(tree)
        jobId = tree[0][1].text
        return(jobId)









            