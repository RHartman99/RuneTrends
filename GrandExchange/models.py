from django.db import models
from .constants import ALPHABET
import requests
import json
import math
import time

# Create your models here.
class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    item_id = models.IntegerField()
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    icon = models.URLField(max_length=200)
    icon_large = models.URLField(max_length=200)
    description = models.CharField(max_length=400)
    members = models.BooleanField()

    def __str__(self):
        return self.name

    # TODO: Seperate this into a module.
    @classmethod
    def get_all_items(cls):
        URL = "http://services.runescape.com/m=itemdb_oldschool/api/catalogue/"
        data = {}
        endpoint = "%(url)s%(endpoint)s.json" % {"url": URL, "endpoint": "items"}
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
                        print(
                            "Request for page %i of letter %s resulted in invalid JSON. Retrying..."
                            % (page, letter)
                        )
                        continue

                    print(
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
                    print("Request for page %i of letter %s failed." % (page, letter))

                page += 1
