import cv2
import numpy as np
import pytesseract
from dto.team import Team
from matplotlib import pyplot as plt

from image_processing import (apply_brightness_contrast, dilate_operation,
                              thresholding_operation)


def detect_keras_ocr(image):
    image = cv2.blur(image, (3, 3))
    plt.imshow(image)
    plt.show()
    detections = pipeline.recognize([image])[0]
    recognized_text = ""
    for i in detections:
        recognized_text = recognized_text + " " + i[0]
    return recognized_text.strip()


def easy_ocr_reader(image):
    result = reader.readtext(image, detail = 0)
    if len(result) > 0 :
        return result[0]
    else:
        return None


def detect_statistic_digits_pytesseract(image):
    if np.mean(image) > 100:
      image = (255-image)
    image = apply_brightness_contrast(image, brightness=100, contrast=-300)
    image = thresholding_operation(image)
    image = dilate_operation(image)
    #plt.imshow(image)
    #plt.show()
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

    
def detect_statistic_digits(image):
    home = detect_statistic_digits_pytesseract(image[440:850, 970:1120])
    away = detect_statistic_digits_pytesseract(image[440:850, 1650:1760])
    home_team_stats = create_team_stats_from_result_list(home)
    away_team_stats = create_team_stats_from_result_list(away)
    return home_team_stats, away_team_stats
