from django.urls import include, path
from rest_auth.urls import LoginView, LogoutView

urlpatterns = [
    # path('registration/', include('rest_auth.registration.urls')),

    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
