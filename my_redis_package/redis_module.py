import redis
from time import sleep
from abc import ABC, abstractmethod
import os
from datetime import datetime
import json



class LogFetcher(ABC):
    #интерфейс получения логов
    @abstractmethod
    def fetch_logs(self, count: int):
        pass


class Connector:
    #общий класс подключения с экспоненциальнй задержкой
    def connect_retry(self, func_connect, max_attempts=None, initial_wait=1, max_wait=60):
        """
        Подключение к БД ClickHouse с использованием метода экспоненциальной задержки и 
        последующей повторной попыткой подключения.

        max_attempts: Задается количество попыток подключения
        initial_wait: Начальная задержка, которая увеличивается экспоненцивльно
        max_wait: Максимальное время ожидания между попытками подкючения
        """
        attempt = 0
        while True:
            try:
                client = func_connect()
                return client
            except Exception as e:
                attempt +=1
                if max_attempts and attempt >= max_attempts:
                    raise e
                
                wait_time = min(initial_wait * (2 ** (attempt - 1)), max_wait)
                sleep(wait_time)


class RedisConnector(Connector, LogFetcher):
    #класс коннектор для redis
    def __init__(self):
        self.host = os.getenv('REDIS_HOST')
        self.port = int(os.getenv('REDIS_PORT'))
        self.client = self.connect_retry(self.connect_redis)


class RedisLogFetcher(RedisConnector):
    #подкласс для извлечения данных из redis 
    def fetch_logs(self, count=100):
        logs = []
        for _ in range(count):
            try:
                log_entry = self.client.lpop('log_queue')
                if log_entry:
                    log = json.loads(log_entry)
                    log['timestamp'] = datetime.fromtimestamp(log['timestamp']) + timedelta(hours=4)
                    logs.append(list(log.values()))
            except Exception as err:
                self.client = self.connect()
        return logs
