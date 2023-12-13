# Распознаём речь.

![](https://ltdfoto.ru/images/2023/12/08/Screencast-from-12-08-2023-03_54_07-PM.gif)

![](https://ltdfoto.ru/images/2023/12/08/Screencast-from-12-08-2023-04_00_41-PM.gif)

Ссылка на [Группу VK](https://vk.com/club223677588) и [Телеграмм](https://t.me/RecognizingSpeech_bot)

Бот-помощник в TG и VK
## Установка 

Установите [python3](https://realpython.com/installing-python/).

## Репозиторий
Клонируйте репозиторий в удобную папку.

## Виртуальное окружение
В терминале перейдите в папку с репозиторием.

### Создание виртуального окружения
```bush 
python3 -m venv venv
```

### Активация виртуального окружения Linux

```bush
source venv/bin/activate
```

### Активация виртуального окружения Windows

```bush
venv\Scripts\activate
```

### Установка библиотек

```bush 
pip3 install -r requirements.txt
```

#### Запись токена Telegram
```bush
echo TELEGRAM_BOT_TOKEN=ваш токен > .env
```

#### Запись токена VK
```bush
echo VK_TOKEN=ваш токен >> .env
```

#### Запись токена VK
```bush
echo VK_TOKEN=ваш токен >> .env
```

#### Запись TG_CHAT_ID
```bush
echo TG_CHAT_ID=ваш TG_CHAT_ID >> .env
```
Узнать CHAT_ID можно [@userinfobot](https://telegram.me/userinfobot).

#### Запись пути до файла с ключами от Google
```bush
echo GOOGLE_APPLICATION_CREDENTIALS=путь до файла с ключами от Google >> .env
```

Получить [ключи](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk).

#### Запись PROJECT_ID при создании проекта
```bush
echo PROJECT_ID=ваш PROJECT_ID >> .env
```

## Запуск

### Тренеровка ботов

Из директории с проектом выполните команду.
```bush
python3 create_intent.py путь до json файла с фразами
```
### Запуск ботов
Из директории с проектом выполните команды.
```bush
python3 tg_bot.py Бот в TG
python3 vk_bot.py Бот в VK
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
