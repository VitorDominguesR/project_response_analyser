# -*- coding:utf8 -*-

import re
import requests
from urllib import unquote

class HTTPRequestHandler():

    def __init__(self, request_raw):
        self.http_method = ''
        self.resquest_path= ''
        self.protocol_version = ''
        self.headers = {}
        self.payload_dict = {}
        self.request_raw_splited = filter(None,request_raw.replace('\r','').split('\n'))

    def get_http_method_path_version(self):
        """Get the HTTP method, version """
        self.http_method, self.resquest_path, self.protocol_version = self.request_raw_splited[0].replace('HTTP/','').split(' ')
        return self.http_method, self.resquest_path, self.protocol_version

    def get_headers(self):
        """Get headers from request and parse to a dict"""
        for x in range(1,len(self.request_raw_splited)-1):
            key, value = re.split(':(?:[\s])', self.request_raw_splited[x])
            self.headers[key] = value
        return self.headers

    def get_payload(self):
        """Get payload from requets"""
        self.payload = self.request_raw_splited[-1]
        if 'urlencoded' in self.get_headers()['Content-Type']:
            self.payload = self.payload.split('&')
            for element in self.payload:
                element = element.split('=')
                self.payload_dict[element[0]] = unquote(element[1]).decode('utf8')
            return self.payload_dict, self.request_raw_splited[-1]
        else:
            return -1




# Using this new class is really easy! =)

