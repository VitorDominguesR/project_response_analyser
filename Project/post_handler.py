import re

class responseHandler():

    def __init__(self, response_file):
        self.response_file = response_file
        self.http_method = ''
        self.resquest_path= ''
        self.protocol_version = ''
        self.headers = {}
        self.payload_dict = {}
        self.response_raw_splited = filter(None,response_file.replace('\r','').split('\n'))

    def get_signature_compare(self):
        response = self.response_file
        matches_regex = re.findall('(?<=\$).+?(?=\$)', response)
        return matches_regex


    def get_reponse_code(self):
        """Get the HTTP method, version """
        self.reponse_version, self.code, self.response_code_sig = re.split("(?<!\D)\s",self.response_raw_splited[0].replace('HTTP/',''))
        return self.reponse_version, self.code, self.response_code_sig

    def get_headers_reponse(self):
        """Get headers from request and parse to a dict"""
        for x in range(1,len(self.response_raw_splited)-1):
            values_and_keys = re.split(':(?:[\s\A])', self.response_raw_splited[x])
            if len(values_and_keys) > 1:
                key, value = values_and_keys
                self.headers[key] = value
            else:
                break
        return self.headers

    def get_page_content(self):
        """Get payload from requets"""
        self.content = re.split('(?<=\S)\n+(?=\s)', self.response_file.replace('\r',''))

        self.content = "\n".join(self.content[1:])
        return self.content
