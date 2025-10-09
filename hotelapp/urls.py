from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('view_reservations/',views.view_reservations,name='view_reservations'),
    path('checkout/<int:reservation_id>/', views.checkout_reservation, name='checkout_reservation'),

    path('roomcategory_list/',views.roomcategory_list,name='roomcategory_list'),
    path('roomcategory_add/',views.roomcategory_add,name='roomcategory_add'),
    path("roomcategory_edit/<int:id>/", views.roomcategory_edit, name="roomcategory_edit"),
    path("room_category_delete/<int:id>/", views.roomcategory_delete, name="roomcategory_delete"),

    path('room_list/',views.room_list,name='room_list'),
    path('room_add/',views.room_add,name='room_add'),
    path("room_edit/<int:id>/", views.room_edit, name="room_edit"),
    path("room_delete/<int:id>/", views.room_delete, name="room_delete"),

    path('specialrate_list/',views.specialrate_list,name='specialrate_list'),
    path('specialrate_add/',views.specialrate_add,name='specialrate_add'),
    path("specialrate_edit/<int:id>/", views.specialrate_edit, name="specialrate_edit"),
    path("specialrate_delete/<int:id>/", views.specialrate_delete, name="specialrate_delete"),

    path('check_availability/',views.check_availability,name='check_availability'),
    path('reservation/<int:id>/',views.reservation,name='reservation'),
    path('reservation-success/<int:reservation_id>/', views.reservation_success, name='reservation_success'),

    path('view_gallery/',views.gallery,name='view_gallery'),
    
   

]


 