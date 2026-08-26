from playwright.sync_api import Page
import time

class WhatsAppPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_chat(self, phone: str):
        # Navegar directamente al chat con el número indicado
        url = f"https://web.whatsapp.com/send?phone={phone}"
        self.page.goto(url, wait_until="domcontentloaded")

    def wait_for_login(self):
        # Esperar a que la interfaz principal cargue
        # Si no hay sesión, se mostrará el QR y el usuario deberá escanearlo.
        # #main es el contenedor principal que aparece cuando un chat está abierto.
        print("Esperando a que cargue el chat (escanea el código QR si es necesario)...")
        self.page.wait_for_selector("#main", timeout=120000) # 2 minutos de tiempo de espera
        print("Chat cargado correctamente.")

    def send_message(self, message: str):
        print(f"Enviando mensaje:\n{message}")
        # El cuadro de texto tiene un contenteditable y está dentro del footer.
        textbox = self.page.locator('#main footer div[contenteditable="true"]')
        textbox.wait_for(state="visible")
        # Forzamos el click en caso de que Playwright considere que hay un elemento superpuesto
        textbox.click(force=True)
        
        # En el editor moderno de WhatsApp (Lexical), 'fill' a veces no dispara los eventos de React.
        # Además, al usar '\n', Playwright puede enviar el mensaje prematuramente. 
        # La solución es dividir por líneas y usar Shift+Enter para los saltos de línea.
        for i, line in enumerate(message.split('\n')):
            self.page.keyboard.insert_text(line)
            if i < len(message.split('\n')) - 1:
                self.page.keyboard.press("Shift+Enter")
                
        time.sleep(0.5)
        
        # Enviar usando la tecla Enter
        self.page.keyboard.press("Enter")
        # Esperar un momento para asegurar que el mensaje fue enviado antes de cerrar
        time.sleep(2)
        print("Mensaje enviado.")
