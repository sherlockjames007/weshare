from django.shortcuts import render, redirect
from base.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Q
import json, datetime

# Create your views here.

def login_user(request):
    if request.user.is_authenticated:
        return redirect('base:home')
    if request.method == 'POST':
        user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('base:home')
        else:
            return HttpResponse('invalid login details')
    page = 'login'
    context = {
        'page': page,
    }
    return render(request, 'login_register.html', context)

@login_required
def logout_user(request):
    logout(request)
    return redirect('base:login')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('base:home')
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username = username,
                password = password,
            )
            profile = Profile.objects.create(user = user)
            Follow.objects.create(profile = profile)
            login(request, user)
        except:
            return HttpResponse('invalid details')
        else:
            return redirect('base:home')
    page = 'register'
    context = {
        'page': page,
    }
    return render(request, 'login_register.html', context)

@login_required
def home(request):
    profile = Profile.objects.get(user = request.user)
    following = Follow.objects.get(profile = profile).following.all()
    posts = Post.objects.filter(created_by__in = following)
    context = {
        'posts': posts,
        'following': following,
    }
    return render(request, 'home.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user = request.user)
        photo = request.FILES.get('photo')
        caption = request.POST.get('caption')
        try:
            photo = Photo.objects.create(created_by = request.user, content = photo)
            Post.objects.create(created_by = profile, photo = photo, caption = caption)
        except:
            print('somethings wrong')
        return redirect('base:home')
    return render(request, 'create-post.html', {})
    
@login_required
def show_profile(request, pk):
    profile = Profile.objects.get(user__id = pk)
    following = Follow.objects.get(profile = profile).following.all()
    context = {
        'profile': profile,
        'following': following,
    }
    return render(request, 'show-profile.html', context)

@login_required
def search(request):
    q = request.GET.get('search_query')
    if not q:
        return HttpResponse('invalid request')
    res = Profile.objects.filter(user__username__icontains = q).exclude(user = request.user)
    following = Follow.objects.get(profile = request.user.profile).following.all()
    context = {
        'res': res,
        'following': following,
    }
    return render(request, 'search.html', context)

@login_required
def follow(request, pk):
    if request.method == 'POST':        
        following_profile = Profile.objects.get(user__id = pk)
        profile = Profile.objects.get(user = request.user)        
        Follow.objects.get(profile = profile).following.add(following_profile)
        return redirect('base:home')
    return HttpResponse('invalid request')

@login_required
def unfollow(request, pk):
    if request.method == 'POST':
        following_profile = Profile.objects.get(user__id = pk)
        profile = Profile.objects.get(user = request.user)
        Follow.objects.get(profile = profile).following.remove(following_profile)
        return redirect('base:home')
    return HttpResponse('invalid request')

@login_required
def show_chats(request):
    profile = Profile.objects.get(user = request.user)
    messages = Message.objects.filter(Q(by = profile) | Q(to = profile))
    chats = Profile.objects.filter(Q(messages_sent_by_user__in = messages) | Q(messages_sent_to_user__in = messages)).exclude(user = profile.user).distinct()
    res = []
    for obj in chats:
        mess = Message.objects.filter(by = obj, to = profile).order_by('-upload_time')[:1] | Message.objects.filter(by = profile, to = obj).order_by('-upload_time')[:1]         
        res.append((mess.order_by('-upload_time')[0], obj))
    context = {
        'chats': res
    }    
    return render(request, 'show-chats.html', context)

@login_required
def show_messages(request, pk):
    profile = Profile.objects.get(user = request.user)
    profile2 = Profile.objects.get(user__id = pk)
    messages = Message.objects.filter(by = profile, to = profile2).order_by('upload_time') | Message.objects.filter(by = profile2, to = profile).order_by('-upload_time')
    following = Follow.objects.get(profile = profile).following.all()
    context = {
        'messages': messages,
        'pk': pk,
        'following': following,
    }    
    return render(request, 'show-messages.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pk = data.get('pk')
        message_text = data.get('text')
        by = Profile.objects.get(user = request.user)
        to = Profile.objects.get(user__id = pk)        
        m = Message.objects.create(by = by, to = to, body = message_text)
        return JsonResponse(m.body, safe=False)
    return HttpResponse('invalid request')

@login_required
def settings(request):
    if request.method == 'POST':
        u = User.objects.get(id = request.user.id)
        p = Profile.objects.get(user = u)
        if 'first_name' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            u.first_name = first_name
            u.last_name = u.last_name
            u.save()
        elif 'bio' in request.POST:
            bio = request.POST.get('bio')
            p.bio = bio
            p.save()
        else:
            photo = request.FILES.get('photo')
            photo = Photo.objects.create(created_by = u, content = photo)            
            p.profilePic = photo
            p.save()
        return redirect('base:home')
    return render(request, 'settings.html', {})

