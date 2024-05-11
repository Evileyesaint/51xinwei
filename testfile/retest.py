import re

s = r'acw_tc=784e2c9117149378338908532e2d3b984c7c8e7079ff99dd10e5438046105c; Authorization=070d1cd2-eb37-46c6-8777-439906f6f5dd; Authorization=070d1cd2-eb37-46c6-8777-439906f6f5dd; loginToken=070d1cd2-eb37-46c6-8777-439906f6f5dd; JSESSIONID=E77BF31F2853DCFBC27317048AFBA377'



x = re.search(r'Authorization=(\S+);',s)
print(x.group(1))