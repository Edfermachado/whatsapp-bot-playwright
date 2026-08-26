from playwright.sync_api import sync_playwright, Page
import os

class BotBuilder:
    def __init__(self):
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
        self._storage_state_path = "storage_state.json"
        self._headless = False

    def set_storage_path(self, path: str):
        self._storage_state_path = path
        return self

    def set_headless(self, headless: bool):
        self._headless = headless
        return self

    def build(self) -> Page:
        self._playwright = sync_playwright().start()
        # Headless mode should be False for WhatsApp Web as it requires scanning QR and sometimes headless is detected
        self._browser = self._playwright.chromium.launch(headless=self._headless)
        
        # Check if storage state exists for session persistence
        if os.path.exists(self._storage_state_path):
            print(f"Cargando sesión guardada desde {self._storage_state_path}")
            self._context = self._browser.new_context(storage_state=self._storage_state_path)
        else:
            print("No se encontró sesión guardada. Se requerirá escanear el QR.")
            self._context = self._browser.new_context()

        self._page = self._context.new_page()
        return self._page

    def save_session(self):
        if self._context:
            self._context.storage_state(path=self._storage_state_path)
            print(f"Sesión guardada en {self._storage_state_path}")

    def teardown(self):
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
