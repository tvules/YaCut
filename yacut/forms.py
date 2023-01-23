from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import Field, StringField
from wtforms.validators import (
    URL,
    DataRequired,
    Length,
    Regexp,
    ValidationError,
)

from yacut import constants as const
from yacut.models import URLMap


class URLMapForm(FlaskForm):
    """The form of the URLMap model."""

    original_link = StringField(
        "Адрес URL",
        description="https://example.com",
        validators=(
            DataRequired(message="Обязательное поле."),
            URL(message="Некорректный адрес URL."),
        ),
    )
    custom_id = StringField(
        "Идентификатор ссылки",
        description="Идентификатор ссылки",
        validators=(
            Length(
                max=16,
                message="Длина поля не должна превышать 16 символов.",
            ),
            Regexp(
                const.CUSTOM_ID_REGEX,
                message=(
                    "Идентификатор может состоять только "
                    "из латинских букв и цифр."
                ),
            ),
        ),
    )
    submit = SubmitField("Сократить")

    def validate_custom_id(self, field: Field) -> None:
        if field.data and not URLMap.is_free_short_id(field.data):
            raise ValidationError(f"Имя {field.data} уже занято!")
