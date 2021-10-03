#!/usr/bin/python3
import cgi
import cgitb;

cgitb.enable()
import PicClient

print('Content-type: text/html\n')

client = PicClient.PicClient()

form = cgi.FieldStorage()

action = form.getvalue('action', 'unkown')
speed = int(form.getvalue('speed', 'unkown'))

#if not client.server.isEnable():
#    try:
#        client.server.setup()
#    except Exception:
#        pass

returnVal = client.callAction(action, speed, 0)
if not returnVal:
    print("action:", form.getvalue('action', 'unkown'))
else:
    print(str(returnVal))