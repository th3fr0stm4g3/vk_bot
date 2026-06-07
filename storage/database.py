"""
Модуль работы с JSON-хранилищем.

Отвечает за:
- загрузку данных из файла;
- сохранение данных в файл;
- создание файла при первом запуске.
"""

import json
from pathlib import Path


class JsonDatabase:
    """
    Класс для работы с JSON-файлом.

    Используется как простая база данных
    для хранения подписок.
    """

    def __init__(
        self,
        file_path: str
    ):
        """
        Инициализация базы данных.

        Args:
            file_path: путь к JSON-файлу.
        """

        self.file_path = Path(file_path)

        # Создание файла при его отсутствии
        if not self.file_path.exists():

            self.file_path.write_text(
                '{"subscriptions": []}',
                encoding="utf-8"
            )

    def load(self) -> dict:
        """
        Загрузить данные из JSON-файла.

        Returns:
            Словарь с данными.
        """

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def save(
        self,
        data: dict
    ) -> None:
        """
        Сохранить данные в JSON-файл.

        Args:
            data: данные для сохранения.
        """

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )
