from django.db import models
from django.utils import timezone
from .constants import ALPHABET, URLS
import requests
import json
import math
import time
import sys
import datetime
import os
from progress.bar import ChargingBar


def null_sentinel(obj, sentinel):
    if obj is None:
        return sentinel
    else:
        return obj

class ProgressBar(ChargingBar):
    suffix = '%(percent).1f%% - %(remaining_minutes).1fm'
    @property
    def remaining_minutes(self):
        return self.eta / 60

# Create your models here.
class Item(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    id = models.IntegerField(primary_key=True)
    item_id = models.IntegerField()
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    icon = models.URLField(max_length=200)
    icon_large = models.URLField(max_length=200)
    description = models.CharField(max_length=400)
    members = models.BooleanField()

    # Item info from OSBOX
    low_alch = models.IntegerField()
    high_alch = models.IntegerField()
    weight = models.IntegerField()
    buy_limit = models.IntegerField()
    quest_item = models.BooleanField()
    release_date = models.CharField(max_length=11)
    wiki_name = models.CharField(max_length=200)
    wiki_url = models.URLField(max_length=400)
    wiki_exchange = models.URLField(max_length=400)

    def __str__(self):
        return self.name

    # TODO: Seperate this into a module.
    @classmethod
    def get_all_items(cls):
        api_url = URLS["GE"]
        data = {}
        endpoint = "%(url)s%(endpoint)s.json" % {"url": api_url, "endpoint": "items"}
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
                    print(
                        "ERROR: Request for page %i of letter %s failed."
                        % (page, letter),
                        file=sys.stderr,
                    )

                page += 1

        cls.update_all_items_info()

    @classmethod
    def update_all_items_info(cls):
        start_time = time.time()
        for item in cls.objects.all():
            item.update_item_info()
        print("\nFinished updating all items.")
        print(
            "|  Execution time (real time): %s"
            % str(datetime.timedelta(seconds=(time.time() - start_time)))
        )

    @classmethod
    def set_all_data_points(cls):
        start_time = time.time()
        
        with ProgressBar('Getting data points', max=cls.objects.all().count()) as bar:
            for item in cls.objects.all():
                item.set_data_point()
                os.system('cls||clear')
                bar.next()
        print("\nFinished updating all items.")
        print(
            "|  Execution time (real time): %s"
            % str(datetime.timedelta(seconds=(time.time() - start_time)))
        )

    def update_item_info(self):
        api_url = URLS["OSBOX"]
        endpoint = f"{api_url}items"
        # fmt: off
        payload = "{\n\t\"name\":\"" + self.name + "\"\n}"
        response = requests.get(endpoint, params={"where": payload},)
        if response.ok:
            print("Request for information on item '%s' succesful" % self.name)
            data = response.json()
            item = data["_items"][0]
            self.low_alch = null_sentinel(item["lowalch"], -1)
            self.high_alch = null_sentinel(item["highalch"], -1)
            self.weight = null_sentinel(item["weight"], -1)
            self.buy_limit = null_sentinel(item["buy_limit"], -1)
            self.quest_item = null_sentinel(item["quest_item"], "")
            self.release_date = null_sentinel(item["release_date"], "")
            self.wiki_name = null_sentinel(item["wiki_name"], "")
            self.wiki_url = null_sentinel(item["wiki_url"], "")
            self.wiki_exchange = null_sentinel(item["wiki_exchange"], "")
            self.save()

        else:
            print(
                "ERROR: Request for information on item '%s' failed. \n| Code: %d\n|  URL: %s"
                % (self.name, response.status_code, response.url),
                file=sys.stderr,
            )
    
    def set_data_point(self):
        endpoint = '%sitem/%d.json' % (URLS["OSBGOOGLE"], self.item_id)
        response = requests.get(endpoint)
        if response.ok:
            try:
                data = response.json()
                d = DataPoint(
                    item = self,
                    buy_average = data["buy_average"],
                    buy_quantity = data["buy_quantity"],
                    overall_average = data["overall_average"],
                    overall_quantity = data["overall_quantity"],
                    sell_average = data["sell_average"],
                    sell_quantity = data["sell_quantity"],
                    store_price = data["sp"],
                )

            except json.decoder.JSONDecodeError:
                print("ERROR: DataPoint Request for %s (%d) resulted in invalid JSON." % (self.name, self.id), file=sys.stderr,)
    
        else:
            print("ERROR: Could not fetch page for %s. URL: %s" % (self.name, response.url), file=sys.stderr)
    
    def getSlug(self):
        return self.name.replace(' ', '_').lower()

class DataPoint(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buy_average = models.IntegerField()
    buy_quantity = models.IntegerField()
    overall_average = models.IntegerField()
    overall_quantity = models.IntegerField()
    sell_average = models.IntegerField()
    sell_quantity = models.IntegerField()
    store_price = models.IntegerField()

    def __str__(self):
        return "<DataPoint:\"" + self.item.name + "\">"
    

