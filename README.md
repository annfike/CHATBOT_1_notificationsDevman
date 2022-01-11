# Devman - check

Сервис для отправки уведомлений о проверке работ в учебных модулях на сайте [Devman](https://dvmn.org/).

### Как установить

 - Для использования скрипта необходимо получить токен от Телеграм-бота, узнать ваш chat_id в Телеграме и токен на сайте Devman.
 - Полученные токены присвоить переменным окружения в файле ".env":
```python
   DEVMAN_TOKEN=ВашТокен
   
   TG_BOT_TOKEN=ВашТокен

   CHAT_ID=ваш chat_id в Телеграме
```
 - Python3 должен быть уже установлен.
 - Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```python
   pip install -r requirements.txt
   ```
 - Для запуска скрипта используйте команду:
```python
   python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).