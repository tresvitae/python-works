import jmespath

#Load JSON data from file
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


query = "reservations[].instances[?state=='running' && reservationInYears<3].name"

#Parse the input JSON file and evaluate the JMESPath query
json_data = json.loads(json_file)
results = jmespath.search(query, json_data)

# Print the resulting list of instance names
print(results)



import json

# Open the input file
with open('input.json') as json_file:
  # Parse the JSON data
  json_data = json.load(json_file)
  # Use the JSON data...
