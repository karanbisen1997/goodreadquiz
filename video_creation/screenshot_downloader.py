import json
import os
import random
import re
import sys
import time
from urllib.parse import urlparse
import requests

from pathlib import Path
from typing import Dict
from utils import settings
from playwright.async_api import async_playwright  # pylint: disable=unused-import

# do not remove the above line

from playwright.sync_api import sync_playwright, ViewportSize
from rich.progress import track
import translators as ts

from utils.console import print_step, print_substep
from video_creation.final_video import name_normalize

storymode = False


def download_screenshots_of_reddit_posts():
    """Downloads screenshots of reddit posts as seen on the web. Downloads to assets/temp/png

    Args:
        reddit_object (Dict): Reddit object received from reddit/subreddit.py
        screenshot_num (int): Number of screenshots to download
    """
    print_step("Downloading screenshots of reddit posts...")

    # ! Make sure the reddit screenshots folder exists
    Path("assets/temp/png").mkdir(parents=True, exist_ok=True)
    Path("shorts").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print_substep("Launching Headless Browser...")

        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # if settings.config["settings"]["theme"] == "dark":
        #     cookie_file = open("./video_creation/data/cookie-dark-mode.json", encoding="utf-8")
        # else:
        #     cookie_file = open("./video_creation/data/cookie-light-mode.json", encoding="utf-8")
        # cookies = json.load(cookie_file)
        # context.add_cookies(cookies)  # load preference cookies

        # Get the thread screenshot
        page = context.new_page()
        # url=input("Enter lakshya Education Quiz Page url  :  ")
        url=input("Enter Page url  :  ")
        if len(url)>10:
            url=url
        else:
            url="https://www.goodreads.com/quotes"

        parse=urlparse(url)
        filderno = f"{name_normalize(re.sub('[^A-Za-z0-9]+', '_', parse.path))}"
        print(parse)
        # exit()
        if os.path.exists(f"shorts/{filderno}.txt"):
            f= open(f"shorts/{filderno}.txt", 'r')
            last_line = f.readlines()[-1]
            f.close()
            # print('last_line',last_line)
            # exit()
            f= open(f"shorts/{filderno}.txt", 'a')
            f.write(f'{int(last_line)+1} \n')
            f.close()
            # print('ere')
        else:
            f= open(f"shorts/{filderno}.txt", 'a')
            f.write('1 \n')
            f.close()
        # print(last_line)
        # exit()
        url=url+"?page="+last_line
        print(url)
        # url="https://lakshyaeducation.in/topic/tally/16305448225876caacbdd21/"
        # exit()
        page.set_viewport_size(ViewportSize(width=400, height=529))
        page.goto(url, timeout=0)
        page.set_viewport_size(ViewportSize(width=400, height=529))
        page.goto(url, timeout=0)
       
        
        comment={}
        # title= ["You know     ", "Someone says    ", "Here we go    ","people says   ","Do enjoy    "]
        comment['filderno']=f"shorts/{filderno}/{int(last_line)}"
        comment['thread_title']="Do enjoy    "
        comment["thread_id"] = comment['thread_title']+" "+last_line
        comment["thread_post"] = comment['thread_title']+" "+last_line
        comment["comments"] = []
        multi=page.query_selector_all("(//div[@class='quote'])")
        # print(multi)
        count=0
        image=0
        for idx,single in enumerate(multi):
            if image==9:
                image=0
            que=single.query_selector("[class='quoteText']").inner_text()
            quecount=len(re.findall(r'\w+', que))
            if quecount<100:
                if quecount<50:
                    page1 = context.new_page()
                    url=f"https://tools.ineotron.com/vdotron/render.php?pid=1099&slide={67+image}&final=1&text1="+que
                    page1.goto(url, timeout=0)
                    # page1.set_viewport_size(ViewportSize(width=881, height=350))
                    page1.locator("img").screenshot(path=f"assets/temp/png/comment_{count}.png")
                    # page.locator(f"(//div[@class='quoteText'])[{idx+1}]").screenshot(path=f"assets/temp/png/comment_{count}.png")
                    comment['comments'].append({'comment_body': que})
                    print(count)
                    time.sleep(2.4)
                    count=len(comment['comments'])
                    image+=1
                else:
                    page1 = context.new_page()
                    url="https://tools.ineotron.com/vdotron/render.php?pid=1099&slide=66&final=1&text1="+que
                    page1.goto(url, timeout=0)
                    # page1.set_viewport_size(ViewportSize(width=881, height=350))
                    page1.locator("img").screenshot(path=f"assets/temp/png/comment_{count}.png")
                    # page.locator(f"(//div[@class='quoteText'])[{idx+1}]").screenshot(path=f"assets/temp/png/comment_{count}.png")
                    comment['comments'].append({'comment_body': que})
                    print(count)
                    time.sleep(2.4)
                    count=len(comment['comments'])
        # exit(que)
        

        print_substep("Screenshots downloaded Successfully.", style="bold green")
        return comment
       
    #    http://lakshyapanel.com/api//quiz/topic/fetch_vbot/?limit=1&process_vbot=0&columns=front_link 
