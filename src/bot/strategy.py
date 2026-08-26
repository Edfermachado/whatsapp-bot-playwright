from abc import ABC, abstractmethod
from playwright.sync_api import Page
from src.pages.whatsapp_page import WhatsAppPage

class MessagingStrategy(ABC):
    @abstractmethod
    def send_message(self, page: Page, target: str, message: str) -> None:
        pass

class WhatsAppStrategy(MessagingStrategy):
    def send_message(self, page: Page, target: str, message: str) -> None:
        whatsapp_page = WhatsAppPage(page)
        whatsapp_page.navigate_to_chat(target)
        whatsapp_page.wait_for_login()
        whatsapp_page.send_message(message)
