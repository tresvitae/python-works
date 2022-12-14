import jmespath
import json

#Load JSON data from file
with open('APIresponse.json') as json_file:
  # Parse the JSON data
  json_data = json.load(json_file)

'''
json_file = """
{
  "reservations": [
    {
      "instances": [
        {"name": "instance1", "state": "running", "reservationInYears": "2"},
        {"name": "instance2", "state": "stopped", "reservationInYears": "1"}
      ]
    },
    {
      "instances": [
        {"name": "instance3", "state": "terminated", "reservationInYears": "3"},
        {"name": "instance4", "state": "running", "reservationInYears": "4"}
      ]
    }
  ]
}
"""
'''
query = "reservations[].instances[?state=='running' && reservationInYears<'3'].name"

#Evaluate the JMESPath query
#json_data = json.loads(json_file)
results = jmespath.search(query, json_data)

print(results)