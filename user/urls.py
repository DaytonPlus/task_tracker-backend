from django.urls import path
from.views import CheckToken, Login, Register, Logout, ProfileView, ProfileMe

urlpatterns = [
    path('check/', CheckToken),
    path('login/', Login),
    path('register/', Register),
    path('profile/me/', ProfileMe),
    path('profile/<int:id>/', ProfileView.as_view()),
    path('logout/', Logout),
]
