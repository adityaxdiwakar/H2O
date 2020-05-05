import json
import time

with open("bin/sample_data.json", "r") as f:
    data = json.load(f)

from PIL import Image, ImageDraw, ImageFont

SCALE_FACTOR = 4

for timeframe in data:
    print(timeframe["timestamp"])
    img = Image.new('RGB', (192*SCALE_FACTOR, 640*SCALE_FACTOR), color = 'black')
    pixels = img.load()

    bids = []
    for bid in timeframe["bids"]:
        bids.append(bid["size"])
    bids.reverse()
    bidmax, bidmin = max(bids), min(bids)
    bidnorm = [((2/3) * (bid - bidmin)/(bidmax-bidmin)) + (1/3) for bid in bids]
    bidnorm.reverse()

    asks = []
    for ask in timeframe["offers"]:
        asks.append(ask["size"])
    asks.reverse()
    askmax, askmin = max(asks), min(asks)
    asknorm = [((2/3) * (ask - askmin)/(askmax-askmin)) + (1/3) for ask in asks]

    for index, bid_perc in enumerate(bidnorm):
        for row in range(320*SCALE_FACTOR + (index)*32*SCALE_FACTOR,320*SCALE_FACTOR + (index+1)*32*SCALE_FACTOR):
            for column in range(1,int(64*SCALE_FACTOR*bid_perc)):
                pixels[64*SCALE_FACTOR - column, row] = (0,255,0)

    for index, ask_perc in enumerate(asknorm):
        for row in range(index*32*SCALE_FACTOR,(index+1)*32*SCALE_FACTOR):
            for column in range(128*SCALE_FACTOR, 128*SCALE_FACTOR + int(64*ask_perc*SCALE_FACTOR)):
                pixels[column, row] = (255,0,0)

    # for row in range(1,320*SCALE_FACTOR):
    #     for column in range(128*SCALE_FACTOR, 192*SCALE_FACTOR):
    #         pixels[column, row] = (255,0,0)

    for row in range(640*SCALE_FACTOR):
        if row % (32*SCALE_FACTOR) == 0:
            for column in range(1, 192*SCALE_FACTOR):
                pixels[column, row] = (0,0,0)

    for row in range(640*SCALE_FACTOR):
        pixels[64*SCALE_FACTOR, row] = (255, 255, 255)
        pixels[128*SCALE_FACTOR, row] = (255, 255, 255)

    for row in range(640*SCALE_FACTOR):
        if row % (32*SCALE_FACTOR) == 0:
            for column in range(64*SCALE_FACTOR, 128*SCALE_FACTOR):
                pixels[column, row] = (255, 255, 255)

    # d.text((10,10), "Hello World", fill=(255,255,0))

    prices = []

    for bid in timeframe["bids"]:
        prices.append(bid["price"])

    for offer in timeframe["offers"]:
        prices.append(offer["price"])

    prices.sort()
    prices.reverse() 

    fnt = ImageFont.truetype('bin/arial.ttf', 13*SCALE_FACTOR)
    d = ImageDraw.Draw(img)
    for index, price in enumerate(prices):
        w, h = d.textsize(str(price))
        position = ((192*SCALE_FACTOR)/2 - 2 * w, (index*32*SCALE_FACTOR) + 8*SCALE_FACTOR)
        d.text(position, str(price), font=fnt, fill=(255,255,255))

    for index, bid in enumerate(bids):
        position = (46*SCALE_FACTOR, (640*SCALE_FACTOR) - ((index+1)*32*SCALE_FACTOR) + 6*SCALE_FACTOR)
        d.text(position, str(bid).zfill(2), font=fnt, fill=(0,0,0))

    for index, ask in enumerate(asks):
        position = (130*SCALE_FACTOR, ((index)*32*SCALE_FACTOR) + 6*SCALE_FACTOR)
        d.text(position, str(ask).zfill(2), font=fnt, fill=(0,0,0))


    img.save('bin/output.png')