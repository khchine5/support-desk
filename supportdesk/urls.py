from django.urls import path
from . import views

urlpatterns = [
    path("requests/", views.RequestsView.as_view(), name="requests-list"),
    path("request/new", views.CreateRequest.as_view(), name="request-create"),
    path(
        "request/<int:pk>/complete/",
        views.mark_request_compelete,
        name="request-complete",
    ),
    path(
        "request/<int:pk>/reassign/",
        views.RequestUpdateView.as_view(),
        name="request-reassign",
    ),
    path("request/<int:pk>/", views.RequestDetailView.as_view(), name="request-detail"),
    path(
        "placeholder/", views.PlaceholderHome.as_view(), name="supportdesk_placeholder"
    ),
]
