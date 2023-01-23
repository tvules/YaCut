import re
from http import HTTPStatus

from flask import Response, jsonify, request, url_for

from yacut import app
from yacut import constants as const
from yacut.exceptions import APIRequestError
from yacut.models import URLMap
from yacut.utils import required_fields, save

CUSTOM_ID_VALIDATORS = {
    lambda value: (len(value) > const.CUSTOM_ID_LENGTH): (
        const.INVALID_CUSTOM_ID
    ),
    lambda value: (re.match(const.CUSTOM_ID_REGEX, value) is None): (
        const.INVALID_CUSTOM_ID
    ),
    lambda value: not URLMap.is_free_short_id(value): (
        const.NOT_UNIQUE_CUSTOM_ID
    ),
}


@app.route("/api/id/", methods=("POST",))
@required_fields(("url",))
def create_short_url() -> tuple[Response, int]:
    data = request.get_json()

    custom_id = data.get("custom_id")
    if custom_id is not None:
        for func, message in CUSTOM_ID_VALIDATORS.items():
            if func(custom_id):
                raise APIRequestError(message.format(custom_id=custom_id))
    else:
        data["custom_id"] = URLMap.get_unique_short_id()

    urlmap = URLMap(original=data.get("url"), short=data.get("custom_id"))
    save(urlmap)

    response = {
        "url": urlmap.original,
        "short_link": url_for(
            "mapping_redirect",
            short_id=urlmap.short,
            _external=True,
        ),
    }
    return jsonify(response), HTTPStatus.CREATED


@app.route("/api/id/<string:short_id>/")
def get_short_url(short_id: str) -> tuple[Response, int]:
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise APIRequestError(const.SHORT_ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({"url": urlmap.original}), HTTPStatus.OK
