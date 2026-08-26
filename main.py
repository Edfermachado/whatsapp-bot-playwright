import keyring
from src.bot.builder import BotBuilder
from src.bot.strategy import WhatsAppStrategy

def get_target_phone() -> str:
    service_name = "whatsapp_bot"
    username = "target_phone"
    phone = keyring.get_password(service_name, username)
    if not phone:
        phone = input("Por favor, ingresa el número de teléfono con código de país (ej. +5491123456789): ")
        keyring.set_password(service_name, username, phone)
        print("Número guardado en el keyring del sistema.")
    else:
        print(f"Número recuperado del keyring: {phone}")
    return phone

def main():
    phone = get_target_phone()
    
    # Mensaje a enviar
    message = (
        "Tarea finalizada.\n"
        "Patrones utilizados: Builder, Page Object Model, Strategy."
    )

    # Patrón Builder para configurar el bot
    builder = BotBuilder().set_headless(False).set_storage_path("storage_state.json")
    page = builder.build()

    try:
        # Patrón Strategy para enviar el mensaje por WhatsApp
        strategy = WhatsAppStrategy()
        strategy.send_message(page, phone, message)

        # Guardar sesión después de un envío exitoso (o un inicio de sesión)
        builder.save_session()
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        builder.teardown()

if __name__ == "__main__":
    main()
