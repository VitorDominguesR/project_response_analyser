# -*- coding:utf8 -*-

from post_handler import responseHandler
import difflib
import re
from difflib import *


class attacksTest():

    def __init__(self,r, attackName = ''):
        self.r = r
        self.attack_name = attackName

    def xssTest(self, attack_signature):

        if type(attack_signature) is str:
            # print 'str é o que há'
            if attack_signature in self.r.content:
                return "Vulnerable"
            else:
                return "Not vulnerable"
        elif type(attack_signature) is list:
            attack_count = 0
            for element in attack_signature:
                if element in self.r.content:
                    attack_count += 1
                else:
                    pass
            if attack_count > 0:
                return "Vulnerable"
            else:
                return "Not Vulnerable"

    def errorHandlingTest(self, attack_signature):

        if type(attack_signature) is str:
            # print 'str é o que há'
            if attack_signature in self.r.content or attack_signature in self.r.status_code:
                return "Vulnerable"
            else:
                return "Not vulnerable"
        elif type(attack_signature) is list:
            attack_count = 0
            for element in attack_signature:
                if element in self.r.content or element in str(self.r.status_code):
                    attack_count += 1
                else:
                    pass
            if attack_count > 0:
                return "Vulnerable"
            else:
                return "Not Vulnerable"

    def serviceBannerTest(self, attack_signature):
        attack_count = 0
        for key, value in self.r.headers.items():
            if type(attack_signature) is str:
                # print 'str é o que há'
                if attack_signature in value:
                    return "Vulnerable"
                else:
                    return "Not vulnerable"
            elif type(attack_signature) is list:
                for element in attack_signature:
                    if element in value:
                        attack_count += 1
                    else:
                        pass
        if attack_count > 0:
            return "Vulnerable"
        else:
            return "Not Vulnerable"

    def testCORS(self, attack_signature):
        attack_count = 0
        for key, value in self.r.headers.items():
            if type(attack_signature) is str:
                # print 'str é o que há'

                if attack_signature in value and 'allow' in key.lower():
                    return "Vulnerable"
                else:
                    return "Not vulnerable"
            elif type(attack_signature) is list:
                for element in attack_signature :
                    if element in value and 'allow-origin' in key.lower():
                        attack_count += 1
                    else:
                        pass
        if attack_count > 0:
            return "Vulnerable"
        else:
            return "Not Vulnerable"

    def testSecureCookie(self,attack_signature):
        attack_count = 0
        for cookie in self.r.cookies:
            if not cookie.secure:
                attack_count += 1
            else:
                pass
        if attack_count > 0:
            return "Vulnerable"
        else:
            return "Not Vulnerable"

    def testHttpOnlyCookie(self,attack_signature):
        has_httponly = False
        for cookie in self.r.cookies:
            print cookie._rest.keys()
            for x in cookie._rest.keys():
                if 'httponly' in x.lower():
                    has_httponly = True

        if not has_httponly:
            return "Vulnerable"
        else:
            return "Not Vulnerable"

    def compareResponses(self, response):
        self.chanded = []
        self.response_handler = responseHandler(response)
        d = difflib.Differ()
        self.chanded.append("########################INICIO########################\n\nVulnerability Name:%s\n\n"%self.attack_name.upper().replace("_"," "))

        #self.response_handler.get_reponse_code()[1]
        self.reponse_code_txt = self.response_handler.get_reponse_code()[1]
        if self.reponse_code_txt == self.r.status_code:
            pass
        else:
            self.chanded.append("status code chaged to:%s\nOld value:%s\n\n"%(self.r.status_code,self.reponse_code_txt))

        dict_reponse_file = self.response_handler.get_headers_reponse()
        dict_reponse_newrequest = self.r.headers

        for key_reponsetxt in dict_reponse_file.keys():
            if key_reponsetxt in dict_reponse_newrequest.keys():
                if dict_reponse_newrequest[key_reponsetxt] == dict_reponse_file[key_reponsetxt]:
                    pass
                else:
                    self.chanded.append("The value of header '%s' changed.\nNew value: %s \nOld value: %s\n\n"%(key_reponsetxt,
                                                                                                         dict_reponse_newrequest[key_reponsetxt],
                                                                                                         dict_reponse_file[key_reponsetxt]))
            else:
                self.chanded.append("the header %s is not in this request" %key_reponsetxt)

        content_response_txt_temp = filter(None, self.response_handler.get_page_content().split('\n'))
        content_response_new_temp = filter(None, self.r.content.replace('\r','').split('\n'))

        content_response_txt = [y.strip() for y in content_response_txt_temp]
        content_response_new = [x.strip() for x in content_response_new_temp]

        # print content_response_txt
        # print content_response_new

        diff = d.compare(content_response_txt, content_response_new )

        pattern_match = re.compile('(^\-\s|^\+\s|^\?\s)', re.MULTILINE)

        diff = "\n".join(diff)
        #print diff
        if re.match(pattern_match, diff):
            self.chanded.append("The content has changed: \n%s\n"%diff)
        else:
            pass
        self.chanded.append("########################FIM########################\n\n")
        return self.chanded





    def runTests(self,attack_signature, attack_name):
        self.results = ''
        self.attack_name = attack_name.lower()
        if "xss" in self.attack_name or "cross_site_scripting" in self.attack_name:
            self.results = attack_name +':' +self.xssTest(attack_signature)
        elif "error_handling" in self.attack_name:
            self.results = attack_name + ':' + self.errorHandlingTest(attack_signature)
        elif "service_banner_enabled" in self.attack_name:
            self.results = attack_name + ':' + self.serviceBannerTest(attack_signature)
        elif "overly_permissive" in self.attack_name:
            self.results = attack_name + ':' + self.testCORS(attack_signature)
        elif "without_secure_flag" in self.attack_name:
            self.results = attack_name + ':' + self.testSecureCookie(attack_signature)
        elif "without_httponly_flag" in self.attack_name:
            self.results = attack_name + ':' + self.testHttpOnlyCookie(attack_signature)
        return self.results

