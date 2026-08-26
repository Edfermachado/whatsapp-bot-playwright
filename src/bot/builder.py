from playwright.sync_api import sync_playwright, Page
import os

class BotBuilder:
    def __init__(self):
        self._playwright = None
        self._context = None
        self._page = None
        self._user_data_dir = "whatsapp_session"
        self._headless = False

    def set_user_data_dir(self, path: str):
        self._user_data_dir = path
        return self
        
    def set_storage_path(self, path: str):
        # Mantenemos este método para compatibilidad con main.py
        # Usamos el nombre base sin extensión
        self._user_data_dir = path.replace(".json", "")
        return self

    def set_headless(self, headless: bool):
        self._headless = headless
        return self

    def build(self) -> Page:
        self._playwright = sync_playwright().start()
        
        print(f"Iniciando sesión persistente en: {self._user_data_dir}")
        # Usamos launch_persistent_context en lugar de storage_state
        # Esto es vital para WhatsApp Web porque usa IndexedDB (el cual storage_state no guarda).
        self._context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=self._user_data_dir,
            headless=self._headless
        )

        # En contextos persistentes se abre una pestaña por defecto
        if len(self._context.pages) > 0:
            self._page = self._context.pages[0]
        else:
            self._page = self._context.new_page()
            
        return self._page

    def save_session(self):
        # Con launch_persistent_context, se guarda todo al vuelo de forma automática.
        print(f"Sesión persistida automáticamente en el directorio {self._user_data_dir}")

    def teardown(self):
        if self._context:
            self._context.close()
        if self._playwright:
            self._playwright.stop()
