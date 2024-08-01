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

        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies([{'name': 'pendulum_session', 'value': 'a%3A36%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22ddbee11fcd609310671189378213c9c2%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A14%3A%22157.34.235.219%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A80%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%3B+rv%3A108.0%29+Gecko%2F20100101+Firefox%2F108.0%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1672054408%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3Bs%3A23%3A%22intSessionEnglishQuizId%22%3Bs%3A4%3A%221249%22%3Bs%3A21%3A%22intSessionHindiQuizId%22%3Bs%3A0%3A%22%22%3Bs%3A16%3A%22quiz_session_url%22%3Bs%3A82%3A%22https%3A%2F%2Fpendulumedu.com%2Fquiz%2Fcurrent-affairs%2F23-december-2022-current-affairs-quiz%22%3Bs%3A9%3A%22txtAnswer%22%3Bs%3A0%3A%22%22%3Bs%3A11%3A%22description%22%3Bs%3A0%3A%22%22%3Bs%3A8%3A%22strTitle%22%3Bs%3A0%3A%22%22%3Bs%3A7%3A%22strExam%22%3Bs%3A0%3A%22%22%3Bs%3A10%3A%22strSubject%22%3Bs%3A0%3A%22%22%3Bs%3A8%3A%22strTopic%22%3Bs%3A0%3A%22%22%3Bs%3A12%3A%22intVersionId%22%3Bs%3A0%3A%22%22%3Bs%3A12%3A%22intEditionId%22%3Bs%3A0%3A%22%22%3Bs%3A15%3A%22txtTestSeriesId%22%3Bb%3A0%3Bs%3A13%3A%22intCategoryId%22%3Bb%3A0%3Bs%3A2%3A%22id%22%3Bs%3A5%3A%2290257%22%3Bs%3A5%3A%22email%22%3Bs%3A20%3A%22karantemp8%40gmail.com%22%3Bs%3A8%3A%22password%22%3BN%3Bs%3A4%3A%22name%22%3Bs%3A5%3A%22Karan%22%3Bs%3A10%3A%22contact_no%22%3BN%3Bs%3A11%3A%22is_verified%22%3Bs%3A1%3A%22Y%22%3Bs%3A6%3A%22status%22%3Bs%3A1%3A%22Y%22%3Bs%3A12%3A%22created_date%22%3Bs%3A19%3A%222022-12-25+11%3A48%3A14%22%3Bs%3A8%3A%22lastname%22%3Bs%3A5%3A%22Temp+%22%3Bs%3A13%3A%22lastlogindate%22%3Bs%3A19%3A%222022-12-26+16%3A51%3A40%22%3Bs%3A15%3A%22NotificationYes%22%3Bs%3A1%3A%22Y%22%3Bs%3A17%3A%22emailnotification%22%3Bs%3A1%3A%22Y%22%3Bs%3A14%3A%22registersource%22%3Bs%3A82%3A%22https%3A%2F%2Fpendulumedu.com%2Fquiz%2Fcurrent-affairs%2F24-december-2022-current-affairs-quiz%22%3Bs%3A13%3A%22issociallogin%22%3Bs%3A1%3A%22N%22%3Bs%3A3%3A%22otp%22%3BN%3Bs%3A12%3A%22otp_verified%22%3Bs%3A1%3A%22N%22%3Bs%3A8%3A%22otp_time%22%3BN%3Bs%3A11%3A%22current_url%22%3Bs%3A56%3A%22https%3A%2F%2Fpendulumedu.com%2Fthemes%2Fcss%2Fbootstrap.min.css.map%22%3B%7Db30ed2326ffc0d0641dee69345f9f2e5036411bf', 'domain': 'pendulumedu.com', 'path': '/'}])

        # if settings.config["settings"]["theme"] == "dark":
        #     cookie_file = open("./video_creation/data/cookie-dark-mode.json", encoding="utf-8")
        # else:
        #     cookie_file = open("./video_creation/data/cookie-light-mode.json", encoding="utf-8")
        # cookies = json.load(cookie_file)
        # context.add_cookies(cookies)  # load preference cookies

        # Get the thread screenshot
        page = context.new_page()
        page.set_viewport_size(ViewportSize(width=400, height=529))
        
        url="https://pendulumedu.com/quiz/current-affairs/25-and-26-december-2022-current-affairs-quiz"
        # url=input("Enter Page url  :  ")
       

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
        settings.config["reddit"]["thread"]["post_lang"]='hi'

        comment["comments"] = []
        ans=['Correct Answer: Option B','Correct Answer: Option C','Correct Answer: Option A','Correct Answer: Option c','Correct Answer: Option A','Correct Answer: Option D','Correct Answer: Option C','Correct Answer: Option C','Correct Answer: Option D','Correct Answer: Option B']
        multi=page.query_selector_all("(//div[@id='english_quiz']//div[@class='q-section-inner clear-fix'])")
        for idx,single in enumerate(multi):
            print(idx)
            que=single.query_selector("[class='more']").inner_text()
            op=single.query_selector("[class='q-option']").inner_text()
            currectop=ans[idx]
            # print(que)
            # print(op)
            op=op.replace("A","option A")
            op=op.replace("B","option B")
            op=op.replace("C","option C")
            op=op.replace("D","option D")
            if 'E' in op:
                op=op.replace("E","option E")
            if 'F' in op:
                op=op.replace("F","option F")
            op=op.replace("\n","")
          
            # print(op)
            # print(currectop)
            # comment['comments'].append({'comment_que': f"you will get the answer in last 1 second,\n  Question. {(idx+1)},  "+que+", ",'comment_op':op,'comment_ans':"Correct "+currectop})


        page.locator(f"(//a[@class='hndi-eng-img hndi-eng-img-qz'])[1]").click()
        page.eval_on_selector(selector="//a[@data-target='#myModal-examinfoo']",expression="(el) => el.style.display = 'none'")
        page.eval_on_selector(selector="//div[@class='q-pallate-sticky']/following-sibling::div[1]",expression="(el) => el.style.display = 'none'")
        page.eval_on_selector(selector="[class='scrollup']",expression="(el) => el.style.display = 'none'")
        # page.locator(f"(//a[@class='hndi-eng-img hndi-eng-img-qz'])[1]")
        # 


        multi=page.query_selector_all("(//div[@class='more_hindi'])")
        print(len(multi))
        for idx,single in enumerate(multi):
            # page.locator(f"(//div[@id='hindi_quiz']//div[@class='q-section-inner clear-fix']//a[@class='quiz-rm'][{idx+1}])").click()
            page.eval_on_selector(selector=f"(//div[@class='more_hindi'])[{idx+1}]",expression="(el) => el.style = ''")

        multi=page.query_selector_all("(//a[@class='quiz-rm'])")
        print(len(multi))
        for idx,single in enumerate(multi):
            # page.locator(f"(//div[@id='hindi_quiz']//div[@class='q-section-inner clear-fix']//a[@class='quiz-rm'][{idx+1}])").click()
            page.eval_on_selector(selector=f"(//a[@class='quiz-rm'])[{idx+1}]",expression="(el) => el.style.display = 'none'")


        multi=page.query_selector_all("(//div[@id='hindi_quiz']//div[@class='q-section-inner clear-fix'])")
        # exit()

        for idx,single in enumerate(multi):
            print(idx)
            page.set_viewport_size(ViewportSize(width=400, height=529))
            page.eval_on_selector(selector="(//header[@class='quiz-navv']//div)[1]",expression="(el) => el.style.display = 'none'")
            page.eval_on_selector(selector="[class='scrollup']",expression="(el) => el.style.display = 'none'")
            page.locator(f"(//div[@id='hindi_quiz']//div[@class='q-section-inner clear-fix'][{idx+1}])").screenshot(path=f"assets/temp/quiz_hindi/comment_{idx}.png")
            que=single.query_selector("[class='more_hindi']").inner_text()
            op=single.query_selector("[class='q-option']").inner_text()
            currectop=ans[idx]
            # print(que)
            # print(op)
            que=que.replace("\n"," ")
            op=op.replace("A","option A")
            op=op.replace("B","option B")
            op=op.replace("C","option C")
            op=op.replace("D","option D")
            if 'E' in op:
                op=op.replace("E","option E")
            if 'F' in op:
                op=op.replace("F","option F")
            op=op.replace("\n"," ")
            # print(op)
            # print(currectop)
            print(len(que))
            comment['comments'].append({'comment_que': "उत्तर अंत में दिखाया जाएगा, तेजी से सही उत्तर नीचे Comment करें, "+que,'comment_op':op,'comment_ans':currectop})

            page.set_viewport_size(ViewportSize(width=803, height=494))
            page.eval_on_selector(selector="[class='scrollup']",expression="(el) => el.style.display = 'none'")
            page.locator(f"(//div[@id='hindi_quiz']//div[@class='q-section-inner clear-fix'][{idx+1}])").screenshot(path=f"assets/temp/quiz_hindi/comment_full_{idx}.png")
            # उत्तर अंत में दिखाया जाएगा, तेजी से सही उत्तर नीचे Comment करें, Question 
        
            
        print(comment)
        # subreddit = settings.config["reddit"]["thread"]["subreddit"]
        # end="Let me know in the comments below which line inspires you.\n\n If you enjoyed the content of this video, click the Subscribe button so you can receive more content like this every day."
        # comment['comments'].append({'comment_body': end+",","imageline":end})
        print_substep("Screenshots downloaded Successfully.", style="bold green")
        return comment
       
    #    https://pendulumedu.com/quiz/current-affairs/24-december-2022-current-affairs-quiz
