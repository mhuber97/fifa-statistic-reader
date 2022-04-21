import cv2
import numpy as np
import pytesseract
from dto.team import Team
from matplotlib import pyplot as plt

from .image_processing import (apply_brightness_contrast, erode_operation,
                               opening_operation, thresholding_operation)

# Pytesseract location
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def detect_statistic_digits_pytesseract(image):
    if np.mean(image) > 100:
      image = (255-image)
    image = apply_brightness_contrast(image, brightness=100, contrast=-300)
    image = thresholding_operation(image)
    image = opening_operation(image)
    image = cv2.resize(image, dsize=(int(image.shape[1]*1.5), image.shape[0]), interpolation=cv2.INTER_NEAREST)
    config = r'--psm 6 --oem 0 outputbase digits'
    result = pytesseract.image_to_string(image, config=config)
    return result.split("\n")[:-1]

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

def read_statistic_column(image, home=True):
    custom_config = r'--oem 0 --psm 8 outputbase digits'
    start = 295
    statistics = np.zeros(8, dtype="int")

    for range_images in range(8):

        image_index = range_images*33+start
        if home:
            img_box = image[image_index:image_index+30, 575:600] # left column
        else:
            img_box = image[image_index:image_index+30, 955:980] #right column
        
        if np.mean(img_box) > 100:
              img_box = (255-img_box)

        h, w = img_box.shape
        img = img_box.copy()
        img = cv2.resize(img, (w*5,h*3), cv2.INTER_NEAREST)

        (thresh, img) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

        img = erode_operation(img, 2, 2, 1)
        result = pytesseract.image_to_string(img, config=custom_config)
        result = result.splitlines()
        
        if len(result) > 1 and str(result[0]).isdigit(): # pytesseract returns an empty result as the last index
            np.put(statistics, range_images, int(result[0]))
        else:
            np.put(statistics, range_images, int(-1))
    return statistics
    
def detect_statistic_digits(image):
    # make image smaller for faster processing
    image = cv2.resize(image, dsize=(1080, 720), interpolation=cv2.INTER_NEAREST) 
    home = read_statistic_column(image, home=True)
    away = read_statistic_column(image, home=False)
    home_team_stats = create_team_stats_from_result_list(home)
    away_team_stats = create_team_stats_from_result_list(away)
    return home_team_stats, away_team_stats
