from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Fridge Savior API",
        default_version="v1",
        description="Fridge Savior API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="Min", email="minnimida@gmail.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('users/', include('dj_rest_auth.urls')),
    # path('users/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('items/', include('items.urls')),
]


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('sentry-debug/', trigger_error),
    ]