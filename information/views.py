from django.shortcuts import render
from .connect import users_collection, books_collection
from django.http import JsonResponse
import json
# Create your views here.
# Home page
def home(request):
    # users_collection.insert_one({'name': 'son', 'email': 'son@gmail.com'})
    count = books_collection.count_documents({})
    print(count)
    response = {'data': {'count': count}, 'message': 'successful'}
    return JsonResponse(response, status=200)

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
