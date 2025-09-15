import requests
from dotenv import load_dotenv
import os
load_dotenv()

def send_telegram_message(token: str, chat_id: str, message: str) -> bool:
    """
    Envia uma mensagem para um chat do Telegram usando Bot API.
    
    Args:
        token (str): Token do bot do Telegram.
        chat_id (str): ID do chat ou usuário.
        message (str): Texto da mensagem a ser enviada.
    
    Returns:
        bool: True se a mensagem foi enviada com sucesso, False caso contrário.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # levanta erro se status code não for 2xx
        return True
    except requests.RequestException as e:
        print(f"Erro ao enviar mensagem: {e}")
        return False


if __name__ == "__main__":

    # Apenas para testar rodando via terminal!
    # Função deve ser atribuida a um callback no rabbitMQ

    token = os.getenv("TOKEN_TELEGRAM")
    chat_id = os.getenv("CHAT_ID")
    message = "Oi, estou no Telegram"

    if not token or not chat_id:
        raise ValueError("TOKEN_TELEGRAM e CHAT_ID devem estar definidos no .env")

    sucess = send_telegram_message(token, chat_id, message)
    print("Mensagem enviada!" if sucess else "Falha ao enviar mensagem")