'''from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import profilepic
import subprocess

def home(request):
    if request.user.is_authenticated:
        pr = profilepic.objects.all().filter(user=request.user)
        c = {"img": pr}
        return render(request, "home.html", context=c)
    else:
        return redirect('/signin')

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, "login.html", {"error": "Invalid credentials"})
        else:
            return render(request, "login.html")

def signout(request):
    logout(request)
    return redirect('/signin')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confpassword = request.POST['confirmpassword']
        if password == confpassword:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('/')
        else:
            return redirect('/signup')
    else:
        return render(request, 'signup.html')

@login_required
def upload(request):
    if request.method == "POST":
        pr = profilepic.objects.all().filter(user=request.user)
        pr.delete()
        pic = request.FILES['pic']

        new = profilepic(user=request.user, pic=pic)
        new.save()
        return redirect('/home/')
    else:
        return redirect('/home')

def open_camera(request):
    if request.method == 'POST':
        try:
            result = subprocess.run(
                ["python", "virtual_paint.py"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return HttpResponse(f"Script Output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Error: {e.stderr}")
    return render(request, 'open_camera.html')'''  
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages 

from .models import profilepic
import subprocess

def home(request):
    if request.user.is_authenticated:
        pr = profilepic.objects.all().filter(user=request.user)
        c = {"img": pr}
        return render(request, "home.html", context=c)
    else:
        return redirect('signin')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, "login.html", {"error": "Invalid credentials"})
        else:
            return render(request, "login.html")





def signout(request):
    print("hello")
    logout(request)
    return redirect('/signin')



def signup(request):
    print("hello")
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        print("pp")
        if password != confirmpassword:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            print("pp")
            messages.success(request, 'Account created successfully.')
            return redirect('signin')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('signup')

    return render(request, 'signup.html')
@login_required
def upload(request):
    if request.method == "POST":
        pr = profilepic.objects.all().filter(user=request.user)
        pic = request.FILES['pic']

        new = profilepic(user=request.user, pic=pic)
        new.save()
        return redirect('/home/')
    else:
        return redirect('/home')

@login_required
def open_camera(request):
    if request.method == 'POST':
        try:
            result = subprocess.run(
                ["python", "virtual_paint.py"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return HttpResponse(f"Script Output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Error: {e.stderr}")
    return render(request, 'open_camera.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def change_password(request):
    return render(request, 'change_password.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')  # Redirect to home page after success
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'change_password.html', {'form': form})



@login_required
def profile(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }
    return render(request, 'profile.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate the token and reset URL
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())

            reset_link = f'http://{get_current_site(request).domain}/reset/{uid}/{token}/'
            
            # Send the password reset email
            send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n\n{reset_link}',
                'no-reply@yourwebsite.com',
                [email],
                fail_silently=False,
            )
            return redirect('password_reset_done')  # Redirect to a page confirming the email is sent

        else:
            return render(request, 'forgot_password.html', {'error': 'Email not found'})

    return render(request, 'forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        # Decode the user ID from the URL
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()  # Save the new password
                return redirect('password_reset_complete')  # Redirect to a confirmation page
        else:
            form = SetPasswordForm(user)

        return render(request, 'reset_password.html', {'form': form})
    else:
        return redirect('password_reset_invalid')  