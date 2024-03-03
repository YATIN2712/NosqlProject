import os
import ply.lex as lex
import ply.yacc as yacc
import re
from urllib.request import Request, urlopen

import task1
import task2

req = Request('https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic',headers ={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()
mydata = webpage.decode("utf8")
f=open('webpage.html','w',encoding="utf-8")
f.write(mydata)
f.close()

###DEFINING TOKENS###
tokens = ('BEGINTABLE', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENSPAN',
'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE','GARBAGE',
'OPENIMG','OPENLIST','CLOSELIST','OPENUL','CLOSEUL')
t_ignore = '\t'	

###############Tokenizer Rules################
def t_BEGINTABLE(t):
     r'<p>The.following.are.the.timelines.of.the.COVID-19.pandemic.respectively.in:.\n</p>'
     return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    return t

def t_CLOSEHREF(t):
    r'</a[^>]*>'
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9, ]+'
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

def t_OPENUL(t):
    r'<ul[^>]*>'
    return t

def t_CLOSEUL(t): 
    r'</ul[^>]*>'
    return t

def t_OPENLIST(t):
    r'<li[^>]*>'
    return t

def t_CLOSELIST(t): 
    r'</li[^>]*>'
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

def t_GARBAGE(t):
    r'<[^>]*>'

def t_error(t):
    t.lexer.skip(1)

####################################################################################################################################################################################################
											#GRAMMAR RULES

def p_start(p):
    '''start : table'''
    p[0] = p[1]

def p_skiptag(p):
    '''skiptag : CONTENT skiptag
               | OPENIMG skiptag
               | OPENSPAN skiptag
               | CLOSESPAN skiptag 
               | OPENDIV skiptag
               | CLOSEDIV skiptag
               | '''

def p_printhref(p):
    '''printhref    : OPENHREF
                    | '''
    global timeline_links
    timeline_links.append(p[1])

def p_dataCell(p):
    '''dataCell : OPENLIST skiptag printhref CONTENT CLOSEHREF CLOSELIST dataCell
                | OPENLIST skiptag OPENUL dataCell CLOSEUL CLOSELIST dataCell
		        | '''

def p_table(p):
    '''table : BEGINTABLE OPENUL dataCell CLOSEUL'''

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

def get_link(href_values):

    current_dir = os.getcwd()
    path = os.path.join(current_dir,'Timeline_news')
    os.makedirs(path, exist_ok=True)

    years_ex=['2023','2024']
    for href_value in href_values:
        link_match = re.search(r'href="([^"]+)"', href_value)
        title_match = re.search(r'title="Timeline of the COVID-19 pandemic in (\w+(?: \d+)?)', href_value)
        if link_match and title_match:
            link = link_match.group(1)
            title = title_match.group(1)

        task1.reset_lists()
        task2.reset_lists()
        title=title.split()

        if(title[-1] in years_ex):
            task2.main(path,title[-1],link)
        else:
            title=' '.join(title)
            task1.main(path,title,link)

timeline_links=list()
def main():
    file_obj= open('webpage.html','r',encoding="utf-8")
    data=file_obj.read()
    lexer = lex.lex()
    lexer.input(data)
    parser = yacc.yacc()
    parser.parse(data)
    file_obj.close()

if __name__ == '__main__':
    main()
    get_link(timeline_links)