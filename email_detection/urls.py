from django.urls import path
from . views import classify_email
app_name= "email_detection"

urlpatterns = [
    path('', classify_email, name="classify_email"),
]
