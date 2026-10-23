from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy, ngettext

ROLES = {
    "admin": gettext_lazy("Admin"),
    "member": gettext_lazy("Member"),
}

TEAM_NAME = "Northwind"
SEATS_ON_PLAN = 10
SIGNED_IN_USER = "Maja Lindqvist"
MEMBERS = [
    {"name": "Maja Lindqvist", "email": "maja@example.com", "role": "admin"},
    {"name": "Tomasz Nowak", "email": "tomasz@example.com", "role": "member"},
    {"name": "Layla Haddad", "email": "layla@example.com", "role": "member"},
]

PENDING_INVITES = ["alva@example.com", "jonas@example.com"]


def seats_left_template(seats_left):
    return ngettext(
        "%(count)s seat left on your plan.",
        "%(count)s seats left on your plan.",
        seats_left,
    )


def seats_left_message(seats_left):
    return seats_left_template(seats_left) % {"count": seats_left}


def team_settings(request):
    members = [{**member, "role_label": ROLES[member["role"]]} for member in MEMBERS]
    context = {
        "team_name": TEAM_NAME,
        "signed_in_as": _("Signed in as %(name)s") % {"name": SIGNED_IN_USER},
        "seats_left": seats_left_message(SEATS_ON_PLAN - len(MEMBERS)),
        "members": members,
        "pending_invites": PENDING_INVITES,
        "roles": ROLES.items(),
    }
    return render(request, "teams/team_settings.html", context)
