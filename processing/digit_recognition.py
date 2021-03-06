import cv2
import easyocr
import keras_ocr
import numpy as np
import pytesseract
from dto.team import Team
from matplotlib import pyplot as plt

from .image_processing import (apply_brightness_contrast, erode_operation,
                               opening_operation, thresholding_operation)

# Pytesseract location
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

pipeline = keras_ocr.pipeline.Pipeline()
reader = easyocr.Reader(["en"], gpu=True)

def detect_digit(image, library="E"):
     match library:
        case "E":
            return easyocr_detect_digit(image)
        case "T":
            return pytesseract_detect_digit(image)
        case "K":
            return kerasocr_detect_digit(image)

def kerasocr_detect_digit(image):
    results = pipeline.recognize([image])[0]
    if len(results) > 0 and results[0][0].isdigit():
      return int(results[0][0])
    else:
      return None

def pytesseract_detect_digit(image):
    custom_config = r'--oem 0 --psm 6 outputbase digits'
    result = pytesseract.image_to_string(image, config=custom_config)
    result = result.splitlines()
    if len(result) > 1 and str(result[0]).isdigit(): # pytesseract returns an empty result as the last index
      return int(result[0])
    else:
      return None

def easyocr_detect_digit(image):
    results = reader.readtext(image, allowlist="1234567890", detail=0)
    if len(results) > 0:
      return int(results[0])
    else:
      return None

def create_team_stats_from_result_list(stats):
    assert(len(stats) == 8)
    return Team(
        shots = stats[0], 
        shots_on_target = stats[1], 
        possession = stats[2],
        tackles = stats[3],
        fouls = stats[4],
        corners = stats[5],
        shot_acc = stats[6],
        pass_acc = stats[7]
    )

def read_statistic_column(image, home=True, library="E"):
    start = 295
    statistics = np.zeros(8, dtype="int")

    for range_images in range(8):

        image_index = range_images*33+start
        if home:
            img_box = image[int(image_index*1.5):int((image_index+30)*1.5), int(1.777*575):int(1.777*600)] # left column
        else:
            img_box = image[int(image_index*1.5):int(1.5*(image_index+30)), int(1.777*955):int(1.777*980)] #right column
        
        if np.mean(img_box) > 100:
              img_box = (255-img_box)

        img = img_box.copy()

        if library != "K": # kerasOCR only supports RGB images for which this operation does not work
            (thresh, img) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

        img = cv2.resize(img, dsize=(img.shape[0]*3, img.shape[1]*3), interpolation=cv2.INTER_LINEAR) 
        img = cv2.blur(img, (3, 3))

        result = detect_digit(img, library=library)

        if result is not None: 
            np.put(statistics, range_images, result)
        else:
            np.put(statistics, range_images, int(-1))
    return statistics
    
def detect_statistic_digits(image, library="E"):
    # make image smaller for faster processing
    image = cv2.resize(image, dsize=(1080, 720), interpolation=cv2.INTER_NEAREST) 
    home = read_statistic_column(image, home=True, library=library)
    away = read_statistic_column(image, home=False, library=)
    home_team_stats = create_team_stats_from_result_list(home)
    away_team_stats = create_team_stats_from_result_list(away)
    return home_team_stats, away_team_stats
