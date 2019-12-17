from apps.invitations import views
from django.urls import path, include

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('invitations/', views.InvitationView.as_view()),
    path('invitations/<id>/', views.InvitationDetail.as_view())
]
