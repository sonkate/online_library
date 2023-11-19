from django.shortcuts import render
from .connect import users_collection, books_collection
from django.http import JsonResponse
import jsonfrom bson.objectid import ObjectId
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
    count = books_collection.count_documents({})
    print(count)
    response = {'data': {'count': count}, 'message': 'successful'}
    return JsonResponse(response, status=200)

def getBook(request):
    book = books_collection.find_one({'_id': ObjectId('6554763758dd11208593bc60')})
    book['_id'] = str(book['_id'])
    print(book)
    return JsonResponse(book)

def get_book(request):
    if request.method == 'GET':
        data = []
        if request.GET.get('name'):
            searched = request.GET.get('name')
            data = books_collection.find({'name': { "$regex": searched}}, {"_id": 0})
        elif request.GET.get('genre'):
            searched = request.GET.get('genre')
            data = books_collection.find({'genre': { "$regex": searched}}, {"_id": 0})

        data_res = []
        for ele in data:
            data_res += [ele]
        response =  {'data': data_res, 'message': 'successful'}
        return JsonResponse(response, status=200)
