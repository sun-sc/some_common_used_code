import json
f = open('info.json')
g =json.load(f)
print(len(g))
print(g[0])
print(g[0]['hospitalid'])
print('**********')
print(g[1])