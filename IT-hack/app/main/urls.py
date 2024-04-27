from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page),
    path('profile/', views.profile),
    path('profile_edit/', views.profile_edit),
    path('add_place/', views.add_place),
    path('place_more/', views.place_more),
    path('delete_place/', views.delete_place),
    path('edit_place/', views.edit_place),
    path('add_place_room', views.add_place_room),
    path('edit_place_room/', views.edit_place_room),
    path('delete_place_room/', views.delete_place_room),
    path('buy/', views.buy),
    path('buygroup/', views.buygroup),
    # path('buy_remove/', views.buy_remove),
    path('send_faq/', views.send_faq),
    path('read_faqs/', views.read_faq_messages),
    path('delete_faq/', views.delete_faq),
    path('place_members', views.place_members),
]
