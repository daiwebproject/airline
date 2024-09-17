from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
# nếu không có người dùng nào đã đăng nhập quay lại trang đăng nhập.
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    return render(request, "users/user.html")

def login_view(request):
    if request.method =="POST":
        #truy cập username pasword từ mẫu dữ liệu:
        username = request.POST["username"]
        password = request.POST["password"]

        #kiểm tra nếu usernae và password có đúng không, trả về  đối tượng người dùng nếu đúng
        user = authenticate(request, username=username,password=password)
        #nếu đối tượng user được trả về, hãy đăng nhập vào định tuyến đến trang chỉ mục
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        #nếu không, quay lại trang login với ngữ cảnh invalid
        else:
            return render(request, "users/login.html",{
                "message": "invalid Credentials"
                
            })
    return(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "logged out"
    })
# Create your views here.
