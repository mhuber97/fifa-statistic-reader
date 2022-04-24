# FIFA statistic reader
This repository uses computer vision to read the statistics from FIFA 21 menu screens and analyses the data.

## Requirements
We need Python 3.10 or newer.
We need the images that are required for the data extraction. Please create a directory `./data` and put them in there. 
Please install the requirements with the script `install_requirements.sh`. This entails a download of english training data for the legacy engine of Tesseract. The default location of Tesseract is in `/usr/share/tesseract-ocr/4.00/tessdata/`. If your setup is different, please change the path in the file. 
Furthermore, we are using Tesseract and its python interface for the OCR.

```sh
sh install_requirements.sh
```

We use the following libraries that need to be installed:
- cv2
- matplotlib.pyplot
- numpy
- pandas
- os
- pytesseract
- easyocr
- keras-ocr
- re

## Usage
For the statistic extraction, please run the file `statistic_extractor.py`. It will generate a file `data.csv`. By default the extraction is using the EasyOCR library. You can change that by modifying the variable `LIBRARY` in `statistic_extractor.py` line 43 into:
- E = EasyOCR
- T = Tesseract
- K = KerasOCR
