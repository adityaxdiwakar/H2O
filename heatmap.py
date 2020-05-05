from PIL import Image, ImageDraw, ImageFont

import dateutil.parser
import time
import json

with open("bin/sample_data.json", "r") as f:
    data = json.load(f)

data = data[:5000]

# for tf in data:
#     ts = tf["timestamp"]
#     date = dateutil.parser.parse(ts)
#     tf["timestamp"] = int(time.mktime(date.timetuple()))

# start_time = data[0]["timestamp"]
# end_time = data[-1]["timestamp"]

# print(start_time, end_time)
# print(end_time-start_time)

minv = 1e9
maxv = 0
for timeframe in data:
    for ask in timeframe["offers"]:
        maxv = ask["price"] if ask["price"] > maxv else maxv
    for bid in timeframe["bids"]:
        minv = bid["price"] if bid["price"] < minv else minv

difference = maxv - minv
print(difference)

PADDING_TOP = 1
PADDING_BOTTOM = 1
PADDING = PADDING_TOP + PADDING_BOTTOM

HEIGHT = int(difference * 4) + PADDING
img = Image.new('RGB', (len(data), HEIGHT), color = 'black')
pixels = img.load()
for index, timeframe in enumerate(data): 
    for bid in timeframe["bids"]:
        bidp = bid["price"]
        pixels[index, HEIGHT - 4*(bidp-minv) - PADDING_BOTTOM] = (0,255,0)

    for ask in timeframe["offers"]:
        askp = ask["price"]
        pixels[index, 4*(maxv-askp) + PADDING_TOP] = (255,0,0)

img.save('bin/map.png')
