from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.dashboard.views import index


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("login/", 
        auth_views.LoginView.as_view(template_name="login.html"), 
        name="login"
    ),
    path("logout/",
        auth_views.LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
    path("visitantes/", include("visitantes.urls", namespace="visitantes")),
    path("usuarios/", include("usuarios.urls", namespace="usuarios")),
    path("unidades/", include("unidades.urls", namespace="unidades")),
    path("proprietarios/", include("proprietarios.urls", namespace="proprietarios")),
    path("porteiros/", include("porteiros.urls", namespace="porteiros")),
]
