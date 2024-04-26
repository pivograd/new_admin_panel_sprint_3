import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, max_retries=10, exceptions: tuple = None):
    """
    Декоратор для повторного выполнения функции через некоторое время, если возникла ошибка, с использованием экспоненциального роста.

    :param start_sleep_time: Начальное время ожидания (в секундах).
    :param factor: Множитель для увеличения времени ожидания.
    :param border_sleep_time: Максимальное время ожидания (в секундах).
    :param max_retries: Максимальное количество повторных попыток (по умолчанию 10).
    :param exceptions: Кортеж исключений, которые перехватываются (по умолчанию None).
    :return: Декоратор.
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions if exceptions else Exception as exc:
                    retries += 1
                    logger.error(f"Ошибка: {exc}. Попытка {retries}")

                    sleep_time = sleep_time * factor
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time

                    time.sleep(sleep_time)

        return inner

    return func_wrapper
