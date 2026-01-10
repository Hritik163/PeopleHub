from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Profile, Post, LikePost, Followers


# =====================
# AUTH
# =====================
def signup(request):
    if request.method == "POST":
        username = request.POST.get("fnm")
        email = request.POST.get("emailid")
        password = request.POST.get("pwd")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"invalid": "User already exists"})

        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user, id_user=user.id)
        login(request, user)
        return redirect("/")

    return render(request, "signup.html")


def loginn(request):
    if request.method == "POST":
        username = request.POST.get("fnm")
        password = request.POST.get("pwd")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")

        return render(request, "loginn.html", {"invalid": "Invalid credentials"})

    return render(request, "loginn.html")


@login_required(login_url="/loginn/")
def logoutt(request):
    logout(request)
    return redirect("/loginn/")


# =====================
# HOME
# =====================
@login_required(login_url="/loginn/")
def home(request):
    profile = Profile.objects.get(user=request.user)

    following = Followers.objects.filter(
        follower=request.user.username
    ).values_list("user", flat=True)

    posts = Post.objects.filter(
        Q(user=request.user.username) | Q(user__in=following)
    ).order_by("-created_at")

    return render(request, "main.html", {
        "profile": profile,
        "post": posts
    })


# =====================
# UPLOAD POST
# =====================
@login_required(login_url="/loginn/")
def upload(request):
    if request.method == "POST":
        image = request.FILES.get("image_upload")
        caption = request.POST.get("caption")

        if not image:
            return redirect("/")

        Post.objects.create(
            user=request.user.username,
            image=image,
            caption=caption
        )

    return redirect("/")


# =====================
# LIKE POST
# =====================
@login_required(login_url="/loginn/")
def likes(request, id):
    post = get_object_or_404(Post, id=id)
    like = LikePost.objects.filter(post_id=str(id), username=request.user.username).first()

    if like:
        like.delete()
        post.no_of_likes -= 1
    else:
        LikePost.objects.create(post_id=str(id), username=request.user.username)
        post.no_of_likes += 1

    post.save()
    return redirect("/")


# =====================
# PROFILE
# =====================
@login_required(login_url="/loginn/")
def profile(request, user_id):
    user_object = get_object_or_404(User, id=user_id)
    user_profile = Profile.objects.get(user=user_object)
    profile = Profile.objects.get(user=request.user)

    user_posts = Post.objects.filter(user=user_object.username)

    follow_status = Followers.objects.filter(
        follower=request.user.username,
        user=user_object.username
    ).exists()

    if request.method == "POST" and request.user == user_object:
        bio = request.POST.get("bio")
        location = request.POST.get("location")
        image = request.FILES.get("image")

        if image:
            user_profile.profileimg = image

        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect("profile", user_id=user_id)

    return render(request, "profile.html", {
        "user_object": user_object,
        "user_profile": user_profile,
        "profile": profile,
        "user_posts": user_posts,
        "user_post_length": user_posts.count(),
        "follow_unfollow": "Unfollow" if follow_status else "Follow",
        "user_followers": Followers.objects.filter(user=user_object.username).count(),
        "user_following": Followers.objects.filter(follower=user_object.username).count(),
    })


# =====================
# DELETE POST
# =====================
@login_required(login_url="/loginn/")
def delete(request, id):
    post = get_object_or_404(Post, id=id, user=request.user.username)
    post.delete()
    return redirect("profile", user_id=request.user.id)


# =====================
# SEARCH (🔥 MISSING FUNCTION — FIXED)
# =====================
@login_required(login_url="/loginn/")
def search_results(request):
    query = request.GET.get("q", "")

    users = Profile.objects.filter(
        user__username__icontains=query
    )

    posts = Post.objects.filter(
        caption__icontains=query
    )

    return render(request, "search_user.html", {
        "query": query,
        "users": users,
        "posts": posts
    })


# =====================
# FOLLOW / UNFOLLOW
# =====================
@login_required(login_url="/loginn/")
def follow(request):
    if request.method == "POST":
        follower = request.user.username
        user = request.POST.get("user")

        relation = Followers.objects.filter(follower=follower, user=user).first()
        if relation:
            relation.delete()
        else:
            Followers.objects.create(follower=follower, user=user)

    user_obj = User.objects.get(username=user)
    return redirect("profile", user_id=user_obj.id)
