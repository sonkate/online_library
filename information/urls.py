from django.urls import path
from information import views

"""
Define path for HTML pages
"""

urlpatterns = [
    path("", views.home, name = "home"),
    path("getBook/", views.getBook, name = "getBook"),
    path("book", views.get_book, name = "get_book"),

]