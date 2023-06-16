from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import TODO
from users.models import User
from .forms import LoginForm

from datetime import datetime
from typing import Dict
import time

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home_index')
        else:
            return view_func(request,*args,**kwargs)

    return wrapper_func

@login_required(login_url='login')
# Create your views here.
def index(request):
    if request.method=="POST":
        name = request.POST.get("name",None)
        dt = datetime.strptime(request.POST.get("datetime",None),'%Y-%m-%dT%H:%M')
        try:
            tmp = TODO(name=name,create_date=datetime.now(),todo_date=dt,user=request.user)
            tmp.clean()
            tmp.save()
        except Exception as ex:
            request.session["index_error"]=ex.message
        return redirect("home_index")
    return render(request,'index.html',{
        "todo_list":TODO.objects.filter(user=request.user).order_by("-todo_date"),
        "count_of_not_done":TODO.objects.filter(user=request.user,done=False).count(),
        "error":request.session.pop("index_error",None)
        })

@login_required(login_url='login')
def delete_todo(request):
    json_response:Dict={}
    if request.method=="POST":
        todo_id:int=request.POST.get("id",None)
        if todo_id is None:
            json_response["error"]=f'Id {todo_id} není v POST'
            return JsonResponse(json_response,status=504)            
        if not TODO.objects.filter(id=todo_id).exists():
            json_response["error"]=f'Id {todo_id} není zaznamenán'
            return JsonResponse(json_response,status=504)   
        TODO.objects.get(id=todo_id).delete()
        return JsonResponse(json_response,status=200)

@login_required(login_url='login')
def change_todo(request):
    json_response:Dict={}
    if request.method=="POST":
        todo_id:int=request.POST.get("id",None)
        if todo_id is None:
            json_response["error"]=f'Id {todo_id} není v POST'
            return JsonResponse(json_response,status=504)            
        if not TODO.objects.filter(id=todo_id).exists():
            json_response["error"]=f'Id {todo_id} není zaznamenán'
            return JsonResponse(json_response,status=504)   
        tmp = TODO.objects.get(id=todo_id)
        tmp.done=not tmp.done
        tmp.save()
        json_response["result"]=tmp.done
        return JsonResponse(json_response,status=200)

@login_required(login_url='login')
def get_not_done(request):
    return JsonResponse({"count_of_not_done":TODO.objects.filter(user=request.user,done=False).count()},status=200)

@unauthenticated_user
def login_page(request,error=None):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Ověřte jméno a heslo
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Přihlásit uživatele
                login(request, user)
                return redirect('home_index')
            else:
                messages.info(request,"Neplatné přihlášení, zkuste znovu")
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def logout_path(request):
    logout(request)
    return redirect("login")