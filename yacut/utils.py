from functools import wraps
from typing import Callable, Iterable

from flask import request
from flask_sqlalchemy.model import Model

from yacut import constants as const
from yacut import db
from yacut.exceptions import APIRequestError


def save(obj: Model) -> None:
    db.session.add(obj)
    db.session.commit()


def required_fields(
    fields: Iterable,
    message=const.FIELD_IS_REQUIRED,
) -> Callable:
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                raise APIRequestError(const.EMPTY_REQUEST_BODY)

            for field in fields:
                if field not in data or field is None:
                    raise APIRequestError(message.format(field=field))

            return func(*args, **kwargs)

        return wrapper

    return decorator
