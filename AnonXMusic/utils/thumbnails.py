import os
import re

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from AnonXMusic import app
from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def clear(text):
    list = text.split(" ")
    title = ""
    for i in list:
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()


async def get_thumb(videoid, user_id):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        try:
            wxyz = await app.get_chat_photos(user_id)
            wxy = await app.download_media(wxyz[0]['file_id'], file_name=f'{user_id}.jpg')
        except:
            hehe = await app.get_chat_photos(app.id)
            wxy = await app.download_media(hehe[0]['file_id'], file_name=f'{app.id}.jpg')
        xy = Image.open(wxy)
        a = Image.new('L', [640, 640], 0)
        b = ImageDraw.Draw(a)
        b.pieslice([(0, 0), (640,640)], 0, 360, fill = 255, outline = "white")                
        c = np.array(xy)
        d = np.array(a)
        e = np.dstack((c, d))
        f = Image.fromarray(e)
        x = f.resize((197, 197))
        
        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        bg = Image.open("AnonXMusic/assets/kaithumb.png")
        image2 = bg.convert("RGBA")
        #background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(image2)
        background = enhancer.enhance(1)
        image2 = background
        
        circle = Image.open("AnonXMusic/assets/circle.png")

        # changing circle color
        im = circle
        im = im.convert('RGBA')
        color = make_col()

        data = np.array(im)
        red, green, blue, alpha = data.T

        white_areas = (red == 255) & (blue == 255) & (green == 255)
        data[..., :-1][white_areas.T] = color

        im2 = Image.fromarray(data)
        circle = im2
        # done

        image3 = image1.crop((280,0,1000,720))
        lum_img = Image.new('L', [720,720] , 0)
        draw = ImageDraw.Draw(lum_img)
        draw.pieslice([(0,0), (720,720)], 0, 360, fill = 255, outline = "white")
        img_arr = np.array(image3)
        lum_img_arr = np.array(lum_img)
        final_img_arr = np.dstack((img_arr,lum_img_arr))
        image3 = Image.fromarray(final_img_arr)
        image3 = image3.resize((380,380))
            

        image2.paste(image3, (229,141), mask = image3)
        image2.paste(x, (980, 586), mask=x)
        #image2.paste(circle, (0,0), mask = circle)
        
        arial = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 30)
        font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 30)
        draw.text((1110, 8), unidecode(app.name), fill="white", font=arial)
        draw.text(
            (55, 560),
            f"{channel} | {views[:23]}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (57, 600),
            clear(title),
            (255, 255, 255),
            font=font,
        )
        draw.line(
            [(55, 660), (1220, 660)],
            fill="white",
            width=5,
            joint="curve",
        )
        draw.ellipse(
            [(918, 648), (942, 672)],
            outline="white",
            fill="white",
            width=15,
        )
        draw.text(
            (36, 685),
            "00:00",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (1185, 685),
            f"{duration[:23]}",
            (255, 255, 255),
            font=arial,
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        image2 = image2.convert('RGB')
        image2.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
