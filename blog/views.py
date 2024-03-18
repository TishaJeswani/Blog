from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .forms import signupform,Loginform,PostmethodForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Postmethod
from django.contrib .auth.models import Group

def home(request):
    posts=Postmethod.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

def about(request):
    return render(request,'blog/about.html')

def contact(request):
    return render(request,'blog/contact.html')
def user_login(request):
     if not request.user.is_authenticated:
        if request.method == "POST":
            form = Loginform(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)  
                    messages.success(request, 'Logged in successfully!!!')
                    return HttpResponseRedirect('/blog/dashboard/')  
                else:
                    messages.error(request, 'Invalid username or password')
        else:
            form = Loginform()
        return render(request, 'blog/login.html', {'form': form})
     else:
          return HttpResponseRedirect('/blog/dashboard/')
   
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/blog')
def user_signup(request):
        if request.method=="POST":
            form=signupform(request.POST)
            if form.is_valid():
                messages.success(request, 'Congratulations!! You have become an Author ')
                user=form.save() 
                group=Group.objects.get(name='author')
                user.groups.add(group)
                return render(request, 'blog/signup.html', {'form': signupform()})
            else:   
                return render(request, 'blog/signup.html', {'form': form})
        else:
            form=signupform()
            return render(request,'blog/signup.html',{'form':form})
def dashboard(request):

    if request.user.is_authenticated:
            posts=Postmethod.objects.all()
            user=request.user
            fullname=user.get_full_name()
            gps=user.groups.all()

            return render(request, 'blog/dashboard.html',{'posts':posts,'fullname':fullname,'groups':gps})

    else:
        return HttpResponseRedirect('/blog/login/')
def add_post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=PostmethodForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=Postmethod(title=title,desc=desc)
                pst.save()
                return HttpResponseRedirect('/blog/') 
        else:
            form=PostmethodForm()
            return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/blog/login/')
def update_post(request, id):
    if request.user.is_authenticated:
        post_instance = get_object_or_404(Postmethod, pk=id)
        
        if request.method == 'POST':
            form = PostmethodForm(request.POST, instance=post_instance)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/blog/dashboard/')  # Redirect after successful update
        else:
            form = PostmethodForm(instance=post_instance)
            
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/blog/login/')
def delete_post(request,id):
    if request.user.is_authenticated:
         if request.method == 'POST':
             pi=Postmethod.objects.get(pk=id)
             pi.delete()
             return HttpResponseRedirect('/blog/dashboard')
    else:
        return HttpResponseRedirect('/blog/login/')
   
    