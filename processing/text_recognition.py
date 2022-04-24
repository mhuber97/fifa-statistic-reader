import easyocr
import keras_ocr
import pytesseract

pipeline = keras_ocr.pipeline.Pipeline()
reader = easyocr.Reader(["en"], gpu=True)


def detect_text(image, library="E"):
     match library:
        case "E":
            return easyocr_detect_text(image)
        case "T":
            return pytesseract_detect_text(image)
        case "K":
            return kerasocr_detect_text(image)

def pytesseract_detect_text(image):
    config = r'--psm 7 --oem 0'
    result = pytesseract.image_to_string(image, config=config)
    return "".join(result.split("\n")[:-1])

def kerasocr_detect_text(image):
    detections = pipeline.recognize([image])[0]
    recognized_text = ""
    for i in detections:
        recognized_text = recognized_text + " " + i[0]
    return recognized_text.strip()

def easyocr_detect_text(image):
    result = reader.readtext(image, detail = 0)
    if len(result) > 0 :
        return result[0]
    else:
        return None

def read_string_from_box(image, top_left=None, bottom_right=None, library="E"):
    if not top_left:
        top_left = (0, 0)
    if not bottom_right:
        bottom_right = (image.shape[0], image.shape[1])
    img_box = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    result = detect_text(img_box, library=library)
    return result
