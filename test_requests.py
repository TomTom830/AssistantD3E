'''
http://villatemoindauphin.hopto.org:8080/UniversalListen?var1=eclairage&var2=allumer&var3={{TextField}}&clesecrete=oZEpmjBk5eW1zZyY34CEbATKcWfRWSi0glnxLo39WVY
'''

import requests

r = requests.get("http://linuxfr.org/")
print(r.status_code)
