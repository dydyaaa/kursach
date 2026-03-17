import requests
import json
import urllib3
import os
import uuid
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_access_token() -> str:
    """
    Функция, генерирующая access_token для Gigachat

    Возвращает:
    result (str): access_token
    """
    load_dotenv()
    new_uuid = uuid.uuid4()
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': f'{new_uuid}',
        'Authorization': f'Basic {os.getenv("GIGACHAT_AUTHORIATION")}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    response_json = response.json()
    result = response_json['access_token']
    return result


def gigachat_answer(prompt: str, for_dev: bool = False) -> str:
    """
    Генерирует ответ с использованием модели Gigachat на основе заданного промпта.

    Аргументы:
    prompt (str): Текст промпта для генерации ответа.

    Возвращает:
    result (str): Сгенерированный ответ на основе промпта в виде строки.
    """
    access_token = get_access_token()
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": f'{prompt}'
            }
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response_json = response.json()
        result = response_json['choices'][0]['message']['content']
        if for_dev:
            with open(os.getenv("AI_RECOMMENDATION_PATH_DEV"), "w") as f:
                print(result)
                f.write(result.replace("*", "").replace("#", ""))
        else:
            with open(os.getenv("AI_RECOMMENDATION_PATH"), "w") as f:
                print(result)
                f.write(result.replace("*", "").replace("#", ""))
        return result
    except Exception as e:
        result = str(e)
        return result

