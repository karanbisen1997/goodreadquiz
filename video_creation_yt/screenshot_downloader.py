import os
import re
import time
from pathlib import Path

# do not remove the above line

from playwright.sync_api import sync_playwright, ViewportSize

from utils.console import print_step, print_substep
from urllib.parse import urlparse
storymode = False

def name_normalize(name: str) -> str:
    name = re.sub(r'[?\\"%*:|<>]', "", name)
    name = re.sub(r"( [w,W]\s?\/\s?[o,O,0])", r" without", name)
    name = re.sub(r"( [w,W]\s?\/)", r" with", name)
    name = re.sub(r"(\d+)\s?\/\s?(\d+)", r"\1 of \2", name)
    name = re.sub(r"(\w+)\s?\/\s?(\w+)", r"\1 or \2", name)
    name = re.sub(r"\/", r"", name)

def download_screenshots_of_reddit_posts():
    """Downloads screenshots of reddit posts as seen on the web. Downloads to assets/temp/png

    Args:
        reddit_object (Dict): Reddit object received from reddit/subreddit.py
        screenshot_num (int): Number of screenshots to download
    """
    print_step("Downloading screenshots of reddit posts...")

    # ! Make sure the reddit screenshots folder exists
    Path("assets/temp/png").mkdir(parents=True, exist_ok=True)
    Path("youtube").mkdir(parents=True, exist_ok=True)

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
        
        url=input("Enter Page url  :  ")
        if len(url)>10:
            url=url
        else:
            url="https://www.goodreads.com/quotes"

        parse=urlparse(url)
        filderno = f"{(re.sub('[^A-Za-z0-9]+', '_', parse.path))}"
        # print(filderno)
        # exit()
        if os.path.exists(f"youtube/{filderno}.txt"):
            f= open(f"youtube/{filderno}.txt", 'r')
            last_line = f.readlines()[-1]
            f.close()
            # print('last_line',last_line)
            # exit()
            f= open(f"youtube/{filderno}.txt", 'a')
            f.write(f'{int(last_line)+1} \n')
            f.close()
            # print('ere')
        else:
            f= open(f"youtube/{filderno}.txt", 'a')
            f.write('1 \n')
            last_line="1"
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
        comment['filderno']=f"youtube/{filderno}/{int(last_line)}"
        comment['thread_title']="Do enjoy    "
        comment["thread_id"] = comment['thread_title']+" "+last_line
        comment["thread_post"] = comment['thread_title']+" "+last_line
        comment["comments"] = []
        multi=page.query_selector_all("(//div[@class='quote'])")
        # print(multi)
        count=0
        image=0
        for idx,single in enumerate(multi):
            if image==10:
                image=0
            que=single.query_selector("[class='quoteText']").inner_text()
            que1=que.split("―")
            if len(que1)==1:
                text1=que1[0]
                text2=" "
            else:
                text1=que1[0]
                text2=que1[1]


            quecount=len(re.findall(r'\w+', que))
            if quecount<100:
                page1 = context.new_page()
                url=f"https://tools.ineotron.com/vdotron/render.php?pid=1099&slide={77+image}&final=1&text1="+text1+"&text2="+text2
                page1.goto(url, timeout=0)
                # page1.set_viewport_size(ViewportSize(width=881, height=350))
                page1.locator("img").screenshot(path=f"assets/temp/png/comment_{count}.png")
                # page.locator(f"(//div[@class='quoteText'])[{idx+1}]").screenshot(path=f"assets/temp/png/comment_{count}.png")
                comment['comments'].append({'comment_body': que})
                print(count)
                time.sleep(2.4)
                count=len(comment['comments'])
                image+=1
                
        # exit(que)
        

        print_substep("Screenshots downloaded Successfully.", style="bold green")
        return comment
       
    #    http://lakshyapanel.com/api//quiz/topic/fetch_vbot/?limit=1&process_vbot=0&columns=front_link 
