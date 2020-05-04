import json
import time

with open("bin/sample_data.json", "r") as f:
    data = json.load(f)

from PIL import Image, ImageDraw, ImageFont

SCALE_FACTOR = 4

for timeframe in data:

    img = Image.new('RGB', (192*SCALE_FACTOR, 640*SCALE_FACTOR), color = 'black')
    pixels = img.load()
    for row in range(320*SCALE_FACTOR,640*SCALE_FACTOR):
        for column in range(1,64*SCALE_FACTOR):
            pixels[column, row] = (0,255,0)

    for row in range(1,320*SCALE_FACTOR):
        for column in range(128*SCALE_FACTOR, 192*SCALE_FACTOR):
            pixels[column, row] = (255,0,0)

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

    fnt = ImageFont.truetype('bin/arial.ttf', 15*SCALE_FACTOR)
    d = ImageDraw.Draw(img)
    for index, price in enumerate(prices):
        position = (68*SCALE_FACTOR, (index*32*SCALE_FACTOR) + 6*SCALE_FACTOR)
        d.text(position, str(price), font=fnt, fill=(255,255,255))


    bids = []
    for bid in timeframe["bids"]:
        bids.append(bid["size"])
    bids.reverse()

    asks = []
    for ask in timeframe["offers"]:
        asks.append(ask["size"])
    asks.reverse()

    for index, bid in enumerate(bids):
        position = (20*SCALE_FACTOR, (640*SCALE_FACTOR) - ((index+1)*32*SCALE_FACTOR) + 6*SCALE_FACTOR)
        d.text(position, str(bid), font=fnt, fill=(0,0,0))

    for index, ask in enumerate(asks):
        position = (148*SCALE_FACTOR, ((index)*32*SCALE_FACTOR) + 6*SCALE_FACTOR)
        d.text(position, str(ask), font=fnt, fill=(0,0,0))


    img.save('bin/output.png')

    time.sleep(0.25)