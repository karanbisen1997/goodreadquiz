import os
import re
import time
from pathlib import Path
import string
# do not remove the above line
from utils import settings
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

    with sync_playwright() as p:
        print_substep("Launching Headless Browser...")

        # browser = p.chromium.launch(headless=True)
        browser = p.firefox.launch(headless=True)
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
       

        parse=urlparse(url)
        filderno = f"{(re.sub('[^A-Za-z0-9]+', '_', parse.path))}"
        
        page.goto(url, timeout=0)
       
        
        comment={}
        # title= ["You know     ", "Someone says    ", "Here we go    ","people says   ","Do enjoy    "]
        comment['filderno']=f"youtube_quiz/{filderno}"
        comment['thread_title']="Do enjoy    "
        comment["thread_id"] = "asdf"
        comment["thread_post"] = comment['thread_title']
        comment["thread_update"] = f"youtube/{filderno}.txt"

        comment["comments"] = []
        multi=page.query_selector_all("(//div[@class='wp_quiz_question testclass'])")
        # time.sleep(10.0)
        # print(page)
        # print(multi)
        # exit()
        for i in range(0, len(multi)):
            que=page.query_selector(f"(//div[@class='wp_quiz_question testclass'])[{(i+1)}]").inner_text().replace('\n',' ')+"\n"
            ans=page.query_selector(f"(//div[@class='wp_quiz_question_options'])[{(i+1)}]").inner_text()
            answ=ans.split("\n")
            people="., check full video on my channel"
            asw=""
            for j in range(0, len(answ)):
                asw=asw+" , option "+answ[j]
            correct_ans=page.query_selector(f"(//div[@class='ques_answer'])[{(i+1)}]").inner_text()
            correct_hint=page.query_selector(f"(//div[@class='answer_hint'])[{(i+1)}]").inner_text()
            comment['comments'].append({'comment_que': " Comment down correct answer before showing. "+que+asw+" . ","image_que_ans":que+"\n"+ans,'comment_ans':correct_ans+"\n\n"+people,'image_ans':correct_ans+"\n\n"+correct_hint.strip()})
            # print(count)
                
        print(comment)
        # subreddit = settings.config["reddit"]["thread"]["subreddit"]  Do you know The currect Answer of Question
        # end="Let me know in the comments below which line inspires you.\n\n If you enjoyed the content of this video, click the Subscribe button so you can receive more content like this every day."
        # comment['comments'].append({'comment_body': end+",","imageline":end})
        print_substep("Screenshots downloaded Successfully.", style="bold green")
        return comment
       
    #    http://lakshyapanel.com/api//quiz/topic/fetch_vbot/?limit=1&process_vbot=0&columns=front_link 
