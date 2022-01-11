import os
import requests
from dotenv import load_dotenv
import telegram



def main():
    load_dotenv()
    dvmn_token = os.getenv('DEVMAN_TOKEN')
    tg_token = os.getenv('TG_BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    
    url = 'https://dvmn.org/api/long_polling/'
    payload = {}
    headers = {'Authorization': f'Token {dvmn_token}'}
    bot = telegram.Bot(token=tg_token)

    while True:
        try:
            response = requests.get(url, headers=headers, params=payload, timeout=100)
            response.raise_for_status()
            response = response.json()
            if response['status'] == 'found':
                payload = {'timestamp': response['last_attempt_timestamp']}
                lessons = response['new_attempts']
                for lesson in lessons:
                    lesson_title = lesson['lesson_title']
                    lesson_url = lesson['lesson_url']
                    if lesson['is_negative']:
                        comment = 'К сожалению, в работе нашлись ошибки.'
                    else:
                        comment = 'Преподавателю всё понравилось, можно приступать к следующему уроку!'
                    bot.send_message(text=f'У вас проверили работу "{lesson_title}" {lesson_url} \n {comment}', 
                        chat_id=chat_id)
            elif response['status'] == 'timeout':
                payload = {"timestamp": response['timestamp_to_request']}
                bot.send_message(text='У вас нет работ на проверке!', chat_id=chat_id)
        except requests.exceptions.Timeout:
            print('Timeout occurred')
        except requests.exceptions.ConnectionError:
            print('No connection')
        


if __name__ == '__main__':
    main()


