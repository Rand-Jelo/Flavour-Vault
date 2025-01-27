from django.urls import path
from .views import recipe_list, recipe_detail, signup_page, login_page, home_page

from .auth_views import signup, login

urlpatterns = [
    # Frontend Pages
    path('', home_page, name='home_page'),
    path('signup/', signup_page, name='signup_page'),
    path('login/', login_page, name='login_page'),

    # API Endpoints (Authentication)
    path('api/auth/signup/', signup, name='signup'),
    path('api/auth/login/', login, name='login'),

    # API Endpoints (Recipes)
    path('api/recipes/', recipe_list, name='recipe_list'),
    path('api/recipes/<int:id>/', recipe_detail, name='recipe_detail'),
]
