import os
import time
import requests
from dotenv import load_dotenv
import telegram
import logging


logger = logging.getLogger(__file__)

class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()
    dvmn_token = os.getenv('DEVMAN_TOKEN')
    tg_token = os.getenv('TG_BOT_TOKEN')
    tg_token_admin = os.getenv('TG_BOT_ADMIN_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    
    url = 'https://dvmn.org/api/long_polling/'
    payload = {}
    headers = {'Authorization': f'Token {dvmn_token}'}
    bot = telegram.Bot(token=tg_token)
    tg_bot = telegram.Bot(token=tg_token_admin)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(tg_bot, chat_id))
    logger.info('Бот запущен.')

    while True:
        try:
            response = requests.get(url, headers=headers, params=payload, timeout=100)
            response.raise_for_status()
            dvmn_lessons_check = response.json()
            if dvmn_lessons_check['status'] == 'found':
                payload = {'timestamp': dvmn_lessons_check['last_attempt_timestamp']}
                lessons = dvmn_lessons_check['new_attempts']
                for lesson in lessons:
                    lesson_title = lesson['lesson_title']
                    lesson_url = lesson['lesson_url']
                    if lesson['is_negative']:
                        comment = 'К сожалению, в работе нашлись ошибки.'
                    else:
                        comment = 'Преподавателю всё понравилось, можно приступать к следующему уроку!'
                    bot.send_message(text=f'У вас проверили работу "{lesson_title}" {lesson_url} \n {comment}', 
                        chat_id=chat_id)
            elif dvmn_lessons_check['status'] == 'timeout':
                payload = {"timestamp": dvmn_lessons_check['timestamp_to_request']}
        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(20)
        except Exception:
            logger.exception('Ошибка!')
        


if __name__ == '__main__':
    main()


