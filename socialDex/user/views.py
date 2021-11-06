from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserInfo
from django.utils import timezone
from api.models import Post
from django.db.models import Count



#get_ip
def getIpAdd(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful.")
			return redirect("user:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="user/register.html", context={"register_form":form})

def login_request(request):
	ip_address = getIpAdd(request)

	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				try:
					user_info = UserInfo.objects.get(user=user)
				except:
					user_info = UserInfo.objects.create(user=user)
				user_info.last_login = timezone.now()
				user_info.save()
				ip_address = getIpAdd(request)
				if ip_address != user_info.ip_address:
					user_info.ip_address = ip_address
					user_info.save()
					return redirect(f"/ip_check/?next={next}")

				return redirect("api:home")
			else:
				messages.error(request,"Invalid username or password.")

		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="user/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("user:login")

@login_required
def profile(request, id):
	number_of_posts = Post.objects.filter(user=request.user).count()
	return render(request, 'user/profile.html', {'id':id, 'number_of_posts': number_of_posts})


#ip_check_view
@login_required()
def ip_check_view(request):
    context = {}
    return render(request, 'user/ip_check.html', context)

