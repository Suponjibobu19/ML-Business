from mistralcognitionagent import agentclassification
import json

jsonfile = 'codes\\fakemails.json'

with open(jsonfile, 'r') as file:
    data = json.load(file)
    for mail in data['emails']:
        agentclassification(str(mail))