#!/usr/bin/env python
# encoding: utf-8

# pip install translate
from translate import Translator
import subprocess



def translate_zh_to_en(content):
    # from zh to en
    translator= Translator(from_lang='zh',to_lang="en")
    translation = translator.translate(content)
    return translation


def howdoi_zh(content_zh):
    content_en = translate_zh_to_en(content_zh)
    command = ["howdoi","-a",content_en]
    answer = subprocess.check_output(command)
    #return answer
    print(answer)
    return answer

if __name__ == '__main__':
    query = u"如何学python"
    howdoi_zh(query.encode('utf-8'))
    #query = "如何学python"
    #howdoi_zh(query)
