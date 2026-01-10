from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Followers, LikePost, Post, Profile


# =========================
# SIGNUP
# =========================
def signup(request):
    try:
        if request.method == 'POST':
            fnm = request.POST.get('fnm')
            emailid = request.POST.get('emailid')
            pwd = request.POST.get('pwd')

            if User.objects.filter(username=fnm).exists():
                return render(request, 'signup.html', {'invalid': 'User already exists'})

            user = User.objects.create_user(
                username=fnm,
                email=emailid,
                password=pwd
            )
            user.save()

            Profile.objects.create(user=user, id_user=user.id)

            login(request, user)
            return redirect('/')

        return render(request, 'signup.html')

    except Exception as e:
        return render(request, 'signup.html', {'invalid': 'Something went wrong'})


# =========================
# LOGIN
# =========================
def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')

        user = authenticate(request, username=fnm, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/')

        return render(request, 'loginn.html', {'invalid': 'Invalid Credentials'})

    return render(request, 'loginn.html')


# =========================
# LOGOUT
# =========================
@login_required(login_url='/loginn')
def logoutt(request):
    logout(request)
    return redirect('/loginn')


# =========================
# HOME
# =========================
@login_required(login_url='/loginn')
def home(request):
    following_users = Followers.objects.filter(
        follower=request.user.username
    ).values_list('user', flat=True)

    posts = Post.objects.filter(
        Q(user=request.user.username) | Q(user__in=following_users)
    ).order_by('-created_at')

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'id_user': request.user.id}
    )

    context = {
        'post': posts,
        'profile': profile,
    }
    return render(request, 'main.html', context)


# =========================
# UPLOAD POST
# =========================
@login_required(login_url='/loginn')
def upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')

        if not image:
            return redirect('/')

        Post.objects.create(
            user=request.user.username,
            image=image,
            caption=caption
        )

        return redirect('/')

    return redirect('/')


# =========================
# LIKE POST
# =========================
@login_required(login_url='/loginn')
def likes(request, id):
    post = get_object_or_404(Post, id=id)
    username = request.user.username

    like = LikePost.objects.filter(post_id=id, username=username).first()

    if like:
        like.delete()
        post.no_of_likes -= 1
    else:
        LikePost.objects.create(post_id=id, username=username)
        post.no_of_likes += 1

    post.save()
    return redirect('/')


# =========================
# EXPLORE
# =========================
@login_required(login_url='/loginn')
def explore(request):
    posts = Post.objects.all().order_by('-created_at')

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'id_user': request.user.id}
    )

    return render(request, 'explore.html', {
        'post': posts,
        'profile': profile
    })


# =========================
# PROFILE
# =========================
@login_required(login_url='/loginn')
def profile(request, user_id):
   
    user_object = get_object_or_404(User, id=user_id)

    
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'id_user': request.user.id}
    )

    user_profile, _ = Profile.objects.get_or_create(
        user=user_object,
        defaults={'id_user': user_object.id}
    )

    
    user_posts = Post.objects.filter(
        user=user_object.username
    ).order_by('-created_at')

    # follow / unfollow status
    follow_unfollow = 'Follow'
    if Followers.objects.filter(
        follower=request.user.username,
        user=user_object.username
    ).exists():
        follow_unfollow = 'Unfollow'

    # ------------------
    # PROFILE UPDATE (POST)
    # ------------------
    if request.method == 'POST' and request.user == user_object:
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')
        image = request.FILES.get('image')

        if image:
            user_profile.profileimg = image

        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('profile', user_id=user_object.id)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_posts.count(),
        'profile': profile,
        'follow_unfollow': follow_unfollow,
        'user_followers': Followers.objects.filter(
            user=user_object.username
        ).count(),
        'user_following': Followers.objects.filter(
            follower=user_object.username
        ).count(),
    }

    return render(request, 'profile.html', context)

# =========================
# DELETE POST (SECURE)
# =========================
@login_required(login_url='/loginn')
def delete(request, id):
    post = get_object_or_404(
        Post,
        id=id,
        user=request.user.username
    )
    post.delete()
    return redirect('profile', user_id=request.user.id)




# =========================
# SEARCH
# =========================
@login_required(login_url='/loginn')
def search_results(request):
    query = request.GET.get('q', '')

    users = Profile.objects.filter(
        user__username__icontains=query
    )
    posts = Post.objects.filter(
        caption__icontains=query
    )

    return render(request, 'search_user.html', {
        'query': query,
        'users': users,
        'posts': posts,
    })


# =========================
# FOLLOW / UNFOLLOW
# =========================
@login_required(login_url='/loginn')
def follow(request):
    if request.method == 'POST':
        follower = request.user.username
        user = request.POST.get('user')

        relation = Followers.objects.filter(
            follower=follower,
            user=user
        ).first()

        if relation:
            relation.delete()
        else:
            Followers.objects.create(
                follower=follower,
                user=user
            )

        user_obj = get_object_or_404(User, username=user)
        return redirect('profile', user_id=user_obj.id)

    return redirect('/')

@login_required(login_url='/loginn')
def home_post(request, id):
    post = get_object_or_404(Post, id=id)
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'id_user': request.user.id}
    )

    return render(request, 'main.html', {
        'post': [post],
        'profile': profile
    })
