#!/usr/bin/python3
import cgi
import cgitb;cgitb.enable()
import ctrlClient

print('Content-type: text/html\n')

client = ctrlClient.CtrlClient()

form=cgi.FieldStorage()

action = form.getvalue('action','unkown')
if not client.server.isEnable():
    try:
        client.server.setup()
    except Exception:
        pass

client.callAction(action,30,0)

print("action:",form.getvalue('action','unkown'))