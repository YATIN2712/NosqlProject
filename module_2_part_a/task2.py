import os
import re
import task1
import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen


###DEFINING TOKENS###
tokens = ('OPENBOLD', 'CLOSEBOLD', 'OPENSUP', 'CLOSESUP','TABLE2',
'OPENHREF', 'CLOSEHREF','CONTENT','OPENSPAN','CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 
'OPENSTYLE', 'CLOSESTYLE','GARBAGE','OPENIMG','OPENH3','CLOSEH3','OPENP','CLOSEP',
'OPENH4','CLOSEH4','OPENH2','CLOSEH2','OPENUL','CLOSEUL','OPENLI','CLOSELI')
t_ignore = '\t'	

###############Tokenizer Rules################

def t_TABLE2(t):
    r'<h2><span.class="mw-headline".id="Pandemic_chronology">Pandemic.chronology</span><span.class="mw-editsection">'
    return t

def t_OPENBOLD(t):
    r'<b[^>]*>'
    return t

def t_CLOSEBOLD(t):
    r'</b[^>]*>'
    return t

def t_OPENSUP(t):
    r'<sup[^>]*>'
    return t

def t_CLOSESUP(t):
    r'</sup[^>]*>'
    return t

def t_OPENH3(t):
    r'<h3[^>]*>'
    return t

def t_CLOSEH3(t):
    r'</h3[^>]*>'
    return t

def t_OPENH4(t):
    r'<h4[^>]*>'
    return t

def t_CLOSEH4(t):
    r'</h4[^>]*>'
    return t

def t_OPENH2(t):
    r'<h2[^>]*>'
    return t

def t_CLOSEH2(t):
    r'</h2[^>]*>'
    return t

def t_OPENP(t):
    r'<p[^>]*>'
    return t

def t_CLOSEP(t):
    r'</p[^>]*>'
    return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    return t

def t_CLOSEHREF(t):
    r'</a[^>]*>'
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9, -();:.\'/–-]+'
    return t

def t_OPENDIV(t):
    r'<div[^>]*>'
    return t

def t_CLOSEDIV(t):
    r'</div[^>]*>'
    return t

def t_OPENSTYLE(t):
    r'<style[^>]*>'
    return t

def t_CLOSESTYLE(t):
    r'</style[^>]*>'
    return t

def t_OPENSPAN(t):
    r'<span[^>]*>'
    return t

def t_CLOSESPAN(t): 
    r'</span[^>]*>'
    return t

def t_OPENIMG(t):
    r'<img[^>]*/>'
    return t

def t_OPENUL(t):
    r'<ul[^>]*>'
    return t

def t_CLOSEUL(t): 
    r'</ul[^>]*>'
    return t

def t_OPENLI(t):
    r'<li[^>]*>'
    return t

def t_CLOSELI(t): 
    r'</li[^>]*>'
    return t

def t_GARBAGE(t):
    r'<[^>]*>'

def t_error(t):
    t.lexer.skip(1)
####################################################################################################################################################################################################
											#GRAMMAR RULES
def p_start(p):
    '''start : table2'''
    p[0] = p[1]

def p_handleSup2(p):
    '''handleSup2 : OPENHREF CONTENT CLOSEHREF CLOSESUP skiptable2
                | skiptable2
                | '''

def p_printcontent2(p):
    '''printcontent2 : CONTENT
                    | '''

    if (len(p)==2):
        global news_list_latest
        news_list_latest.append(p[1])

def p_printmonthcontent(p):
    '''printmonthcontent : CONTENT
                        | '''

    if (len(p)==2):
        global news_list_latest
        news_list_latest.append("##########"+p[1]+"##########")

def p_printdatecontent(p):
    '''printdatecontent : CONTENT
                        | '''

    if (len(p)==2):
        global news_list_latest
        news_list_latest.append("#####"+p[1]+"#####")

def p_skiptable2(p):
    '''skiptable2 : printcontent2 skiptable2
               | OPENHREF skiptable2
               | CLOSEHREF skiptable2
               | OPENIMG skiptable2
               | OPENSPAN skiptable2
               | CLOSESPAN skiptable2
               | OPENDIV skiptable2
               | CLOSEDIV skiptable2
               | OPENBOLD skiptable2
               | CLOSEBOLD skiptable2
               | OPENSUP handleSup2
               | CLOSESUP skiptable2
               | OPENSTYLE skiptable2
               | CLOSESTYLE skiptable2
               | OPENUL skiptable2
               | CLOSEUL skiptable2
               | OPENLI skiptable2
               | CLOSELI skiptable2
               | OPENP skiptable2
               | CLOSEP skiptable2
               | OPENH3 OPENSPAN printmonthcontent CLOSESPAN skiptable2
               | OPENH4 OPENSPAN printdatecontent CLOSESPAN skiptable2
               | CLOSEH3 skiptable2
               | CLOSEH4 skiptable2
               | CLOSEH2 skiptable2
               | OPENH2
               | '''

def p_table2(p):
    '''table2 : TABLE2 skiptable2'''

def p_empty(p):
    '''empty :'''
    pass

def p_content(p):
    '''content : CONTENT
               | empty'''
    p[0] = p[1]

def p_error(p):
    #print(p.lineno,p.value)
    pass

#########DRIVER FUNCTION#######

news_list_latest=[]

def reset_lists():
    global news_list_latest
    news_list_latest = []

def preprocessing_latest(path,data,title):
    hash_positions = [i for i, entry in enumerate(data) if entry.startswith('##########')]
    for i in range(len(hash_positions)):
        if(i==len(hash_positions)-1):
            start_index = hash_positions[-1]
            current_data = data[start_index + 1:]
        else:
            start_index = hash_positions[i]
            end_index = hash_positions[i + 1]
            current_data = data[start_index + 1:end_index]

        new_title=title.copy()
        current_date = data[start_index]
        pattern = r'#{10}(\w+)#{10}'
        match = re.search(pattern, current_date)
        if match:
            month_name = match.group(1)
            new_title.insert(0,month_name)
        
        task1.preprocessing(path,current_data,new_title)

def main(path,title,link):
    #print(title)
    link="https://en.wikipedia.org"+link
    req = Request(link,headers ={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read()
    mydata = webpage.decode("utf8")
    web="webpage_"+title
    f=open(web,'w',encoding="utf-8")
    f.write(mydata)
    f.close()

    file_obj= open(web,'r',encoding="utf-8")
    data=file_obj.read()
    lexer = lex.lex()
    lexer.input(data)
    parser = yacc.yacc()
    parser.parse(data)
    file_obj.close()
    
    title=title.split()
    preprocessing_latest(path,news_list_latest,title)
        
    