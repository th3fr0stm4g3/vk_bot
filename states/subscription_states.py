from enum import Enum


class UserState(Enum):
    DEFAULT = "default"

    ADD_NAME = "add_name"
    ADD_PRICE = "add_price"

    DELETE_SELECT = "delete_select"

    PAY_SELECT = "pay_select"

    UPDATE_SELECT = "update_select"
    UPDATE_PRICE = "update_price"