import requests
import json

URL = "http://services.runescape.com/m=itemdb_oldschool/api/catalogue/"

endpoint = "%(url)s%(endpoint)s.json" % {"url": URL, "endpoint": "items"}
response = requests.get(endpoint, params={"category": 1, "alpha": "a", "page": 1})
data = response.json()
print(json.dumps(data, indent=2, sort_keys=True))

with open("response.json", "w") as file:
    file.write(json.dumps(data, indent=2, sort_keys=True))

if response.ok:
    print("Request Success!")
    print("Information: ")
    print("   Status Code: %d" % response.status_code)
    print("   Request URL: %s" % response.url)
    print("   Time Elapsed: %d%s" % (response.elapsed.microseconds / 1000, "ms"))
else:
    print("Request Failure.")
