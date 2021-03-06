import copy
from flask import json, Response
from flask_login import current_user, login_required

from app import db
from app.admin import bp
from app.admin.email import send_update_email
from app.models import User


@bp.route("/send_update_email", methods=["GET"])
@login_required
def update_email():
    if not current_user.is_admin:
        r = json.dumps({"success": False})
        return Response(r, status=403, mimetype="application/json")

    users = User.query.filter_by(unsubscribe=False).filter_by(deleted=False).all()

    sent_list = []

    for u in users:
        send_update_email(u)
        sent_list.append(u.email)

    db.session.close()
    r = json.dumps({"success": True, "sent-to": json.dumps(sent_list)})
    return Response(r, status=200, mimetype="application/json")
