from django.urls import path
from information import views

"""
Define path for HTML pages
"""

urlpatterns = [
    path("", views.home, name = "home"),
    path("get_book_by_id", views.get_book_by_id, name = "get_book_by_id"),
    path("book", views.get_book, name = "get_book"),
    path("place_book", views.place_book, name = "place_book"),
    path("sign_up", views.sign_up, name = "sign_up"),
    path("sign_in", views.sign_in, name = "sign_in"),
]