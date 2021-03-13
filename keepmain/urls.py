from django.urls import path
from . import views


urlpatterns = [
    #FUNCTIONS
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('add_new_item/', views.add_new_item, name="add_new_item"),
    path('change_avatar/', views.change_avatar, name="change_avatar"),
    path('lend/', views.lend, name="lend"),
    path('borrow/', views.borrow, name="borrow"),

    #OTHER VIEWS
    path('u/<str:user>/', views.profile, name="profile"),
    path('search/', views.search, name="search"),

    #API
    path('agree_or_reject_trans/<int:id>', views.agree_or_reject_trans, name="agree_or_reject_trans"),
    path('agree_or_reject_ret/<int:id>', views.agree_or_reject_ret, name="agree_or_reject_ret"),
    path('return_borrowed/<int:id>', views.return_borrowed, name="return_borrowed"),
    path('api/profile/<str:user>', views.api_profile, name="api_profile"),
    path('api/api_borrow_requests/', views.api_borrow_requests, name="api_notif"),
    path('api/api_return_requests/', views.api_return_requests, name="api_notif_ret"),
    path('api/api_for_each_object/<int:id>', views.api_for_each_object, name="api_for_each_object")
]
