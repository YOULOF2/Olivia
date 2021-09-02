from gtts import gTTS
from playsound import playsound
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import os
from random import choice
import json


class Assistant:
    """
    Assistant class responsible to the responses of the assistant.

    Assistant commands supported:
    1. search meaning of [PHRASE]
    2. create timer for [TIME][s/m/h]
    3. tell me a joke
    """

    def __init__(self):
        self.__tts_loc = "temp/tts{}.mp3"
        self.__cur_temp_file_num = 0
        self.__anger = 1.9
        self.__funcs = ["search", "create", "tell"]

        self.__alarm_noise = f"{'noises'}/{os.listdir('noises')[0]}"

    # ================================================================================================================ #
    def __text_to_speech(self, text: str, **kwargs):
        sync_state = kwargs.get("sync", True)
        if self.__anger > 2:
            text = f"hhh........{text}"
        tts = gTTS(text=text, lang="en", slow=False)
        self.__cur_temp_file_num += 1
        file_name = self.__tts_loc.format(self.__cur_temp_file_num)
        tts.save(file_name)
        playsound(file_name, block=sync_state)

    # ================================================================================================================ #
    def __search(self, text: str):
        if text.split()[:2] == ["meaning", "of"]:
            search_term = "%20".join(text.split()[2:])
            html_page = requests.get(f"https://www.urbandictionary.com/define.php?term={search_term}").text
            soup = BeautifulSoup(html_page, 'html.parser')
            try:
                definition = soup.select_one(".meaning").text
            except AttributeError:
                self.__anger += 1
                return "No results found. Thanks for wasting my time.."
            return f"From urban dictionary.. {definition}"

    # ================================================================================================================ #

    def __timer(self, time: str):
        split_time = [char for char in time]
        wait_time = int("".join(split_time[:-1]))

        if "s" in split_time:
            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=wait_time)
            while True:
                if datetime.now().second == end_time.second:
                    self.__text_to_speech("Timer is up!", sync=False)
                    playsound(self.__alarm_noise)
                    break
            return

        elif "m" in split_time:
            start_time = datetime.now()
            end_time = start_time + timedelta(minutes=wait_time)
            while True:
                if datetime.now().second == end_time.minute:
                    self.__text_to_speech("Timer is up!", sync=False)
                    playsound(self.__alarm_noise)
                    break
            return

        elif "h" in split_time:
            start_time = datetime.now()
            end_time = start_time + timedelta(hours=wait_time)
            while True:
                if datetime.now().hour == end_time.hour:
                    self.__text_to_speech("Timer is up!", sync=False)
                    playsound(self.__alarm_noise)
                    break
            return

    # ================================================================================================================ #
    def speak(self, text: str):
        # segments the text inputed to a list 👇
        segmented_text = text.split(" ")
        # searches for keywords in segmented_text 👇
        if segmented_text[0] in self.__funcs:
            keyword = segmented_text[0]

            if keyword == self.__funcs[0]:
                joined_str = " ".join(segmented_text[1:])
                result = self.__search(joined_str)
                self.__text_to_speech(result)
                return result

            elif keyword == self.__funcs[1]:

                if segmented_text[1:3] == ["timer", "for"]:
                    self.__timer(segmented_text[3])

            elif keyword == self.__funcs[2]:

                with open("jokes.json") as file:
                    json_data = json.load(file)
                if segmented_text[1:4] == ["me", "a", "joke"]:
                    if self.__anger >= 2:
                        joke = choice(json_data.get("offensive"))
                        self.__text_to_speech(joke[0])
                        self.__text_to_speech(joke[1])
                    else:
                        joke = choice(json_data.get("normal"))
                        self.__text_to_speech(joke[0])
                        self.__text_to_speech(joke[1])
                    playsound("noises/drums.mp3")
        else:
            self.__anger += 0.5


