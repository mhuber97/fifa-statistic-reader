import os

import cv2
import numpy as np
import pandas as pd
import pytesseract
from matplotlib import pyplot as plt

from dto.match import Match
from processing.data_cleaning import correcting_data
from processing.digit_recognition import detect_digit, detect_statistic_digits
from processing.image_processing import get_grayscale
from processing.text_recognition import read_string_from_box

# Pytesseract location
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

DATA_PATH = "../data"

def extract_match_statistics(image, library="E"):
    time = read_string_from_box(image, (800, 115), (1120, 155), library=library)
    home_name = read_string_from_box(image, (300, 155), (800, 220), library=library)
    away_name = read_string_from_box(image, (1120, 155), (1620, 220), library=library)
    
    home_score = detect_digit(image[150:230, 820:900], library=library)
    home_score = int(home_score) if home_score else int(-1)
    
    away_score = detect_digit(image[150:230, 1020:1110], library=library)
    away_score = int(away_score) if away_score else int(-1)
        
    home_team, away_team = detect_statistic_digits(image, library=library)
    home_team.name = home_name
    home_team.score = home_score
    away_team.name = away_name
    away_team.score = away_score
    
    cancelled = (home_score < 0) and (away_score < 0)
    match = Match(home=home_team, away=away_team, time=time, cancelled=cancelled)
    return match


if __name__ == "__main__":
    LIBRARY = "E" #E=EasyOCR; T=Tesseract; K=KerasOCR

    EXPECTED_RESOLUTION = (1080, 1920, 3)

    df = pd.DataFrame({"h_team": pd.Series(dtype='string'),\
                    "a_team": pd.Series(dtype='string'),\
                    "time": pd.Series(dtype='string'),\
                    "h_score": pd.Series(dtype='int'),\
                    "a_score": pd.Series(dtype='int'),\
                    "cancelled": pd.Series(dtype='bool'),\
                    "h_shots": pd.Series(dtype='int'),\
                    "h_shots_on_target": pd.Series(dtype='int'),\
                    "h_possession": pd.Series(dtype='int'),\
                    "h_tackles": pd.Series(dtype='int'),\
                    "h_fouls": pd.Series(dtype='int'),\
                    "h_corners": pd.Series(dtype='int'),\
                    "h_shot_acc": pd.Series(dtype='int'),\
                    "h_pass_acc": pd.Series(dtype='int'),\
                    "a_shots": pd.Series(dtype='int'),\
                    "a_shots_on_target": pd.Series(dtype='int'),\
                    "a_possession": pd.Series(dtype='int'),\
                    "a_tackles": pd.Series(dtype='int'),\
                    "a_fouls": pd.Series(dtype='int'),\
                    "a_corners": pd.Series(dtype='int'),\
                    "a_shot_acc": pd.Series(dtype='int'),\
                    "a_pass_acc": pd.Series(dtype='int'),\
                    "filename": pd.Series(dtype='string')
                    })

    file_list = [f for f in os.listdir(DATA_PATH) if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg")]
    number_total_image = len(file_list)

    for idx, filename in enumerate(file_list):
        image = cv2.imread(DATA_PATH + "/" + filename)
        if image.shape != EXPECTED_RESOLUTION:
            image = cv2.resize(image, dsize=(EXPECTED_RESOLUTION[1], EXPECTED_RESOLUTION[0]), interpolation=cv2.INTER_NEAREST)

        if LIBRARY != "K":
            image = get_grayscale(image)
        
        try:
            match = extract_match_statistics(image, library=LIBRARY)
            df = pd.concat([df, match.get_data_frame(filename)])
        except Exception as err: 
            print("Problem with file " + filename)
            print(repr(err))

        if (idx%50) == 0:
            print(str(idx) + "/" + str(number_total_image))

    df = correcting_data(df)
    df.to_csv("data_{}.csv".format(LIBRARY), index=False)
