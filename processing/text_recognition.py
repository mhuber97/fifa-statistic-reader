import pytesseract

from image_processing import canny_operation


def read_text_pytesseract(image):
    config = r'--psm 7 --oem 3'
    result = pytesseract.image_to_string(image, config=config)
    return "".join(result.split("\n")[:-1])

def read_text(image):
    return easy_ocr_reader(image)
    #return detect_keras_ocr(image)

def read_string_from_box(image, top_left=None, bottom_right=None, canny=False):
    if not top_left:
        top_left = (0, 0)
    if not bottom_right:
        bottom_right = (image.shape[0], image.shape[1])
    img_box = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    
    #opened = opening_operation(img_box)
    #plt.imshow(opened)
    #plt.show()
    if canny:
        img_box = canny_operation(img_box)

    #plt.imshow(img_box)
    #plt.show()
    #result = easy_ocr_reader(img_box)
    result = read_text_pytesseract(img_box)
    return result
