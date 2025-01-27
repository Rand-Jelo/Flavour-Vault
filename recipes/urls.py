from django.urls import path
from .views import recipe_list, recipe_detail
from .auth_views import signup, login

urlpatterns = [
    path('recipes/', recipe_list, name='recipe_list'),
    path('recipes/<int:id>/', recipe_detail, name='recipe_detail'),
    path('auth/signup/', signup, name='signup'),
    path('auth/login/', login, name='login'),
]