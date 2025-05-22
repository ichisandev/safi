# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# import time
# import base64
#
# # Configure firefox WebDriver options
# options = Options()
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Use headless mode for running in the background
# options.add_argument("--disable-gpu")
#
#
# def get_link_ss(link):
#     # Initialize the firefox WebDriver
#     driver = webdriver.Firefox(options=options)
#     driver.maximize_window()
#
#     # Navigate to the URL you want to capture
#     driver.get(link)
#
#     # Wait for the page to load (you can adjust the sleep time as needed)
#     time.sleep(2)
#
#     # Use JavaScript to get the full height of the webpage
#     height = driver.execute_script(
#         "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
#     )
#
#     # Set the window size to match the entire webpage
#     driver.set_window_size(height=height, width=1920)
#
#     screenshot = driver.get_screenshot_as_png()
#     image_base64 = base64.b64encode(screenshot).decode("utf-8")
#
#     # Close the browser window
#     driver.quit()
#     return image_base64
