from django.shortcuts import render
from .connect import users_collection, books_collection, borrowed_books
from bson.objectid import ObjectId
from datetime import datetime
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import QueryDict
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
        print(data)

        data_res = []
        for ele in data:
            data_res += [ele]
        response = {"data": data_res, "message": "successful"}
        return JsonResponse(response, status=200)

def sign_up(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        data = json.loads(body)

        phone_num = data.get("phone_num")
        avatar = data.get("avatar")

        new_user = {
            "name": data.get("name"),
            "email": data.get("email"),
            "lib_code": data.get("lib_code"),
            "pwd": data.get("password"),
            "phone_num": phone_num if phone_num else "",
            "avatar": avatar if avatar else "",
        }

        if new_user.get("name") and new_user.get("email") and new_user.get("lib_code") and new_user.get("pwd"):
            invalid_email = users_collection.find_one({"email": new_user.get("email")})
            if invalid_email:
                return JsonResponse({"error": "Email has been used"}, status=409)
            
            result = users_collection.insert_one(new_user)

            if result.inserted_id:
                return JsonResponse({"message": "Created account successfully"})

        return JsonResponse({"error": "Failed to create new account"}, status=404)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)

def sign_in(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        data = json.loads(body)

        login = users_collection.find_one({"email": data.get("email"), "pwd": data.get("password")})

        if login:
            return JsonResponse({	
                "message": "Logged in successfully",
                "data": {"id": str(login.get("_id")), "name": login.get("name")}
            })

        return JsonResponse({"error": "Invalid username or password"}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def get_user_info(request, id):
    if request.method == "GET":     
        user = users_collection.find_one({"_id": ObjectId(id)})
        
        if user:
            return JsonResponse({
                "message": "User found",
                "data": {
                    "name": user.get("name"),
                    "email": user.get("email"),
                    "password": user.get("pwd"),
                    "lib_code": user.get("lib_code"),
                    "phone_num": user.get("phone_num"),
                    "avatar": user.get("avatar")
                }
            })
        return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def update_user_info(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        data = json.loads(body)

        name = data.get("name")
        email = data.get("email")
        pwd = data.get("password")
        lib_code = data.get("lib_code")

        user = users_collection.find_one({"_id": ObjectId(data.get("id"))})

        if user and name and email and pwd and lib_code:
            if email != user.get("email"):
                invalid_email = users_collection.find_one({"email": email})
                if invalid_email:
                    return JsonResponse({"error": "New email has been used"}, status=409)
				
            change = {"$set": data}
            result = users_collection.update_one(user, change)

            if result:
                return JsonResponse({"message": "Updated successfully"})
		
        return JsonResponse({"error": "Invalid required fields"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_borrow_history(request, id):
    if request.method == "GET":
        user = users_collection.find_one({"_id": ObjectId(id)})
        books = []

        if user:
            records = borrowed_books.find({"userId": id}, {"userId": 0}, limit=10)
            for record in records:
                books += [record]
                name = books_collection.find_one({"_id": ObjectId(str(record.get("bookId")))})
                books[-1]["_id"] = str(books[-1]["_id"])
                books[-1]["due_date"] = books[-1]["due_date"][0:10]
                books[-1]["start_date"] = books[-1]["start_date"][0:10]
                books[-1]["name"] = name.get("name")
            return JsonResponse({"message": "History found", "history": books})
        
        return JsonResponse({"error": "User not found"}, status=404)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)
