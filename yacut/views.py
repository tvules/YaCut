from flask import Response, redirect, render_template, url_for

from yacut import app
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.utils import save


@app.route("/", methods=("GET", "POST"))
def index() -> str:
    form = URLMapForm()

    if not form.validate_on_submit():
        return render_template("index.html", form=form)

    if not form.custom_id.data:
        form.custom_id.data = URLMap.get_unique_short_id()

    urlmap = URLMap(
        original=form.original_link.data,
        short=form.custom_id.data,
    )
    save(urlmap)

    form.custom_id.data = None
    return render_template(
        "index.html",
        form=form,
        short_link=url_for(
            "mapping_redirect",
            short_id=urlmap.short,
            _external=True,
        ),
    )


@app.route("/<string:short_id>", strict_slashes=False)
def mapping_redirect(short_id: str) -> Response:
    return redirect(
        URLMap.query.filter_by(short=short_id).first_or_404().original,
    )
