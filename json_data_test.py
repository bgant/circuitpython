
import openweathermap
json_data = openweathermap.pull_data()

# Random commands to show JSON data
print("Current Time: ", json_data['current']['dt'])  # Using openweathermap.org data for current time
print("Timezone Offset: ", json_data['timezone_offset'])
print("Feels Like: ", json_data['current']['feels_like'])
print("Description: ", json_data['current']['weather'][0]['description'])
print("Icon: ", json_data['current']['weather'][0]['icon'])

import time
print(time.localtime(json_data['current']['dt'] + json_data['timezone_offset']))
print(time.localtime(json_data['current']['dt'] + json_data['timezone_offset']).tm_hour)

for x in range(1,7):
    print(str(json_data['hourly'][x]['dt']) + "\t" + str(json_data['hourly'][x]['weather'][0]['description']))

print(str(time.localtime(json_data['current']['dt'] + json_data['timezone_offset']).tm_hour % 12) + str("PM" if time.localtime(json_data['current']['dt'] + json_data['timezone_offset']).tm_hour > 12 else "AM"))
