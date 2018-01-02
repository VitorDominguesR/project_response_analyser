# -*- coding:utf8 -*-

import re
import requests
from urllib import unquote

class HTTPRequestHandler():

    def __init__(self, request_raw):
        self.raw_request = request_raw.replace("\r", "")
        self.http_method = ''
        self.resquest_path= ''
        self.protocol_version = ''
        self.headers = {}
        self.payload_dict = {}
        self.payload = self.raw_request.split('\n\n')[1]
        self.request_raw_splited = filter(None,self.raw_request.split('\n\n')[0].replace('\r','').split('\n'))

    def get_http_method_path_version(self):
        """Get the HTTP method, version """
        self.http_method, self.resquest_path, self.protocol_version = self.request_raw_splited[0].replace('HTTP/','').split(' ')
        return self.http_method, self.resquest_path, self.protocol_version

    def get_headers(self):
        """Get headers from request and parse to a dict"""
        for x in range(1,len(self.request_raw_splited)):
            y = re.split(':\s', self.request_raw_splited[x])
            if len(y)<2:
                #print y
                pass
            else:
                key, value = y[0],y[1]
                self.headers[key] = value
        #print repr(self.get_raw_requets())
        return self.headers

    def get_payload(self):
        """Get payload from requets"""
        #print self.payload
        if 'urlencoded' in self.get_headers()['Content-Type']:
            try:
                self.payload = self.payload.split('&')
                for element in self.payload:
                    element = element.split('=')
                    self.payload_dict[element[0]] = unquote(element[1]).decode('utf8')
                return self.payload_dict, "&".join(self.payload)#self.request_raw_splited[-1])
            except:
                return self.payload
        else:
            return self.payload

    def get_raw_requets(self):
        return repr(self.raw_request)


# Using this new class is really easy! =)

