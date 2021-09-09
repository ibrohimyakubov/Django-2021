from django.urls import path
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserList

router = routers.SimpleRouter()
router.register('register', UserList)

urlpatterns = router.urls + [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('my-account/', views.my_account, name='my-account'),

    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>/', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),
    path('remove-tag/', views.removeTag)
]
