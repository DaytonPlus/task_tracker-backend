from django.urls import path
from.views import CheckToken, Login, Register, Logout, ProfileView

urlpatterns = [
    path('check/', CheckToken),
    path('login/', Login),
    path('register/', Register),
    path('profile/', ProfileView.as_view()),
    path('logout/', Logout),
]
