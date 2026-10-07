"""Find malformed and repeated dotenv assignment names."""
import argparse,csv,io,json,math,re
from collections import Counter
from datetime import date,datetime
from pathlib import Path

import base64,ipaddress,uuid
from urllib.parse import parse_qsl,urlsplit
from http.cookies import SimpleCookie

def analyze(data):
    names=[];invalid=[]
    for i,line in enumerate(data['text'].splitlines(),1):
        line=line.strip()
        if not line or line.startswith('#'):continue
        name=line.split('=',1)[0]
        if '=' not in line or not re.fullmatch('[A-Za-z_][A-Za-z0-9_]*',name):invalid.append(i)
        else:names.append(name)
    return {'duplicate_names':sorted(k for k,n in Counter(names).items() if n>1),'invalid_lines':invalid}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,help='UTF-8 JSON input file')
    parser.add_argument('--explain',action='store_true',help='Send the local report to the configured chat gateway')
    args=parser.parse_args()
    report=analyze(json.loads(args.input.read_text(encoding='utf-8')))
    if args.explain:
        from gateway_client import explain
        print(explain(report))
    else:print(json.dumps(report,ensure_ascii=False,indent=2))
