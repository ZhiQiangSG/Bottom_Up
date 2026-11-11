from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from bottom_up.assistant.api.views import ConversationViewSet
from bottom_up.assistant.api.views import FeedbackCreateView
from bottom_up.assistant.api.views import MemoryView
from bottom_up.assistant.api.views import PendingActionViewSet
from bottom_up.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("assistant/conversations", ConversationViewSet, basename="conversation")
router.register("assistant/pending-actions", PendingActionViewSet, basename="pending-action")


urlpatterns = [
    *router.urls,
    path("assistant/memory/", MemoryView.as_view(), name="assistant-memory"),
    path("assistant/feedback/", FeedbackCreateView.as_view(), name="assistant-feedback"),
]


app_name = "api"
