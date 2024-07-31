#!/usr/bin/env python
import math
from subprocess import Popen
from os import name
import requests
import time
from reddit.subreddit import get_subreddit_threads
from utils.cleanup import cleanup
from utils.console import print_markdown, print_step
from utils import settings
import json
import psutil
import sys
import os
import re

from video_creation_yt_quiz.background import (
    download_background,
    chop_background_video,
    get_background_config,
)
from video_creation_yt_quiz.final_video import make_final_video, name_normalize
from video_creation_yt_quiz.screenshot_downloader import download_screenshots_of_reddit_posts
from video_creation_yt_quiz.voices import save_text_to_mp3

__VERSION__ = "2.3"
__BRANCH__ = "master"

def main(POST_ID=None):
    cleanup()
    reddit_object={}
    reddit_object=download_screenshots_of_reddit_posts()
    # print(reddit_object)
    # exit()
    length, number_of_comments = save_text_to_mp3(reddit_object)
    length = math.ceil(length)
    bg_config = get_background_config()
    # download_background(bg_config)
    # chop_background_video(bg_config, length)
    make_final_video(number_of_comments+1, length, reddit_object, bg_config,reddit_object['filderno'])

def run_many(times):
    for x in range(1, times + 1):
        print_step(
            f'on the {x}{("th", "st", "nd", "rd", "th", "th", "th", "th","th", "th")[x%10]} iteration of {times}'
        )  # correct 1st 2nd 3rd 4th 5th....
        main()
        Popen("cls" if name == "nt" else "clear", shell=True).wait()


# j = 1
# while j < 3:
print("----------------------------------------------------------------------------: ") 
print(
    """
██████╗ ███████╗██████╗ ██████╗ ██╗████████╗    ██╗   ██╗██╗██████╗ ███████╗ ██████╗     ███╗   ███╗ █████╗ ██╗  ██╗███████╗██████╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝    ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗    ████╗ ████║██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║       ██║   ██║██║██║  ██║█████╗  ██║   ██║    ██╔████╔██║███████║█████╔╝ █████╗  ██████╔╝
██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║       ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║    ██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗
██║  ██║███████╗██████╔╝██████╔╝██║   ██║        ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██║  ██╗███████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚═╝   ╚═╝         ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""
)

print_step(f"You are using v{__VERSION__} of the bot")

if __name__ == "__main__":
    config = settings.check_toml(".config.template.toml", "config.toml")
    # print(config)
    # exit()
    config is False and exit()
    try:
        if config["settings"]["times_to_run"]:
            # print("hello1")
            # exit()
            run_many(config["settings"]["times_to_run"])

        elif len(config["reddit"]["thread"]["post_id"].split("+")) > 1:
            # print("hello2")
            # exit()
            for index, post_id in enumerate(config["reddit"]["thread"]["post_id"].split("+")):
                index += 1
                print_step(
                    f'on the {index}{("st" if index%10 == 1 else ("nd" if index%10 == 2 else ("rd" if index%10 == 3 else "th")))} post of {len(config["reddit"]["thread"]["post_id"].split("+"))}'
                )
                main(post_id)
                Popen("cls" if name == "nt" else "clear", shell=True).wait()
        else:
            # print("hello3")
            # exit()
            main()
    except KeyboardInterrupt:
        print_markdown("## Clearing temp files")
        cleanup()
        exit()
  