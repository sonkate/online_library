from django.shortcuts import render
from .connect import users_collection, books_collection

# Create your views here.
# Home page
def home(request):
    # users_collection.insert_one({'name': 'son', 'email': 'son@gmail.com'})
    count = books_collection.count_documents({})
    print(count)
    return render(request,'index.html')