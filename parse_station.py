# coding: utf-8
import re
import requests
from pprint import pprint
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9044"'
requests.packages.urllib3.disable_warnings()
r= requests.get(url, verify=False)
satext=r.text
results = re.findall(r'([[\u4e00-\u9fa5]+)\|([A-Z]+)',satext )

station1 = dict(results)
station2 = dict(zip(station1.values(), station1.keys()))
pprint(station1, indent=4)
pprint(station2, indent=4)




