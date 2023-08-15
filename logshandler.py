import logging

import telegram


class TGLogsHandler(logging.Handler):
    def __init__(self, tg_bot_token: str, chat_id: int or str):
        super().__init__()
        self.bot = telegram.Bot(tg_bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.chat_id, log_entry)
