# create urls for the profiles app
from django.urls import path
from profiles.views import MyJobSeekerProfileView

urlpatterns = [
    path("api/me/profile/", MyJobSeekerProfileView.as_view(), name="my-profile"),
]
