#!/usr/bin/env python3
import time
import multiprocessing
from pathlib import Path
import re,random
from typing import Tuple, Any
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import vfx, TextClip, ColorClip, CompositeVideoClip,concatenate_audioclips,afx,CompositeAudioClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from rich.console import Console

from utils.console import print_step, print_substep
from utils import settings

console = Console()
# W, H = 1280, 720
W, H = 1080, 1920 


def name_normalize(name: str) -> str:
    name = re.sub(r'[?\\"%*:|<>]', "", name)
    name = re.sub(r"( [w,W]\s?\/\s?[o,O,0])", r" without", name)
    name = re.sub(r"( [w,W]\s?\/)", r" with", name)
    name = re.sub(r"(\d+)\s?\/\s?(\d+)", r"\1 of \2", name)
    name = re.sub(r"(\w+)\s?\/\s?(\w+)", r"\1 or \2", name)
    name = re.sub(r"\/", r"", name)

    lang = settings.config["reddit"]["thread"]["post_lang"]
    if lang:
        import translators as ts

        print_substep("Translating filename...")
        translated_name = ts.google(name, to_language=lang)
        return translated_name

    else:
        return name


def make_final_video(
    number_of_clips: int,
    length: int,
    reddit_obj1: dict,
    background_config: Tuple[str, str, str, Any],
    folderNo: str,
):
    """Gathers audio clips, gathers all screenshots, stitches them together and saves the final video to assets/temp
    Args:
        number_of_clips (int): Index to end at when going through the screenshots'
        length (int): Length of the video
        reddit_obj (dict): The reddit object that contains the posts to read.
        background_config (Tuple[str, str, str, Any]): The background config to use.
    """
    # try:  # if it isn't found (i.e you just updated and copied over config.toml) it will throw an error
    #    VOLUME_MULTIPLIER = settings.config["settings"]['background']["background_audio_volume"]
    # except (TypeError, KeyError):
    #    print('No background audio volume found in config.toml. Using default value of 1.')
    #    VOLUME_MULTIPLIER = 1
    print_step("Creating the final video 🎥")
    print(number_of_clips)
    VideoFileClip.reW = lambda clip: clip.resize(width=W)
    VideoFileClip.reH = lambda clip: clip.resize(width=H)
    opacity = settings.config["settings"]["opacity"]
    title = re.sub(r"[^\w\s-]", "", reddit_obj1["thread_post"])
    new_opacity = 1 if opacity is None or float(opacity) >= 1 else float(opacity)
    filename = f"{name_normalize(re.sub('[^A-Za-z0-9]+', '_', title))}.mp4"
    subreddit = settings.config["reddit"]["thread"]["subreddit"]
    Path(f"results/{subreddit}/{folderNo}").mkdir(parents=True, exist_ok=True)
    print(reddit_obj1)
    print(number_of_clips)
    # exit()
    back=random.randint(1, 7)
    all_clip=[]
    for i in range(0, number_of_clips):
        W, H = 1080, 1920

        # from moviepy.editor import *
        # Import the audio(Insert to location of your audio instead of audioClip.mp3)
        audio_ans = AudioFileClip(f"assets/temp/mp3/comment_ans{i}.mp3")
        audio_que = AudioFileClip(f"assets/temp/mp3/comment_que{i}.mp3")
        audio_op = AudioFileClip(f"assets/temp/mp3/comment_op{i}.mp3")
        audio_silence = AudioFileClip(f"assets/backgrounds/silence.mp3")
        audio_silence = AudioFileClip(f"assets/temp/audio/start2.mp3")

        audio=concatenate_audioclips([audio_que,audio_op])

        credits = (ImageClip(f"assets/temp/quiz_hindi/comment_{i}.png").set_duration(audio.duration).resize(width=W-100).set_opacity(new_opacity))
        credits = credits.set_position('center')
        colorclip = ColorClip(size=(W, H), color=(255,255,255)).set_duration(audio.duration)
        final_clip = CompositeVideoClip([colorclip, credits])
        final_clip = final_clip.set_position('center')
        final_clip.save_frame(f"out_que{i}.png")
        final_clip = final_clip.set_audio(audio).fx( vfx.speedx, 0.9)
        

        # final_clip = final_clip.set_audio(audio_que).fx(vfx.fadein,1).fx(vfx.fadeout,1).fx( vfx.speedx, 0.9)
        print(reddit_obj1['comments'][i]['comment_ans'])
        
        credits1 = (TextClip(reddit_obj1['comments'][i]['comment_ans'], color='black',font="Arial-Bold",kerning=1, interline=1, size=(W-100, H-300), method='caption',fontsize=100).set_duration(audio_ans.duration))
        credits1 = credits1.set_position('center')
        colorclip = ColorClip(size=(W, H), color=(255,255,255)).set_duration(audio_ans.duration)
        final_clip1 = CompositeVideoClip([colorclip, credits1])
        final_clip1 = final_clip1.set_position('center')
        final_clip1.save_frame(f"out_ans{i}.png")
        final_clip1 = final_clip1.set_audio(audio_ans).fx( vfx.speedx, 0.9)
        time.sleep(2.4)
        # final = concatenate_videoclips([final1,countdown,final2])
        final = concatenate_videoclips([final_clip,final_clip1])
        # final = concatenate_videoclips([countdown])
        # final_clip2 = concatenate_videoclips([final_clip,countdown])
                
        final.write_videofile(
            f"results/{subreddit}/{folderNo}/{(i+1)}_{filename}",
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            fps=24,
            threads=24,
            ffmpeg_params=["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-pix_fmt", "yuv420p"],
        )

        W, H = 1280, 720
        # comment_full_1

        credits = (ImageClip(f"assets/temp/quiz_hindi/comment_full_{i}.png").set_duration(audio.duration).resize(width=W-100).set_opacity(new_opacity))
        credits = credits.set_position('center')
        colorclip = ColorClip(size=(W, H), color=(255,255,255)).set_duration(audio.duration)
        final_clip = CompositeVideoClip([colorclip, credits])
        final_clip = final_clip.set_position('center')
        final_clip.save_frame(f"out_que{i}.png")
        final_clip = final_clip.set_audio(audio).fx( vfx.speedx, 0.9)

        credits1 = (TextClip(reddit_obj1['comments'][i]['comment_ans'],color='black', font="Arial-Bold",kerning=1, interline=1, size=(W-100, H-100), method='caption').set_duration(audio_ans.duration))
        credits1 = credits1.set_position('center')
        colorclip = ColorClip(size=(W, H), color=(255,255,255)).set_duration(audio_ans.duration)
        final_clip1 = CompositeVideoClip([colorclip, credits1])
        final_clip1 = final_clip1.set_position('center')
        final_clip1.save_frame(f"out_ans{i}.png")
        final_clip1 = final_clip1.set_audio(audio_ans).fx( vfx.speedx, 0.9)
        time.sleep(2.4)
        final = concatenate_videoclips([final_clip,final_clip1])
        # Export the clip
        all_clip.append(final)
        # print(f"results/{subreddit}/{i}_{filename}")
    # exit()
    final_clip = concatenate_videoclips(all_clip)
    # video_clip = (
    #         VideoFileClip(f"assets/backgrounds/{back}.mp4")
    #             .loop(duration=final_clip.duration)
    #             .without_audio()
    #             .resize(width=W, height=H)
    #     )
    # final_clip = CompositeVideoClip([video_clip, final_clip])
    
        # f"results/{subreddit}/{folderNo}/{i}_{filename}"
    final_clip.write_videofile(
        f"results/{subreddit}/{folderNo}/final_{i}_{filename}",
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        fps=24,
        threads=24,
        ffmpeg_params=["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-pix_fmt", "yuv420p"],
    )

    print_step("Removing temporary files 🗑")
    # cleanups = cleanup()
    # print_substep(f"Removed {cleanups} temporary files 🗑")
    print_substep("See result in the results folder!")

    print_step(
        f'Reddit title: {reddit_obj1["thread_title"]} \n Background Credit: {background_config[2]}'
    )


# from moviepy.editor import *
# # Import the audio(Insert to location of your audio instead of audioClip.mp3)
# audio = AudioFileClip("AudioClip.mp3")
# # Import the Image and set its duration same as the audio (Insert the location of your photo instead of photo.jpg)
# clip = ImageClip("photo.jpg").set_duration(audio.duration)
# # Set the audio of the clip
# clip = clip.set_audio(audio)
# # Export the clip
# clip.write_videofile("render.mp4", fps=24)
