from gtts import gTTS
from time import sleep
from playsound import playsound
from bs4 import BeautifulSoup
import requests
from pprint import pprint
from datetime import datetime, timedelta
import os


class Assistant:
    def __init__(self):
        self.__tts_loc = "temp/tts.mp3"
        self.__anger = 0
        self.__funcs = ["search", "create", "tell"]

        self.__alarm_noise = f"{'noises'}/{os.listdir('noises')[0]}"

    # ================================================================================================================ #
    def __text_to_speech(self, text: str):
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(self.__tts_loc)
        sleep_length = float(f"0.{len([letter for letter in text])}") * 5
        sleep(sleep_length)
        playsound(self.__tts_loc)

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

    def __timer(self, time: str):
        split_time = [char for char in time]
        wait_time = int("".join(split_time[:-1]))

        if "s" in split_time:
            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=wait_time)
            while True:
                if datetime.now().second == end_time.second:
                    playsound(self.__alarm_noise)
                    break
            return

        elif "m" in split_time:
            start_time = datetime.now()
            end_time = start_time + timedelta(minutes=wait_time)
            while True:
                if datetime.now().second == end_time.minute:
                    playsound(self.__alarm_noise)
                    break
            return

        elif "h" in split_time:
            start_time = datetime.now()
            end_time = start_time + timedelta(hours=wait_time)
            while True:
                if datetime.now().hour == end_time.hour:
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


Assistant().speak("create timer for 2s")
