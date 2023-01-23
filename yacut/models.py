import random
import string
from datetime import datetime

from yacut import constants as const
from yacut import db


class URLMap(db.Model):
    """URL mapping model."""

    original = db.Column(db.String, nullable=False)
    short = db.Column(
        db.String(const.CUSTOM_ID_LENGTH),
        nullable=False,
        unique=True,
        index=True,
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_short_id(length: int) -> str:
        symbols = string.ascii_letters + string.digits
        return "".join((random.choice(symbols) for _ in range(length)))

    @classmethod
    def is_free_short_id(cls, short_id: str) -> bool:
        return cls.query.filter_by(short=short_id).first() is None

    @classmethod
    def get_unique_short_id(cls, length: int = const.SHORT_ID_LENGTH) -> str:
        while True:
            short_id = cls.generate_short_id(length)
            if cls.is_free_short_id(short_id):
                break
        return short_id
