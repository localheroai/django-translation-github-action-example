from django.conf.urls.i18n import i18n_patterns
from django.urls import path

from teams import views

urlpatterns = i18n_patterns(
    path("", views.team_settings, name="team_settings"),
    prefix_default_language=False,
)
