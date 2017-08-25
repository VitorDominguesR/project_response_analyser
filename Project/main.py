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

print os.path.dirname(os.path.abspath(__file__))
vulns_dirs = next(os.walk(os.path.dirname(os.path.abspath(__file__))))[1]
attack_results = []
for dir in vulns_dirs:
    attack_signature = [] # sempre vai ser uma lista

    path_file_request = raw_input("Digite o caminho do arquivo que contenha a requisição desejada (Default: %s/request.txt): "%dir)
    path_file_response = ""
    if path_file_request == "":
        path_file_request = dir+'/request.txt'
        path_file_response = dir + '/response.txt'

    try:
        vuln_config_file = ET.parse(dir+'/vuln.config').getroot()

        for element in vuln_config_file.findall('attackPattern'):
            attack_signature.append(element.text) # posso usar o strip
    except:
        print "It was not possible to read 'vuln.config' file"


    request_file = open(path_file_request,'r').read()
    request_field = HTTPRequestHandler(request_file)

    reponse_file=open(path_file_response,'r').read()
    #reponse_parser = post_handler.responseHandler(reponse_file)

    #print reponse_parser.get_reponse_code(), reponse_parser.get_headers_reponse(), reponse_parser.get_page_content()


    request_method, request_path, request_http_version = request_field.get_http_method_path_version()
    #dict_params_in_request = request_field.get_payload()[0]
    request_headers = request_field.get_headers()
    request_payload = ''

    #attack_signature = '<script>alert(90)</script>'

    url = 'http://'+request_headers['Host'] + request_path

    print attack_signature
    if not attack_signature:
        try:
            response_params = post_handler.responseHandler(reponse_file).get_signature_compare()
        except:
            response_params = []

        if len(response_params) > 0:
            choice =  raw_input("Foram detectados parametros para serem usados como assinaturas de ataque. Deseja us-los ?[S/n]").lower()
            if choice == '':
                choice = 's'
            if choice == 's':
                attack_signature = response_params
            else:
                attack_signature = raw_input("Digite uma assinatura de ataque: ").split(',')
        else:
            attack_signature = raw_input("Digite uma assinatura de ataque: ").split(',')

        print attack_signature

    if request_method == "POST":
        request_payload = request_field.get_payload()[1]
        r = requests.post(url, data=request_payload, headers=request_headers)
    elif request_method == "GET":
        if request_payload == '':
            #print request_headers
            r = requests.get(url, headers=request_headers)
        else:
            r = requests.get(url, data=request_payload,headers=request_headers)

    elif request_method == "OPTIONS":
        r = requests.options(url)


    attack_tests = attacksTest(r,dir)

    #attack_results.append(attack_tests.runTests(attack_signature, dir))
    attack_results.append(attack_tests.compareResponses(reponse_file))

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