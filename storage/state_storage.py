"""
Хранилище состояний пользователей.

Используется для реализации конечного автомата
(FSM) и хранения промежуточных данных
между сообщениями пользователя.
"""

from states.subscription_states import (
    UserState
)


class StateStorage:
    """
    Хранилище состояний пользователей.

    Для каждого пользователя хранится:
    - текущее состояние;
    - временные данные.
    """

    def __init__(self):
        """
        Инициализация хранилища.
        """

        # Состояния пользователей
        self.states = {}

        # Временные данные пользователей
        self.temp_data = {}

    def set_state(
        self,
        user_id: int,
        state: UserState
    ) -> None:
        """
        Установить состояние пользователя.

        Args:
            user_id: ID пользователя.
            state: новое состояние.
        """

        self.states[user_id] = state

    def get_state(
        self,
        user_id: int
    ) -> UserState:
        """
        Получить текущее состояние пользователя.

        Args:
            user_id: ID пользователя.

        Returns:
            Текущее состояние пользователя.
        """

        return self.states.get(
            user_id,
            UserState.DEFAULT
        )

    def clear_state(
        self,
        user_id: int
    ) -> None:
        """
        Сбросить состояние пользователя.

        Также удаляет временные данные.

        Args:
            user_id: ID пользователя.
        """

        self.states[user_id] = (
            UserState.DEFAULT
        )

        if user_id in self.temp_data:
            del self.temp_data[user_id]

