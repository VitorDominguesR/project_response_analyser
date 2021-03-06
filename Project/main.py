#!/usr/bin/python
# -*- coding:utf-8 -*-

from my_request_handler import HTTPRequestHandler
import requests
import post_handler
import os
from attacks_tests import attacksTest
import xml.etree.ElementTree as ET



# print "################################ Escolha uma opção ################################"
# print "[1] Realizar resteste"
# print "[2] Configurar setup"

http_proxy = "http://127.0.0.1:8080"
https_proxy = "https://127.0.0.1:8080"

proxyDict = {
    "http" : http_proxy,
    "https" : https_proxy
}

def teste_attack(path_vulns=""):

    cookies_provided = raw_input("Insira seus cookies (Exp.: cookie1=valor1;cookie2=valor2;..) ou aperte Enter\n").strip()
    
    if len(cookies_provided)<=0:
        print "Não foram inseridos cookies"
    else:
        cookies_dict = get_inserted_cookies(cookies_provided)

    #identifica o caminho que os arquivos das vulnerabilidades estão
    print os.path.dirname(os.path.abspath(__file__))
    if path_vulns == "":
        vulns_dirs = next(os.walk(os.path.dirname(os.path.abspath(__file__))))[1]
    else:
        vulns_dirs = vulns_dirs = next(os.walk(os.path.dirname(path_vulns)))[1]
    attack_results = []
    

    for dir in vulns_dirs:
        error = False
        attack_signature = [] # sempre vai ser uma lista

        # pede o caminho que os arquivos gerados pelo EGV manager estão
        path_file_request = raw_input("Digite o caminho do arquivo que contenha a requisição desejada (Default: %s/request_%s): "%(dir,dir))
        path_file_response = ""
        if path_file_request == "":
            path_file_request = path_vulns + dir + '/request_'+dir
            path_file_response = path_vulns + dir +'/response_'+dir

        # try:
        #     vuln_config_file = ET.parse(dir+'/vuln.config').getroot()
        #
        #     for element in vuln_config_file.findall('attackPattern'):
        #         attack_signature.append(element.text) # posso usar o strip
        # except:
        #     print "It was not possible to read 'vuln.config' file"
        try:
            request_file = open(path_file_request,'r').read()
        except Exception as e:
            print path_file_request
            print "o arquivo %s nao existe" % path_file_request
            print e
            error = True

        if not error:
            #faz o parse dos arquivo de requisição e o le
            request_field = HTTPRequestHandler(request_file)
            reponse_file=open(path_file_response,'r').read()


            #reponse_parser = post_handler.responseHandler(reponse_file)
            #print reponse_parser.get_reponse_code(), reponse_parser.get_headers_reponse(), reponse_parser.get_page_content()

            # pega o método http utilizado, o caminho da url e a versão do HTTP
            request_method, request_path, request_http_version = request_field.get_http_method_path_version()

            #dict_params_in_request = request_field.get_payload()[0]
            #print request_field.get_headers()

            #pega os cabeçalhos originais da requisição
            request_headers = request_field.get_headers()
            #print request_headers


            #print request_path
            request_payload = ''

            #attack_signature = '<script>alert(90)</script>'

            # print attack_signature
            # if not attack_signature:
                # try:
                #     response_params = post_handler.responseHandler(reponse_file).get_signature_compare()
                # except:
                #     response_params = []
                #
                # if len(response_params) > 0:
                #     choice =  raw_input("Foram detectados parametros para serem usados como assinaturas de ataque. Deseja us-los ?[S/n]").lower()
                #     if choice == '':
                #         choice = 's'
                #     if choice == 's':
                #         attack_signature = response_params
                #     else:
                #         attack_signature = raw_input("Digite uma assinatura de ataque: ").split(',')
                # else:
                #     attack_signature = raw_input("Digite uma assinatura de ataque: ").split(',')
                #
                # print attack_signature

            #monta a url da requisição
            try:
                url = 'https://'+request_headers['Host'] + request_path

                #verifica qual metodo está sendo utilizado
                if not cookies_provided:
                    if request_method == "POST":
                        request_payload = request_field.get_payload()[1]
                        r = requests.post(url, data=request_payload, headers=request_headers, timeout = 20)#, proxies=proxyDict)
                    elif request_method == "GET":
                        if request_payload == '':
                            #print request_headers
                            r = requests.get(url, headers=request_headers, timeout=20)#, verify=False)#, proxies=proxyDict)
                        else:
                            r = requests.get(url, data=request_payload,headers=request_headers, timeout=20)#, verify=False)#, proxies=proxyDict)

                    elif request_method == "OPTIONS":
                        r = requests.options(url)
                else:
                    request_headers.pop('Cookies', None)
                    if request_method == "POST":
                        request_payload = request_field.get_payload()[1]
                        r = requests.post(url, data=request_payload, headers=request_headers,
                                          cookies=cookies_dict,timeout=20,verify=False, proxies=proxyDict)
                    elif request_method == "GET":
                        if request_payload == '':
                            # print request_headers
                            r = requests.get(url, headers=request_headers,cookies=cookies_dict, timeout=20)  # , proxies=proxyDict)
                        else:
                            r = requests.get(url, data=request_payload,cookies=cookies_dict, headers=request_headers,
                                             timeout=20)  # , proxies=proxyDict)

                    elif request_method == "OPTIONS":
                        r = requests.options(url,cookies=cookies_dict)

                attack_tests = attacksTest(r,dir)

                #attack_results.append(attack_tests.runTests(attack_signature, dir))
                attack_results.append(attack_tests.compareResponses(reponse_file))
                #print r.text
            except:
                url = 'https://' + request_headers['Host'] + request_path

                # verifica qual metodo está sendo utilizado
                if not cookies_provided:
                    if request_method == "POST":
                        request_payload = request_field.get_payload()[1]
                        r = requests.post(url, data=request_payload, headers=request_headers,
                                          timeout=20 , proxies=proxyDict)
                    elif request_method == "GET":
                        if request_payload == '':
                            # print request_headers
                            r = requests.get(url, headers=request_headers, timeout=20,
                                             verify=False)  # , proxies=proxyDict)
                        else:
                            r = requests.get(url, data=request_payload, headers=request_headers, timeout=20,
                                             verify=False)  # , proxies=proxyDict)

                    elif request_method == "OPTIONS":
                        r = requests.options(url)
                else:
                    request_headers.pop('Cookies', None)
                    if request_method == "POST":
                        request_payload = request_field.get_payload()[1]
                        r = requests.post(url, data=request_payload, headers=request_headers,
                                          cookies=cookies_dict, timeout=20, proxies=proxyDict)
                    elif request_method == "GET":
                        if request_payload == '':
                            # print request_headers
                            r = requests.get(url, headers=request_headers, cookies=cookies_dict,
                                             timeout=20, verify=False,proxies=proxyDict)
                        else:
                            r = requests.get(url, data=request_payload, cookies=cookies_dict, headers=request_headers,
                                             timeout=20 ,verify=False, proxies=proxyDict)

                    elif request_method == "OPTIONS":
                        r = requests.options(url, cookies=cookies_dict)

                attack_tests = attacksTest(r, dir)

                # attack_results.append(attack_tests.runTests(attack_signature, dir))
                attack_results.append(attack_tests.compareResponses(reponse_file))
                # print r.text

        else:
            pass
    for results in attack_results:
        print "\n".join(results)


    # print r.status_code
    #print r.headers
    # print r.text

    #print "A assinatura a ser testada e: " + ",".join(attack_signature)

    #print type(attack_signature)

    # if type(attack_signature) is str:
    #     #print 'str é o que há'
    #     if attack_signature in r.content:
    #         print "Está vulnerável à XSS"
    #     else:
    #         print "Não está vulneravel"
    # elif type(attack_signature) is list:
    #     attack_count = 0
    #     for element in attack_signature:
    #         if element in r.content:
    #             attack_count += 1
    #         else:
    #             pass
    #     if attack_count > 0:
    #         print "Vulneravel"
    #     else:
    #         print "Não está vulnerável"

def get_inserted_cookies(cookies_str):
    cookies_string = filter(None, cookies_str.split(';'))
    dict_cookies = {}
    #url = 'http://httpbin.org/cookies'

    #print cookies_string

    for cookies in cookies_string:
        cookies = cookies.split("=")
        print cookies

        dict_cookies[cookies[0]] = cookies[1]

    return dict_cookies


if __name__ == "__main__":
    teste_attack('/media/veracrypt1/Relatorio/teste_conecta/PTManager/')
