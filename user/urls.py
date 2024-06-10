from django.urls import path
from.views import CheckToken, Login, Register, Logout, ProfilesView, ProfileView

urlpatterns = [
    path('check/', CheckToken),
    path('login/', Login),
    path('register/', Register),
    path('profile/', ProfilesView.as_view()),
    path('profile/<int:id>/', ProfileView.as_view()),
    path('logout/', Logout),
]
