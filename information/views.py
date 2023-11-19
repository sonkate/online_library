from django.shortcuts import render
from .connect import users_collection, books_collection
from bson.objectid import ObjectId
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
# Home page
def home(request):
    # users_collection.insert_one(
    #     {
    #         "name": "son",
    #         "email": "son@gmail.com",
    #         "lib_code": "JEMSOW",
    #         "pwd": "son123",
    #         "phone_num": "091234233123",
    #         "avatar": "",
    #     }
    # )

    # books_collection.insert_one(
    #     {
    #         "pub_date": "12/01/2002",
    #         "publisher": "NXB TPHCM",
    #         "desc": "This is book desc",
    #         "total_page": 200,
    #         "rating": 5.6,
    #         "genre": "science",
    #         "author": "John Thomas",
    #         "name": "Environment and Human",
    #         "total_quantity": 10,
    #         "available": 7,
    #     }
    # )
    # count = books_collection.count_documents({})
    # print(count)
    print(request)
    return render(request, "index.html")

def getBook(request):
    book = books_collection.find_one({'_id': ObjectId('6554763758dd11208593bc60')})
    book['_id'] = str(book['_id'])
    print(book)
    return JsonResponse(book)