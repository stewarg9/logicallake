# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 13:38:17 2020

@author: kbzg512
"""


from lxml import html
from bs4 import BeautifulSoup
from html import unescape  
from pathlib import Path



BASE_DIR = "C:\\Users\\kbzg512\\OneDrive - AZCollaboration\\Personal\\python\\hana_grammar\\"
RAW_DIR = BASE_DIR + "raw_html\\"
GRAMMAR_DIR = BASE_DIR + "grammar\\"


grammar = ""

paths = Path(RAW_DIR).glob('*.html')
for path in paths:
    # because path is object not string
    path_in_str = str(path)

    # Do thing with the path
    soup = BeautifulSoup(open(path, encoding='utf-8'), "html.parser")


    code_blocks = soup.findAll('div',{'class':'codeblock-wrapper'})


    for code_block in code_blocks:
        
        grammar += code_block.text + "\n\n"
        
        bnf_text = unescape(code_block.text)
        
#        if bnf_text.strip()[0] == '<': 
        
#            grammar += bnf_text
    
        #else:
            
#            grammar += "\nNOT_VALID:" +  bnf_text + "|NOT VALID/n"


with open(GRAMMAR_DIR + "SAP_SQL.bnf", 'w',encoding='utf-8') as f:
   f.write(grammar)  