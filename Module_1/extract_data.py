import os
import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
import html

tokens = ('BEGINTABLE','GARBAGE','OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW','OPENBODY',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN'
,'CLOSESPAN', 'OPENDIV', 'CLOSEDIV','OPENSUP','CLOSESUP')

t_ignore = '\t'
countries = []
key = []
links = []
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
    '''start : BEGINTABLE skipall OPENBODY body '''
    
def p_body(p):
    '''body : handlerow '''

def p_handlerow(p):
    '''handlerow : skip OPENROW handlecontent CLOSEROW handlerow
                 | skip '''
def p_handlecontent(p):
    '''handlecontent : skip OPENDATA handledata CLOSEDATA handlecontent
                     | skip '''


def p_skipall(p):
    '''skipall : CONTENT skipall
               | GARBAGE skipall
               | OPENROW skipall
               | CLOSEROW skipall
               | OPENHEADER skipall 
               | CLOSEHEADER skipall
               | '''

def is_alphanumberic(s):
    s_without_commas = s.replace(",", "")
    
    # Check if the string is numeric (ignoring commas)
    if s_without_commas.isdigit():
        return False
    
    # Check if the string is alphanumeric
    if s_without_commas.isalnum():
        return True
    
    # If the string is neither numeric nor alphanumeric
    return False

def p_handledata(p):
    '''handledata : CONTENT 
                  | CONTENT GARBAGE CONTENT GARBAGE CONTENT
                  | CONTENT GARBAGE GARBAGE CONTENT
                  | OPENHREF CONTENT CLOSEHREF
                  | OPENSPAN CONTENT CLOSESPAN
                  | OPENHREF CONTENT CLOSEHREF CONTENT
                  | OPENHREF CONTENT CONTENT CONTENT CLOSEHREF
                  | CONTENT CONTENT
                  | '''
    # print("data")
    global countries
    global key,links
    if len(p) == 1 or (len(p) == 5 and p.slice[1].type == 'CONTENT'):
        countries.append(" ")
    elif len(p) == 2:
        if p[1] == 'World':
            key.append(p[1])
        countries.append(p[1])
    elif len(p) == 6 and p.slice[1].type == 'CONTENT':
        key.append(p[3])
        countries.append(p[3])
    elif len(p) == 6 and p.slice[1].type == 'OPENHREF':
        links.append(p[1])
        if p[2] == "R":
            countries.append("Réunion")
            key.append("Réunion")
        elif p[2] == 'C':
            countries.append("Curaçao")
            key.append("Curaçao")

    elif len(p) == 4:
        links.append(p[1])
        if is_alphanumberic(p[2]):
            key.append(p[2])
        countries.append(p[2])
    elif len(p) == 3:
        countries.append(p[1]+p[2])
    elif len(p) == 5:
        countries.append(p[2])


    
    

def p_skip(p):
    '''skip : CONTENT skip
            | GARBAGE skip
            | '''





def p_error(p):
    pass
    





def main(headings,countries_dict):
    url = 'https://www.worldometers.info/coronavirus/'
    req = Request(url,headers ={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read().decode('utf-8')
    lexer = lex.lex()
    lexer.input(webpage)
    parser = yacc.yacc()
    parser.parse(webpage)
    global countries,key
    
    countries_dict.append('World')
    required_heading = ['TotalCases','ActiveCases','TotalDeaths','TotalRecovered','TotalTests','Deaths/1M pop','Tests/1M pop','NewCases','NewDeaths','NewRecovered']
    for v in countries_dict:
        if v in countries:
            index_v = countries.index(v)
            v_list = countries[max(0,index_v-1): min(index_v+21,len(countries))]
            filename = f'Data/{v}.txt'
            with open(filename,'w') as file:
                for k , val in zip(headings,v_list):
                    if k in required_heading:
                        val = val.replace(",","")
                        file.write(f'{k},{val}\n')
            file.close()
    
    while(True):
        q_country = input("Enter for which country/continent/World you want to extract data:")
        if q_country not in countries_dict:
            print("Country/continent/World not in the list")
            break
        q_val = int(input("Enter number of which query you want\n1.Active Cases\n2.New Death\n3.New Recovered\n4.New Cases\n"))
        query = None
        if q_val == 1:
            query = 'ActiveCases'
        elif q_val == 2:
            query = 'NewDeaths'
        elif q_val == 3:
            query = 'NewRecovered'
        elif q_val == 4:
            query = 'NewCases'
        else:
            print("wrong number entered")
            break

        filename = f'Data/{q_country}.txt'
        with open(filename,'r') as  file:
            for line in file:
                k,v = line.strip().split(",")
                if k == query:
                    print(query,v)
        
        con = int(input("Enter 1 to continue else enter 0 to exit"))
        if con == 0:
            break
                
                





