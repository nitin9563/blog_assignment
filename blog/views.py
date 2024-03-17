from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import bleach
from .models import BlogPost
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        name = request.POST.get("name")
        password = request.POST.get("password")
        c_password = request.POST.get("c_password")

        try:

            if password != c_password:
                messages.error(request, 'Password and confirm password did not match')

            else:
                try:
                
                    user = User.objects.create_user(username=email, password=password,first_name = name)
                    messages.success(request,"Signup succesfully")
                    if user:
                        login(request, user)
                        request.session['user_id'] = user.id

                        return redirect("/")

                except  Exception as e:
                    messages.error(request,e)

        except Exception as E:
            messages.error(request, E)
    
    return render(request,"signup.html")

def login_user(request):
    if request.method == 'POST':
    
        username = request.POST.get('email')
        password = request.POST.get('password')

        try :
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                request.session['user_id'] = user.id
                messages.success(request,"login succesfully")
                return redirect("/")
            else:
                messages.error(request,'Invalid credentials')

        except Exception as e:
            messages.error(request, e)

    return render(request,"login.html")


def index(request):
    
    all_blogs = BlogPost.objects.all().order_by("-created_at")
    context = {
        "all_blogs" :all_blogs
    }

    return render(request, "index.html",context=context)


def view_post(request,id):
    post = BlogPost.objects.filter(id = id)

    if len(post)==0:
        return  HttpResponse("No Post Found!")

    else:
        post = post[0]
        return render(request,"view_post.html",{"post":post}) 


def create_blog(request):

    if not request.user.is_authenticated:
        return redirect("/login/")
    
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        try : 
            title = bleach.clean(title ,  tags=[], attributes={}, strip=True)
            content = bleach.clean(content, tags=['a', 'p', 'strong', 'em', "h1" ,"h2" , "h3" , "h4" , "h5" , "h6" , "br" , "hr"], attributes={}, strip=True)
            messages.success(request,"Blog Created Successfully. you can see it at home page. create more blogs here")

            blog = BlogPost(title=title,content=content,author=request.user)
            blog.save()


        except Exception as e:
            print(e)

    return render(request,"create_blog.html")


def update_blog(request,id):

    if not request.user.is_authenticated:
        return redirect("/login/")
    
    blog = BlogPost.objects.filter(id=id)[0]

    if request.user != blog.author:
        messages.error(request,"You are not authorized to edit this blog.")
        return redirect("/logout/")

    if request.method == "POST":
        title_up = request.POST.get("title")
        content_up = request.POST.get("content")



        try : 
            title_up = bleach.clean(title_up ,  tags=[], attributes={}, strip=True)
            content_up = bleach.clean(content_up, tags=['a', 'p', 'strong', 'em', "h1" ,"h2" , "h3" , "h4" , "h5" , "h6" , "br" , "hr"], attributes={}, strip=True)

            blog["title"] = title_up 
            blog["content"] = content_up 
            blog.save()

            messages.error(request,"succesfully  updated!")


        except Exception as e:
            print(e)

        
    return render(request,"create_blog.html",{"update":True,"blog":blog})


def your_blogs(request):

    if not request.user.is_authenticated:
        return redirect("/login/")
    
    user_id =  request.session["user_id"]
    login_user = User.objects.filter(id=user_id)[0]
    post = BlogPost.objects.filter(author = login_user).order_by("-created_at")
    
    if len(post)==0:
        exist = False
    else:
        exist = True

    return render(request,"your_blog.html",{"post":post, "exist":exist})


def logout_user(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    
    logout(request)
    return redirect('/')