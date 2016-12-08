import os
import re
from datetime import datetime

req_dict = {}
req_list = []

def add_record(line,key):
    m = re.search('time="(.{20})".*uuid:(.{36}).*',line)
    logtime = datetime.strptime(m.group(1),"%y-%m-%d %H:%M:%S.%f")
    if m.group(2) in req_dict:
        req_dict[m.group(2)][key]=logtime
    else:
        req_dict[m.group(2)]={key:logtime}


# init time
with open("/home/ubuntu/log/vl_1208.log",'r') as f:
    for line in f:
        if "start read header" in line:
            add_record(line, "start")
        if "write end" in line:
            add_record(line, "end")

# time spent
for key in req_dict:
    if "end" in req_dict[key]:
        req_list.append({"uuid":key,"spent":(req_dict[key]["end"]-req_dict[key]["start"]).microseconds})

sorted_req = sorted(req_list,key=lambda x:x['spent'])

for req in sorted_req:
    print(req)

