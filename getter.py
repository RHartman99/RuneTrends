import requests
import json
import math
import constants
import time

URL = "http://services.runescape.com/m=itemdb_oldschool/api/catalogue/"
# id:item object
inventory = {"total": 0, "time_elapsed": time.time(), "items": {}}

data = {}
endpoint = "%(url)s%(endpoint)s.json" % {"url": URL, "endpoint": "items"}
start_time = time.time()

for letter in constants.ALPHABET:
    page = 1

    while ("items" in data and data["items"]) or page == 1:
        # Get items JSON for current letter
        response = requests.get(
            endpoint, params={"category": 1, "alpha": letter, "page": page}
        )

        if response.ok:
            try:
                data = response.json()
            except json.decoder.JSONDecodeError:
                print(
                    "Request for page %i of letter %s resulted in invalid JSON. Retrying..."
                    % (page, letter)
                )
                continue

            print("Request for page %i of letter %s succesful." % (page, letter))

            for item in data["items"]:
                inventory["total"] += 1
                inventory["items"][item["id"]] = item

        else:
            print("Request for page %i of letter %s failed." % (page, letter))

        page += 1

inventory["time_elapsed"] = time.time() - start_time

with open("items.json", "w") as f:
    f.write(json.dumps(inventory, indent=2, sort_keys=False))
