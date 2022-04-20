pip install easyocr
apt install tesseract-ocr
pip install pytesseract

wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata
mv ./eng.traineddata /usr/share/tesseract-ocr/4.00/tessdata/

pip install cv2, matplotlib, numpy, pandas, os, re