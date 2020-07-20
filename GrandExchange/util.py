from constants import ALPHABET, URLS
import progressbar
import time
import logging
from tqdm import tqdm


def get_all_items(cls):
    api_url = URLS["GE"]
    data = {}
    endpoint = "%(url)s%(endpoint)s.json" % {"url": api_url, "endpoint": "items"}
    with tqdm(total=len(ALPHABET), ncols=80, desc="Getting all items:") as pbar:
        for letter in ALPHABET:
            page = 1
            while ("items" in data and data["items"]) or page == 1:
                response = requests.get(
                    endpoint, params={"category": 1, "alpha": letter, "page": page}
                )
                if response.ok:
                    try:
                        data = response.json()
                    except json.decoder.JSONDecodeError:
                        pbar.write(
                            "Request for page %i of letter %s resulted in invalid JSON. Retrying..."
                            % (page, letter)
                        )
                        continue

                    pbar.write(
                        "Request for page %i of letter %s succesful." % (page, letter)
                    )

                    for item in data["items"]:
                        if not cls.objects.filter(item_id=item["id"]).exists():
                            cls.objects.create(
                                name=item["name"],
                                item_id=item["id"],
                                type=item["type"],
                                icon=item["icon"],
                                icon_large=item["icon_large"],
                                description=item["description"],
                                members=(item["members"] == "true"),
                                price=item["current"]["price"],
                            )
                        if not cls.objects.filter(item_id=item["id"]).exists():
                            cls.objects.create(
                                name=item["name"],
                                item_id=item["id"],
                                type=item["type"],
                                icon=item["icon"],
                                icon_large=item["icon_large"],
                                description=item["description"],
                                members=(item["members"] == "true"),
                                price=item["current"]["price"],
                            )
                        else:
                            cls.objects.filter(item_id=item["id"]).update(
                                name=item["name"],
                                item_id=item["id"],
                                type=item["type"],
                                icon=item["icon"],
                                icon_large=item["icon_large"],
                                description=item["description"],
                                members=(item["members"] == "true"),
                                price=item["current"]["price"],
                            )

                else:
                    pbar.write(
                        "ERROR: Request for page %i of letter %s failed."
                        % (page, letter)
                    )

                page += 1
            pbar.update()

    cls.update_all_items_info()
