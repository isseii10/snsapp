from django.db.models.base import Model
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import SnsModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.

def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, '', password)
            return render(request, 'signup.html', {})
        except IntegrityError:
            return render(request, 'signup.html', {'error':'このユーザー名はすでに登録されています。'}) 

    return render(request, 'signup.html', {})

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'login.html', {'context':'not logged in'})
    
    return render(request, 'login.html', {'context': 'get method'})

def logoutfunc(request):
    logout(request)
    return redirect('login')


def listfunc(request):
    object_list = SnsModel.objects.all()
    return render(request, 'list.html', {'object_list':object_list})

def detailfunc(request, pk):
    obj = get_object_or_404(SnsModel, pk=pk)
    return render(request, 'detail.html', {'object':obj})


def goodfunc(request, pk):
    obj = SnsModel.objects.get(pk=pk)
    obj.good += 1
    obj.save()
    return redirect('list')

def readfunc(request, pk):
    obj = SnsModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in obj.readtext:
        return redirect('list')
    else:
        obj.read += 1
        obj.readtext += ' ' + username
        obj.save()
        return redirect('list')

class SnsCreate(CreateView):
    template_name = 'create.html'
    model = SnsModel
    fields = ('title', 'content', 'author', 'snsimage')
    success_url = reverse_lazy('list')
