from django.contrib import auth
from django.contrib.auth import login, logout
from .models import Profile, CustomUser
from .forms import CustomUserSignupForm, CustomUserSigninForm
from django.shortcuts import render, redirect


def signup(request):
    form = CustomUserSignupForm()
    #착한 사용자
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    #나쁜 사용자
    return render(request, 'newSignup.html', {"form":form})
def signin(request):
    form = CustomUserSigninForm()
    #착한 사용자
    if request.method == "POST":
        form = CustomUserSigninForm(request,request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    #나쁜 사용자
    return render(request, "newSignin.html", {"form":form})
    
def signout(request):
    logout(request)
    return redirect('home')

def new_profile(request):
    #로그인 하지 않았다면 프로필 누르더라도 계속 홈으로 이동
    if request.user.is_anonymous:
        return redirect("home")
    #로그인을 했다면 해당 user의 프로필 보기
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'newProfile.html', {"profile":profile})

def create_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.nickname = request.POST.get('nickname')
        print(profile.nickname)
        profile.image = request.FILES.get('image')
        profile.save()
        return redirect("users:new_profile")
    
    return render(request, "newProfile.html", {"profile":profile})
    # get한다는것은 이미 존재한다 = created = FALSE
    # create 한다는 것은 존재하지 않는다 = created = TRUE

# # 회원가입
# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             user = User.objects.create_user(
#                 username=request.POST['username'],
#                 password=request.POST['password1'],
#                 email=request.POST['email'],)
#             profile = Profile(user=user, nickname=request.POST['nickname'], image=request.FILES.get('profile_image'))
#             profile.save()

#             auth.login(request, user)
#             return redirect('/')
#         return render(request, 'signup.html')
#     return render(request, 'signup.html')

# # 로그인
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')

# # 로그아웃
# def logout(request):
#   auth.logout(request)
#   return redirect('home')