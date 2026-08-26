# WhatsApp Bot - Playwright

Este proyecto es un bot automatizado para WhatsApp Web construido en Python utilizando **Playwright** y **PDM** como gestor de dependencias y proyectos.

## Requisitos Previos

- Python 3.9+
- PDM instalado (`pip install pdm` o `pipx install pdm`)
- Google Chrome o Chromium (Playwright lo descargará automáticamente)

## Instalación

1. Clona el repositorio o descarga los archivos.
2. Inicializa y sincroniza las dependencias con PDM:
   ```bash
   pdm install
   ```
3. Asegúrate de instalar los navegadores de Playwright:
   ```bash
   pdm run playwright install chromium
   ```

## Ejecución

Puedes ejecutar el bot de dos maneras:

**En Windows:**
Ejecuta el archivo `run_bot.bat` (doble clic) que contiene el comando para iniciar el bot sin que la consola se cierre al finalizar.

**En Linux / Mac:**
Ejecuta el archivo `run_bot.sh` desde la terminal:
```bash
chmod +x run_bot.sh
./run_bot.sh
```

**Ejecución manual:**
```bash
pdm run python main.py
```

### Flujo de Ejecución y Persistencia de Sesión
1. **Primera vez:** Al ejecutar el bot, si no tienes el número guardado, te pedirá por consola que lo ingreses (con el código de país, ej. `+5491123456789`). Este número se guarda de manera segura utilizando `keyring`. Luego, se abrirá el navegador y **se te pedirá escanear el código QR** de WhatsApp Web.
2. Una vez escaneado y enviado el mensaje exitosamente, el estado de la sesión se guarda en el archivo `storage_state.json`.
3. **Siguientes ejecuciones:** El bot utilizará el `storage_state.json` para saltarse el escaneo del QR y enviará el mensaje directamente.

## Patrones de Diseño Utilizados

Para garantizar un código limpio, mantenible y escalable, se implementaron los siguientes patrones de diseño:

### 1. Builder Pattern (`src/bot/builder.py`)
El patrón **Builder** se utiliza para simplificar la construcción y configuración de la instancia del bot (`BotBuilder`). Este patrón permite configurar opciones como si el navegador debe correr en modo *headless*, la ruta del archivo de sesión (`storage_state.json`) y la inicialización fluida de los componentes de Playwright (`browser`, `context`, `page`).

### 2. Page Object Model - POM (`src/pages/whatsapp_page.py`)
El patrón **Page Object Model (POM)** se utiliza para encapsular toda la lógica de interacción con la interfaz gráfica (DOM) de WhatsApp Web. La clase `WhatsAppPage` maneja los selectores, las esperas (`waits`) y las acciones (como escribir y hacer clic en enviar). Esto separa la lógica de negocio del bot de la lógica específica de la página web.

### 3. Strategy Pattern (`src/bot/strategy.py`)
El patrón **Strategy** se utiliza mediante la interfaz `MessagingStrategy` y su implementación concreta `WhatsAppStrategy`. Este patrón permite que el método de envío de mensajes sea intercambiable. Si en el futuro se desea agregar un bot de Telegram, simplemente se crea un `TelegramStrategy` sin tener que modificar la lógica del archivo principal `main.py`.
