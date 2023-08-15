# Support Bot

Боты VK/Telegram для автоматизированного ответа пользователям на их вопросы. Диалоги реализованы с помощью DialogFlow от Google.

Демки бота:
 - [Telegram](https://t.me/zhukov_service_bot)
 - [ВКонтакте](https://vk.com/im?sel=-221535503)

![gif](https://dvmn.org/media/filer_public/7a/08/7a087983-bddd-40a3-b927-a43fb0d2f906/demo_tg_bot.gif)

Если бот получит непонятное сообщение, в Телеграме он так и скажет, что не понял собеседника. ВКонтакте бот не будет отвечать на сообщения, которые не понял, это удобно для того, чтобы на такое сообщение мог ответить оператор и оно не потерялось.

Ниже представлена инструкция, как развернуть проект и запустить ботов на локальной машине.

## Установка зависимостей
Первым делом, скачайте код:
``` 
git clone https://github.com/pas-zhukov/support-bot.git
```
Для работы скрипта понадобятся библиотеки, перечисленные в `reqirements.txt`.
Устанавливаем их командой:
```
pip install -r requirements.txt
```

## Подготовка бэкенда для ботов

Бот генерирует ответы с использованием сервиса [DialogFlow](https://dialogflow.cloud.google.com). Чтобы настроить его под себя, необходимо сделать следующее:

1. Создать проект DialogFlow. [Как создать](https://cloud.google.com/dialogflow/docs/quick/setup).
2. Создать "агента", прикрепить его к ранее созданному проекту по id. [Как создать агента](https://cloud.google.com/dialogflow/es/docs/quick/build-agent). Не забудьте выбрать русский язык.
3. Натренировать "агента": создать новые **intent** по выбранной теме, сконфигурировать для него фразы, ожидаемые от пользователя (по этой теме) и создать варианты ответа бота на эти фразы. Т.к. в сердце DialogFlow лежит нейросеть, улавливаться будут не только четко совпадающие фразы, а ещё и фразы, совпадающие по смыслу.
4. [Включить API](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) DialogFlow.
5. Установить консольную утилиту [Google Cloud CLI](https://cloud.google.com/sdk/docs/install).
6. Запустить GCloud CLI и последовательно ввести следующие команды (это авторизует Вас для текущего компьютера и установит рабочий проект):

```shell
gcloud auth login
```

```shell
gcloud config set project <id-вашего-проекта-dialogflow>
```

```shell
gcloud auth application-default login
```
Последняя команда также создаст файл `credentials.json` с данными для авторизации, сохраните путь к нему, это может пригодиться в дальнейшем.

Если вам понадобится получить API-ключ самого DialogFlow, воспользуйтесь функцией [`create_api_key`](https://github.com/pas-zhukov/support-bot/blob/dbb283ca6d6d9ee5c12c3ec8eb411094c327f50c/dialogflow.py#L13). После авторизации по инструкции выше использование ключа не понадобится.

## Создание и подготовка ботов

- Для создания Телеграм-бота нужно написать [отцу ботов](https://github.com/pas-zhukov/watching-storage) и сохранить полученный токен. Инструкция по созданию бота и получению токена: [ссылка](https://botcreators.ru/blog/botfather-instrukciya/).

- Бот ВКонтакте работает от имени группы. Нужно создать группу (либо использовать имеющуюся под управлением), в настройках включить сообщения сообщества и разрешить боту на них отвечать. Там же, в настройках, необходимо сгенерировать API-ключ и сохранить его. [Как получить токен ВК-бота](https://forum.bottap.ru/t/kak-poluchit-token-vk/33).

## Переменные окружения

Для работы ботов необходимо в корне с программой создать файл `.env` и заполнить его следующим содержимым:
``` 
TG_BOT_TOKEN=<API-токен Вашего Телеграм-бота>
VK_BOT_TOKEN=<API-токен бота ВКонтакте>
DIALOGFLOW_PROJECT_ID=<ID проекта DialogFlow>
```

Бот также поддерживает логирование важных ошибок в админский телеграм-канал (или просто Вам в личку). Чтобы это заработало, нужно задать следующие переменные в `.env`:
```
ADMIN_TG_BOT_TOKEN=<Токен админского Телеграм-бота>
ADMIN_CHAT_ID=<ID чата, в который будут отправляться логи бота>
```

## Запуск ботов

Телеграм-бот запускается следующей командой:

```shell
python tg_bot.py
```

Бот ВКонтакте запускается следующей командой:

```shell
python vk_bot.py
```

_Чтобы приостановить работу бота, используйте сочетание клавиш Ctrl+C._

## Цель проекта

Код написан в учебно-развлекательных целях.