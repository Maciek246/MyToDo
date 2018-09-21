from rest_framework.renderers import JSONRenderer

from rest_auth import views


class LoginView(views.LoginView):
    renderer_classes = (JSONRenderer,)


class LogoutView(views.LogoutView):
    renderer_classes = (JSONRenderer,)
