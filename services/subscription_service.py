"""
Сервисный слой приложения.

Файл содержит бизнес-логику работы с подписками:
- создание;
- получение списка;
- поиск по ID;
- удаление;
- изменение стоимости;
- оплата подписки;
- подсчёт расходов.
"""

from datetime import date

from storage.database import JsonDatabase


class SubscriptionService:
    """
    Сервис для управления подписками.

    Выполняет все операции над подписками
    и взаимодействует с JSON-хранилищем.
    """

    def __init__(
        self,
        database: JsonDatabase
    ):
        """
        Инициализация сервиса.

        Args:
            database: объект работы с БД.
        """

        self.database = database

    def create_subscription(
        self,
        name: str,
        price: int
    ) -> int:
        """
        Создать новую подписку.

        Args:
            name: название подписки.
            price: стоимость подписки.

        Returns:
            ID созданной подписки.
        """

        data = self.database.load()

        # Генерация нового ID
        new_id = (
            max(
                [
                    item["id"]
                    for item in data["subscriptions"]
                ],
                default=0
            ) + 1
        )

        data["subscriptions"].append(
            {
                "id": new_id,
                "name": name,
                "price": price,
                "paid": False,
                "payment_date": None
            }
        )

        self.database.save(data)

        return new_id

    def get_all_subscriptions(
        self
    ) -> list:
        """
        Получить список всех подписок.

        Returns:
            Список подписок.
        """

        return self.database.load()[
            "subscriptions"
        ]

    def get_subscription_by_id(
        self,
        subscription_id: int
    ) -> dict | None:
        """
        Найти подписку по ID.

        Args:
            subscription_id: идентификатор подписки.

        Returns:
            Словарь подписки или None.
        """

        subscriptions = (
            self.get_all_subscriptions()
        )

        for subscription in subscriptions:

            if (
                subscription["id"]
                == subscription_id
            ):
                return subscription

        return None

    def delete_subscription(
        self,
        subscription_id: int
    ) -> bool:
        """
        Удалить подписку по ID.

        Args:
            subscription_id: идентификатор подписки.

        Returns:
            True если удаление выполнено,
            иначе False.
        """

        data = self.database.load()

        old_count = len(
            data["subscriptions"]
        )

        data["subscriptions"] = [
            item
            for item in data["subscriptions"]
            if item["id"] != subscription_id
        ]

        self.database.save(data)

        return (
            len(data["subscriptions"])
            < old_count
        )

    def pay_subscription(
        self,
        subscription_id: int
    ) -> bool:
        """
        Отметить подписку как оплаченную.

        Args:
            subscription_id: идентификатор подписки.

        Returns:
            True при успешной оплате.
        """

        data = self.database.load()

        for subscription in data[
            "subscriptions"
        ]:

            if (
                subscription["id"]
                == subscription_id
            ):

                subscription["paid"] = True

                subscription[
                    "payment_date"
                ] = str(date.today())

                self.database.save(data)

                return True

        return False

    def update_price(
        self,
        subscription_id: int,
        new_price: int
    ) -> bool:
        """
        Изменить стоимость подписки.

        Args:
            subscription_id: ID подписки.
            new_price: новая стоимость.

        Returns:
            True если изменение выполнено.
        """

        data = self.database.load()

        for subscription in data[
            "subscriptions"
        ]:

            if (
                subscription["id"]
                == subscription_id
            ):

                subscription[
                    "price"
                ] = new_price

                self.database.save(data)

                return True

        return False

    def get_unpaid_subscriptions(
        self
    ) -> list:
        """
        Получить список неоплаченных подписок.

        Returns:
            Список неоплаченных подписок.
        """

        return [
            item
            for item in self.get_all_subscriptions()
            if not item["paid"]
        ]

    def get_total_cost(
        self
    ) -> int:
        """
        Подсчитать суммарную стоимость подписок.

        Returns:
            Общая сумма расходов.
        """

        return sum(
            item["price"]
            for item in self.get_all_subscriptions()
        )
