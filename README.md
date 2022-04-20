# FIFA statistic reader
This repository uses computer vision to read the statistics from FIFA 21 menu screens and analyses the data.

## Requirements
We need the images that are required for the data extraction. Please create a directory `./data` and put them in there. 
Furthermore, we are using Tesseract and its python interface for the OCR. Please install both and put the english training data file into the `tessdata/` folder that can be often found in `/usr/share/tesseract-ocr/4.00/tessdata/`. For our purposes we used the english training data from `https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata`. To do that automatically, execute the following:

```sh
sudo apt install tesseract-ocr
pip install pytesseract
wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata
sudo mv ./eng.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
```

We use the following libraries that need to be installed:
- cv2
- matplotlib.pyplot
- numpy
- pandas
- os
- pytesseract
- re

## Usage
For the statistic extraction, please run the file `statistic_extractor.py`. It will generate a file `data.csv`.