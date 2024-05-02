import time

import pytesseract
from PIL import Image, ImageEnhance
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://services.gst.gov.in/services/searchtpbypan")
driver.maximize_window()
input_gstin = driver.find_element(By.ID, 'for_gstin')
input_gstin.send_keys('A')

time.sleep(2)
element = driver.find_element(By.ID, 'imgCaptcha')
element.screenshot("test/image.png")

img = Image.open("test/image.png")
# enhance contrast
enhancer = ImageEnhance.Contrast(img)
contrast_factor = 1
enhanced_img = enhancer.enhance(contrast_factor)
enhanced_img.save("test/enh.png")

threshold = 1  # Adjust as needed
black_and_white_img = enhanced_img.point(lambda x: 0 if x < threshold else 200)
# Save the black-and-white image
black_and_white_img.save("test/black_and_white.png")

# convert to grayscale
gray_img = black_and_white_img.convert('L')
gray_img.save("test/gray_scale.png")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

text = pytesseract.image_to_string(gray_img, config='--psm 10')
print("Text : ", text)


