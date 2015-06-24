from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import MyUserCreationForm, UserDetailForm


def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, prefix='uf')
        user_detail_form = UserDetailForm(request.POST, prefix='ud')

        if form.is_valid() and user_detail_form.is_valid():
             # check if phone number already exists
            phone_number = user_detail_form.cleaned_data['phone_number']
            if User.objects.filter(username=phone_number).exists():
                messages.info(request, 'This phone number has already been used. Please provide an alternate phone number.', extra_tags='alert alert-info alert-dismissible')
                return render(request, 'account/register.html', {'form': form, 'user_detail_form': user_detail_form})

            new_user = form.save(commit=False)
            new_user.username = phone_number
            new_user.save()
            user_detail_form.save(new_user)
            messages.info(request, 'You have been registered on this portal. Login to continue.', extra_tags='alert alert-info alert-dismissible')
            return redirect('account:login')
    else:
        form = MyUserCreationForm(prefix='uf')
        user_detail_form = UserDetailForm(prefix='ud')  # form to collect additional information from the user
    return render(request, 'account/register.html', {'form': form, 'user_detail_form': user_detail_form})


def logout_view(request):
    logout(request)
    return redirect('home')
