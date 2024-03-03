import os
import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
import html
import extract_data

tokens = ('BEGINTABLE','GARBAGE','OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW','OPENBODY',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN'
,'CLOSESPAN', 'OPENDIV', 'CLOSEDIV','OPENSUP','CLOSESUP')

t_ignore = '\t'
headings = []
countries = []
key = []
def t_BEGINTABLE(t):
    r'<table.id="main_table_countries_yesterday"[^>]*>'
    return t

def t_OPENBODY(t):
    r'<tbody[^>]*>'
    return t

def t_OPENSUP(t):
	r'<sup[^>]*>'
	return t

def t_OPENTABLE(t):
    r'<tbody[^>]*>'
    return t
 
def t_CLOSETABLE(t):
    r'</tbody[^>]*>'
    return t

def t_CLOSESUP(t):
	r'</sup>'
	return t

def t_OPENROW(t):
    r'<tr[^>]*>'
    return t
 
def t_CLOSEROW(t):
    r'</tr[^>]*>'
    return t

def t_OPENHEADER(t):
    r'<th\b[^>]*>'
    return t
 
def t_CLOSEHEADER(t):
    r'<\/th\b[^>]*>'
    return t

def t_OPENSPAN(t):
    r'<span[^>]*>'
    return t
 
def t_CLOSESPAN(t):
    r'</span[^>]*>'
    return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    return t
 
def t_CLOSEHREF(t):
    r'</a[^>]*>'
    return t
 
def t_OPENDATA(t):
    r'<td[^>]*>'
    return t
 
def t_CLOSEDATA(t):
    r'</td[^>]*>'
    return t
 
def t_CONTENT(t):
    r'[A-Za-z0-9,\.\-\/#\ ]+'
    return t


 
def t_OPENDIV(t):
    r'<div[^>]*>'
    return t
 
def t_CLOSEDIV(t):
    r'</div[^>]*>'
    return t

def t_GARBAGE(t):
    r'<[^>]*>'
    return t

def t_error(t):
    t.lexer.skip(1)


def p_start(p):
    '''start : BEGINTABLE table'''

def p_table(p):
    '''table : skip OPENROW handleheader CONTENT CLOSEROW'''

def p_skip(p):
    '''skip : CONTENT skip
            | GARBAGE skip
            | '''

def p_handleheader(p):
    '''handleheader : skip OPENHEADER handleheadercontent CLOSEHEADER handleheader
                    | '''

def p_handleheadercontent(p):
    '''handleheadercontent :  CONTENT 
                           | CONTENT CONTENT
                           | CONTENT GARBAGE CONTENT 
                           | CONTENT CONTENT CONTENT GARBAGE CONTENT 
                           | CONTENT GARBAGE CONTENT GARBAGE CONTENT GARBAGE CONTENT
                           | '''
    global headings
    if len(p) == 2:
        headings.append(p[1])
    elif len(p) == 3:
        headings.append(p[1]+p[2])
    elif len(p) == 4:
        headings.append(p[1]+p[3])
    elif len(p) == 6:
        headings.append(p[1]+p[3]+p[5])
    elif len(p) == 8:
        headings.append(p[1]+p[5])

def p_error(p):
    pass
    

def read_countries(filename):
    continents = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and '--------' not in line:
                continents.append(line)
        continents = [place.replace(":", "") for place in continents]

    return list(set(continents))

def collect_data(countries_dict):
    url = 'https://www.worldometers.info/coronavirus/'
    req = Request(url,headers ={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read().decode('utf-8')
    with open('webpage.html', 'w', encoding='utf-8') as file:
        file.write(webpage)
    lexer = lex.lex()
    lexer.input(webpage)
    # with open("extract_tokens.txt","w",encoding="utf-8") as file:
    # 	for tok in lexer:
    # 		file.write(str(tok)+'\n')
    
    
    parser = yacc.yacc()
    parser.parse(webpage)
    global headings
    extract_data.main(headings,countries_dict)

    



def main():

    filename = "worldometers_countrylist.txt"
    countries_dict = read_countries(filename)
    collect_data(countries_dict)


if __name__ == '__main__':
    main()



