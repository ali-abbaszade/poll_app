from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('questions/', views.question_list, name='question-list'),
    path('questions/<int:pk>/', views.question_detail, name='question-detail'),
    path('questions/<int:pk>/vote/', views.question_vote, name='question-vote'),
]
