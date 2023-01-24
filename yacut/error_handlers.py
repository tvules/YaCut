from typing import Tuple

from flask import Response, jsonify, render_template
from werkzeug.exceptions import HTTPException

from yacut import app, db
from yacut.exceptions import APIError


@app.errorhandler(APIError)
def invalid_api_usage(error: APIError) -> Tuple[Response, int]:
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error: HTTPException) -> Tuple[str, int]:
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_error(error: HTTPException) -> Tuple[str, int]:
    db.session.rollback()
    return render_template("errors/500.html"), 500
