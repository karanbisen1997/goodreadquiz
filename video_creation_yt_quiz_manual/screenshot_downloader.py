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
        filderno="28_12"
        
        comment={}
        # title= ["You know     ", "Someone says    ", "Here we go    ","people says   ","Do enjoy    "]
        comment['filderno']=f"youtube_quiz/{filderno}"
        comment['thread_title']="Do enjoy    "
        comment["thread_id"] = "asdf"
        comment["thread_post"] = comment['thread_title']
        comment["thread_update"] = f"youtube/{filderno}.txt"

        manual={}
        manual['que']=[]
        manual['ans']=[]
        manual['correct_ans']=[]
        manual['correct_hint']=[]

        manual['que'].append('Question. Who has launched ‘CRIIIO 4 GOOD’ to promote gender equality among girls and boys?')
        manual['ans'].append('A. UM Ashwini Vaishnaw \nB. UM Dharmendra Pradhan \nC. UM Kiren Rijiju \nD. UM Piyush Goyal')
        manual['correct_ans'].append('Correct Answer: Union Minister Dharmendra Pradhan')
        manual['correct_hint'].append('Union Minister Shri Dharmendra Pradhan launched ‘CRIIIO 4 GOOD’.\n‘CRIIIO 4 GOOD’ is a new online, life skills learning module, to promote gender equality among girls and boys.\nThe programme was launched at the Narendra Modi Stadium, Ahmedabad.\nIt was launched in association with the International Cricket Council, UNICEF, and the Board of Control for Cricket in India.\nIndian cricketer and Celebrity Supporter for ICC-UNICEF CRIIO 4 GOOD initiative, Smt. Smriti Mandhana was also present at the event.\nShe shared the first learning modules of CRIIIO 4 GOOD with over 1000 school children at the stadium.\nHence, (b) is the correct answer.')


        manual['que'].append('Question. Name the Asian Paints non-executive director, who has been passed away at the age of 79 years on 28 September.')
        manual['ans'].append('A. Ashwin Choksi\nB. Abhay Vakil \nC. Amit Syngle \nD. Ashwin Dani')
        manual['correct_ans'].append('Correct Answer: Ashwin Dani')
        manual['correct_hint'].append('On 28 September, the Asian Paints non-executive director Ashwin Dani passed away at the age of 79 years.\nSince 1968, Dani had been with the company and was a strong force in leading the company towards technical excellence.\nAsian Paints was founded in 1942 by his father and three others.\nIn 1970, he joined the board of the company and held the position of Vice Chairman and Managing Director of the company from 1998 to 2009.\nSince 2009, he had remained on the Board of Directors and Company as Non-Executive Director and Vice Chairman.\nHence, (d) is the correct answer.')

        manual['que'].append('Question. What is the theme of International Translation Day 2023?')
        manual['ans'].append('A. Translation Unveils the Many Faces of Humanity\nB. A World Without Barrier \nC. United in translation \nD. Finding the words for a world in crisis')
        manual['correct_ans'].append('Correct Answer: Translation Unveils the Many Faces of Humanity')
        manual['correct_hint'].append('International Translation Day is celebrated every year on 30 September.\nIt is celebrated to honor language professionals whose work helps bring nations closer together through dialogue, understanding, and cooperation.\nThe theme of International Translation Day 2023 is "Translation Unveils the Many Faces of Humanity."\nIt is celebrated every year on 30 September on the feast day of Saint Jerome. He is known as the patron saint of translators.\nOn 24 May 2017, the United Nations General Assembly declared 30 September as International Translation Day.\nHence, (a) is the correct answer.')

        manual['que'].append('Question. President Droupadi Murmu recently gave assent to the Women\'s Reservation Bill. It will be known as the ___.')
        manual['ans'].append('A. 105th Amendment\nB. 106th Amendment\nC. 107th Amendment\nD. 108th Amendment')
        manual['correct_ans'].append('Correct Answer: 106th Amendment')
        manual['correct_hint'].append('President Droupadi Murmu has given assent to the Women\'s Reservation Bill.\nWomen\'s Reservation Bill was introduced as the Constitution (128th) Amendment Bill in the Lok Sabha on 19 September 2023.\nIt will be known as the Constitution (106th Amendment) Act.\nThe Central government has issued a gazette notification for the legislation.\nIt is also called Nari Shakti Vandan Adhiniyam.\nIt provides 33% reservation to women in the Lok Sabha and State Assemblies as well as the Delhi Assembly.\nThe Bill was passed by the Lok Sabha with near unanimity, with only two members opposing it. It was unanimously passed by the Rajya Sabha.\nHence, (b) is the correct answer.')

        manual['que'].append('Question. Government has upgraded the Indian Renewable Energy Development Agency (IREDA) from the __________ category to Schedule A CPSE.')
        manual['ans'].append('A. Schedule B \nB. Schedule C\nC. Schedule D\nD. Schedule E')
        manual['correct_ans'].append('Correct Answer: Schedule B')
        manual['correct_hint'].append('Government has upgraded the Indian Renewable Energy Development Agency (IREDA) to ‘Schedule A’ CPSE.\nIREDA has been upgraded from the Schedule B category to Schedule A Central Public Sector Enterprise (CPSE).\nThe change makes it possible for IREDA to switch from a Mini Ratna to a Navratna company.\nIREDA’s upgradation to a Navratna company can offer it increased financial autonomy.\nCompanies holding the status of "Navratna" must be Miniratna Category-I firms with Schedule A status to qualify.\nEarlier this month, IREDA filed its draft red herring prospectus (DRHP) with SEBI to raise funds through its initial public offering (IPO).\nAs of August 21, 2023, the company has financed 3,137 renewable energy projects.\nHence, (a) is the correct answer.')
        
        comment["comments"] = []
       
       
        for i in range(0, len(manual['que'])):
            que=manual['que'][i]+"\n"
            ans=manual['ans'][i]

            answ=ans.split("\n")

            people="., check full video on my channel"
            asw=""
            for j in range(0, len(answ)):
                asw=asw+" , option "+answ[j]
            correct_ans=manual['correct_ans'][i]
            correct_hint=manual['correct_hint'][i]

            comment['comments'].append({'comment_que': ""+que+asw+" .","image_que_ans":que+"\n"+ans,'comment_ans':correct_ans+"\n\n"+people,'image_ans':correct_ans+"\n\n"+correct_hint})
            # print(count)
                
        print(comment)
        # subreddit = settings.config["reddit"]["thread"]["subreddit"]
        # end="Let me know in the comments below which line inspires you.\n\n If you enjoyed the content of this video, click the Subscribe button so you can receive more content like this every day."
        # comment['comments'].append({'comment_body': end+",","imageline":end})
        print_substep("Screenshots downloaded Successfully.", style="bold green")
        return comment
       
    #    http://lakshyapanel.com/api//quiz/topic/fetch_vbot/?limit=1&process_vbot=0&columns=front_link 
