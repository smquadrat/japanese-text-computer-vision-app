# japanese-text-computer-vision-app

This Flask app enables users to upload an image containing Japanese text (kanji, hiragana or katakana) and receive an output of the image with overlaid English translations along with a table containing raw input text and translated output text. The app utilizes the OpenCV Python library to preprocess uploaded images, the Tesseract OCR (optical character recognition) computer vision engine via the PyOCR Python wrapper to identify Japanese text and the Google Translate api to translate to English. A sample image is provided for illustrative purposes.

Images are preprocessed using the following methods via the OpenCV Python library:
- Conversion to grayscale / black and white
- Noise reduction / removal
- Smoothing of edges

Output results may vary depending on factors such as text clarity, lighting and resolution.

**Input Screen:**

![japanese_ocr _screenshot_1](https://user-images.githubusercontent.com/41703555/233539168-11ada1d9-ce02-45e9-a237-6a093ca6a21d.JPG)

**Output Screen:**

![japanese_ocr_screenshot_2](https://user-images.githubusercontent.com/41703555/233539173-4ed6d89f-b8a0-4ef1-851b-e69823d75983.JPG)
