import time
from datetime import datetime
from typing import List, Tuple

import chromedriver_autoinstaller
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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


# TODO: client can create an account for using chatGPT

# TODO: spam detection bans user!

# TODO: maximum 3 messages per minute


class Logger:
    def read_logs():
        ...

    def add_log():
        ...


class ChatPage:
    def __init__(self, wd: webdriver.Chrome, robot_name: str) -> None:
        self.wd = wd
        self.robot_name = robot_name

    def collect_clients_with_messages(self) -> List[str]:
        clients = self.wd.find_elements(
            By.XPATH,
            "//div[./div[@aria-colindex='2'] and .//span[contains(@aria-label, 'unread message')]]/div[@aria-colindex='2']//span",
        )

        clients = [client.text for client in clients]
        return clients

    def enter_client_chat(self, client: str) -> None:
        searchbar_el = self.wd.find_element(
            By.XPATH, "//div[@title='Search input textbox']"
        )

        searchbar_el.clear()
        searchbar_el.send_keys(client)

        self.wd.find_element(
            By.XPATH,
            f"//span[@title='{client}']",
        ).click()

        searchbar_el.clear()

        self.wd.find_element(By.XPATH, "//span[@data-testid='search']").click()
        self.wd.find_element(By.XPATH, "//span[@data-icon='x-alt']").click()

    def get_client_messages(self, client: str) -> List[Tuple[str, str]]:

        self.enter_client_chat(client)

        # depois de coletar as mensagens, o robo vai para a conversa "eu mesmo" e limpa o searchbar

        message_root_xpath = (
            "//div[contains(@class,'message-in')][//span[contains(@class, 'text')]]"
        )

        message_texts = self.wd.find_elements(
            By.XPATH, message_root_xpath + "//span[contains(@class, 'text')]/span"
        )
        message_texts = [message_text.text for message_text in message_texts]

        message_dates = self.wd.find_elements(
            By.XPATH, message_root_xpath + "//div[@data-testid='msg-meta']/span"
        )

        message_dates = [message_date.text for message_date in message_dates]

        message_infos = list(zip(message_texts, message_dates))

        self.enter_client_chat(self.robot_name)

        return message_infos

    def reply_client(self, client: str, reply_message: str) -> None:
        ...


def main():

    chromedriver_autoinstaller.install()

    with webdriver.Chrome() as wd:
        wd.implicitly_wait(5)
        QRCodePage(wd).wait_manual_QRCode_scan()

        while True:
            time.sleep(5)

            chatpage = ChatPage(wd, "Eu Mesmo")
            print("coletando mensagens não lidas...")
            clients = chatpage.collect_clients_with_messages()

            for client in clients:
                print(f"Coletando mensagens de {client}...")
                messages = chatpage.get_client_messages(
                    "Mariana Prado"
                )  # TODO: TROCAR ISSO

                print(f"Mensagens de {client}:\n" + str(messages))


if __name__ == "__main__":
    main()
