from django.shortcuts import render
from .connect import users_collection, books_collection, borrowed_books
from bson.objectid import ObjectId
from datetime import datetime
from django.http import HttpResponse
from django.http import JsonResponse
import json


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
    response = {"data": {"count": count}, "message": "successful"}
    return JsonResponse(response, status=200)


def get_book_by_id(request):
    response = {}
    print("getting")
    if request.method == "GET":
        if request.GET.get("id"):
            print("id", type(request.GET.get("id")))
            book = books_collection.find_one({"_id": ObjectId(request.GET.get("id"))})
            book["_id"] = str(book["_id"])
            response = {"data": book, "message": "successful"}
    return JsonResponse(response, status=200)


def place_book(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        data = json.loads(body)

        userId = data.get('userId')
        bookId = data.get('bookId')
        due_date = data.get('due_date')
        data_row = {
            "userId": userId,
            "bookId": bookId,
            "due_date": due_date,
            "start_date": datetime.now().isoformat(),
            "status": "borrowing",
        }
        book = books_collection.find_one({"_id": ObjectId(bookId)}) if ObjectId.is_valid(bookId) else None 
        user = users_collection.find_one({"_id": ObjectId(userId)}) if ObjectId.is_valid(userId) else None

        if user and book:
            result = borrowed_books.insert_one(data_row)
        
            if result.inserted_id:
                return JsonResponse({'message': 'Book placed successfully'})

        return JsonResponse({'error': 'Failed to insert book placement'}, status=500)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_book(request):
    if request.method == "GET":
        data = []
        if request.GET.get("name"):
            searched = request.GET.get("name")
            data = books_collection.find({"name": {"$regex": searched}}, {"_id": 0})
        elif request.GET.get("genre"):
            searched = request.GET.get("genre")
            data = books_collection.find({"genre": {"$regex": searched}}, {"_id": 0})
        print(dataa)

        data_res = []
        for ele in data:
            data_res += [ele]
        response = {"data": data_res, "message": "successful"}
        return JsonResponse(response, status=200)

def sign_up(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        data = json.loads(body)

        name = data.get("name")
        email = data.get("username")
        lib_code = data.get("code")
        pwd = data.get("password")
        phone_num = data.get("phone")
        avatar = data.get("avatar")

        new_user = {
            "name": name,
            "email": email,
            "lib_code": lib_code,
            "pwd": pwd,
            "phone_num": phone_num if phone_num else "",
            "avatar": avatar if avatar else "",
        }

        if name and email and lib_code and pwd:
            result = users_collection.insert_one(new_user)

            if result.inserted_id:
                return JsonResponse({'message': 'Created account successfully'})

        return JsonResponse({'error': 'Can not create new account'}, status=500)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def sign_in(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        data = json.loads(body)

        print(data)

        login = users_collection.find_one({"email": data.get("username"), "pwd": data.get("password")})

        if login:
            return JsonResponse({"user_id": login.get("_id"), "name": login.get("name")})

        return JsonResponse({"error": "Invalid username or password"}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
