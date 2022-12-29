import time

import chromedriver_autoinstaller
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


class QRCodePage:
    def __init__(self, wd: webdriver.Chrome) -> None:
        self.wd = wd
        self.url = "https://web.whatsapp.com/"

    def wait_manual_QRCode_scan(self) -> None:

        self.wd.get(self.url)

        self.wd.find_element(By.XPATH, "//canvas[@aria-label='Scan me!']")
        self.wd.save_screenshot("./QRCode/QRCode.png")
        print("QR Code saved.")
        input("Scan it and press ENTER\n->")


def main():

    chromedriver_autoinstaller.install()

    with webdriver.Chrome() as wd:
        wd.implicitly_wait(5)
        QRCodePage(wd).wait_manual_QRCode_scan()


if __name__ == "__main__":
    main()
