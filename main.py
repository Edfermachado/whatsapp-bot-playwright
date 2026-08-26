import keyring
from src.bot.builder import BotBuilder
from src.bot.strategy import WhatsAppStrategy

def get_target_phone() -> str:
    # Se fija el número destinatario tal como lo solicitaste
    return "+5804244553000"

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
