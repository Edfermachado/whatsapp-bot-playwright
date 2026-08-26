import keyring
from src.bot.builder import BotBuilder
from src.bot.strategy import WhatsAppStrategy

def get_target_phone() -> str:
    service_name = "whatsapp_bot"
    username = "target_phone"
    saved_phone = keyring.get_password(service_name, username)
    
    if saved_phone:
        print(f"\nTeléfono destino guardado actualmente: {saved_phone}")
        phone = input("Presiona Enter para usar este número, o escribe uno nuevo: ").strip()
        if not phone:
            return saved_phone
    else:
        phone = input("Por favor, ingresa el número de teléfono destino con código de país (ej. +5491123456789): ").strip()
        while not phone:
            phone = input("El número no puede estar vacío. Ingresa el número: ").strip()
            
    keyring.set_password(service_name, username, phone)
    print("Número actualizado/guardado en el keyring del sistema.")
    return phone

def main():
    phone = get_target_phone()
    
    # Mensaje a enviar
    message = (
        "Tarea finalizada.\n"
        "Patrones utilizados: Builder, Page Object Model, Strategy."
    )

    # Patrón Builder para configurar el bot
    builder = BotBuilder().set_headless(False).set_user_data_dir("whatsapp_session")
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
