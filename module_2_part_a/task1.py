import os
import re
import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen


###DEFINING TOKENS###
tokens = ('BEGINTABLE','OPENBOLD', 'CLOSEBOLD', 'OPENSUP', 'CLOSESUP',
'OPENHREF', 'CLOSEHREF','CONTENT','OPENSPAN','CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 
'OPENSTYLE', 'CLOSESTYLE','GARBAGE','OPENIMG','OPENH3','CLOSEH3','OPENP','CLOSEP',
'OPENH4','CLOSEH4','OPENH2','CLOSEH2','OPENUL','CLOSEUL','OPENLI','CLOSELI','BEFORE')
t_ignore = '\t'	

###############Tokenizer Rules################
def t_BEGINTABLE(t):
    r'<span.class="mw-headline".id="Pandemic_chronology">Pandemic.chronology</span>'
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

def t_BEFORE(t):
    r'::before'
    return t

def t_GARBAGE(t):
    r'<[^>]*>'

def t_error(t):
    t.lexer.skip(1)
####################################################################################################################################################################################################
											#GRAMMAR RULES
def p_start(p):
    '''start : table'''
    p[0] = p[1]

def p_printcontent(p):
    '''printcontent : CONTENT
                    | '''
    if(len(p)==2):
        global news_list
        news_list.append(p[1])
        
def p_printheadcontent(p):
    '''printheadcontent : CONTENT
                        | '''

    if (len(p)==2):
        global news_list
        news_list.append("#####"+p[1]+"#####")

def p_skiptag(p):
    '''skiptag : printcontent skiptag
               | OPENHREF skiptag
               | CLOSEHREF skiptag
               | OPENIMG skiptag
               | OPENSPAN skiptag
               | CLOSESPAN skiptag
               | OPENDIV skiptag
               | CLOSEDIV skiptag
               | OPENBOLD skiptag
               | CLOSEBOLD skiptag
               | OPENSUP handleSup
               | CLOSESUP skiptag
               | OPENH4 skiptag
               | CLOSEH4 skiptag
               | OPENSTYLE skiptag
               | CLOSESTYLE skiptag
               | OPENUL skiptag
               | CLOSEUL skiptag
               | OPENLI skiptag
               | CLOSELI skiptag
               | OPENP skiptag
               | CLOSEP skiptag
               | CLOSEH3 skiptag
               | OPENH3 OPENSPAN printheadcontent CLOSESPAN skiptag
               | OPENH3 OPENSPAN CLOSESPAN OPENSPAN printheadcontent CLOSESPAN CLOSEH3 skiptag
               | CLOSEH2 skiptag
               | BEFORE skiptag
               | OPENH2
               | '''

def p_handleSup(p):
    '''handleSup : OPENHREF CONTENT CLOSEHREF CLOSESUP skiptag
                | skiptag
                | '''
def p_table(p):
    '''table : BEGINTABLE skiptag'''

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

news_list=[]

def reset_lists():
    global news_list
    news_list = []

def preprocessing(path,data,title):
    if data is None:
        return 0
    datewise_data = {}
    hash_positions = [i for i, entry in enumerate(data) if entry.startswith('#####')]
    for i in range(len(hash_positions)):
        if(i==(len(hash_positions)-1)):
            start_index = hash_positions[-1]
            current_data = data[start_index + 1:]
        else:
            start_index = hash_positions[i]
            end_index = hash_positions[i + 1]
            current_data = data[start_index + 1:end_index]

        current_date = data[start_index]
        cleaned_data = [re.sub(r'<.*?>', '', word) for word in current_data if not word.startswith(('&#','.','edit'))]
        cleaned_data = re.sub(r'\s+', ' ', ' '.join(cleaned_data)).strip()
        datewise_data[current_date] = cleaned_data

    title='_'.join(title)
    output_file = os.path.join(path,title+'.txt')
    with open(output_file, 'w', encoding='utf-8') as file:
        year=(title.split('_'))[-1]
        for date, data in datewise_data.items():
            date=(date.strip())
            date=date[:-5]+' '+year+date[-5:]
            file.write(date + '\n')
            file.write(data + '\n')

def main(path,title,link):
    
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
    preprocessing(path,news_list,title)