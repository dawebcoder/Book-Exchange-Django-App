from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('index', views.index, name='index'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('search/', views.search, name='search'),
    path('book_add/<int:book_id>', views.book_add, name='book_add'),
    path('shoppingcart', views.shopping_cart, name='shopping_cart'),
    path('fav/<int:book_id>', views.favorite_add, name='favorite_add'),
    path('favoritebooks', views.favorite_books, name='favorite_books'),
]
