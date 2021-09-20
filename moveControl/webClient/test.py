import json

conf = {
    'IP': '192.168.3.173',
    'APTolerance': 5,
    # ??????
    'enableAP': False,
    # ???? ????
    'APInterval': 0.5,
    # ???? ????
    'APTurnSpeed': 50,
    # ???? ????
    'APForwardSpeed': 40,
    # ???? ??????
    'APMissTimes': 3
}

# with open('conf.json', 'w') as f:
#     json.dump(conf,f)


with open('../conf.json', 'r') as f:
    conf = json.load(f)

print(conf.keys())

for k in conf.keys():
    print("k:",k," v:",conf[k])
print(conf['IP'])




