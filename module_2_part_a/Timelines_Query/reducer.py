import sys
import re

from datetime import datetime

def is_date_in_range(start_date_str, end_date_str, check_date_str):
    start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
    end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
    check_date = datetime.strptime(check_date_str, "%d-%m-%Y")

    return start_date <= check_date <= end_date

dictionary={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,
            'July':7,'August':8,'September':8,'October':10,'November':11,'December':12}

start=sys.argv[1].strip()
end=sys.argv[2].strip()

#start=sys.stdin.readline().strip()
#end=sys.stdin.readline().strip()

#start_date,start_month,start_year=map(int,start.split('-'))
#end_date,end_month,end_year=map(int,end.split('-'))

for line in sys.stdin:
    line=line.strip()
    if not line:
        continue;
    #print(line)
    try:
        key,val=line.split('&&&&&')
    except:
        continue;
    #print(key)
    #print(val)
    if(key and val):
        pattern=r'#####(\d{1,2})\s(\w+)\s(\d{4})#####'
        match=re.search(pattern,key)
        if match:
            date = match.group(1).strip()
            month = dictionary[match.group(2).strip()]
            year = match.group(3).strip()
            two=f"{date}-{month}-{year}"
            if (is_date_in_range(start,end,two)):
                print(key)
                print(val)
