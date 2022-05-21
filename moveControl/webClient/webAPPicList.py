#!/usr/bin/python3
import cgitb;cgitb.enable()
print('Content-type: text/html\n')

#???????
with open("AP_picNames.txt", "r") as f:
    filenames = f.read().splitlines()
    filenames.reverse()

pic_num = len(filenames)
rows = int(pic_num/ 3)
if rows>20: rows=20
html = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>PICList</title>
</head>

<body>
<table width="640" border="1" cellspacing="0" cellpadding="0">
'''
for i in range(0, rows):
    html += '''
      <tr>'''
    for j in range(0,3):
        filename = filenames[i*3+j]
        html += '''
            <td><a href="../img/AP/{}"><img src="../img/AP/{}" width="320" height="240" /></a></td>
            '''.format(filename,filename)
    html += '''
      </tr>'''

html += '''
</table>
<br>
<a href='APWeb.py'>BACK</a>
</body>
</html>

'''

print(html)