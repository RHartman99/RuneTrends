# RuneTrends

<img src="https://github.com/RHartman99/RuneTrends/blob/master/src/images/RuneTrends_Dark.png?raw=true" align="right"
     alt="Size Limit logo by Anton Lovchikov" width="200">
RuneTrends is an [OldSchool Runescape](https://oldschool.runescape.com/) market analysis web application. It records market data and monitors trend data to offer investment predictions, allowing easier and safer item flipping.

- Pulls data from multiple sources, such as [RSBuddy's Exchange API](https://rsbuddy.com/exchange) and Jagex's official [GrandExchange API](https://secure.runescape.com/m=itemdb_oldschool/).
- Stores all tradeable item information in a database for quick access
- Identifies items with correlated trend data, and categorizes them into markets
- Displays item and market statistics in a dashboard to help identify good investments
- Tracks overall health of markets

# Installation

## Requirements

These are the requirements that are _guaranteed_ to work. Older versions may work, but results will vary.

1. `python` >= 3.8.3
2. `pip` >= 20.1.1
3. `node` >= 12.17.0

## Setup

Clone repository and enter its directory:

```console
$ git clone https://github.com/RHartman99/RuneTrends.git
$ cd ./RuneTrends/
```

Install required packages:

```console
$ npm i
$ pip install -r ./requirements-dev.txt
```

Start Django development server:

```console
$ python ./manage.py runserver
```

For more information on using Django, refer to their [documentation](https://www.djangoproject.com/start/).

For BrowserSync and other WebPack benefits, run in a **seperate terminal**:

```console
$ npm start
```

By default, BrowserSync will proxy `localhost:8000`. If this does not suite your needs, edit `webpack.mix.js` in the project's root folder:

```javascript
...
.browserSync({
  ui: false,
  injectChanges: true,
  files: files,
  proxy: "<desired proxy>",
  watch: true,
  logChanges: false,
});
...
```

## Other NPM scripts

- `watch` - Watches files and starts BrowserSync proxying
- `dev` - Runs WebPack once, copying all CSS/JS/Images to the appropriate static folders

## Populating Database

When first launching the app, there will be no item data collected. To have any meaningful data, populate the database by running several model class methods.

Start Django shell:

```shell
$ python ./manage.py shell

Python 3.x.x (...)
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

In the interactive console, run item data collection methods:

```shell
>>> from GrandExchange.models import Item
>>> Item.get_all_items()
>>> Item.set_all_data_points()
```

Both methods will take time to execute, as they make many requests to APIs that have slow response times. They can take anywhere from 10 to 30 minutes, depending on API loads.
