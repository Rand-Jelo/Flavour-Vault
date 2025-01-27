from django.urls import path
from .views import recipe_list, recipe_detail, signup_page, login_page

from .auth_views import signup, login

urlpatterns = [
    # Frontend Pages
    path('signup/', signup_page, name='signup_page'),
    path('login/', login_page, name='login_page'),

    # API Endpoints
    path('api/auth/signup/', signup, name='signup'),
    path('api/auth/login/', login, name='login'),

]