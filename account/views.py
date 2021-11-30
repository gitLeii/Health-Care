from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def register_user(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New user created successfully !!!') 
            return redirect("account:login")
            
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})