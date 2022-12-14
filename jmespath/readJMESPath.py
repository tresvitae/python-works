import jmespath
import json

#Load JSON data from file
with open('APIresponse.json') as json_file:
  # Parse the JSON data
  json_data = json.load(json_file)

query = "reservations[].instances[?state=='running' && reservationInYears<'3'].name"

#Evaluate the JMESPath query
results = jmespath.search(query, json_data)

print(results)