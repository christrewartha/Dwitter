from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from .forms import DweetForm, CustomUserCreationForm
from .models import Profile, Dweet


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})


def profile(request, pk):
    prof = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(prof)
        elif action == "unfollow":
            current_user_profile.follows.remove(prof)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": prof})


def dashboard(request):
    form = DweetForm(request.POST or None)
    followed_dweets = []
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")

    if request.user.is_authenticated:
        followed_dweets = Dweet.objects.filter(
            user__profile__in=request.user.profile.follows.all()
        ).order_by("-created_at")

    return render(
        request,
        "dwitter/dashboard.html",
        {"form": form, "dweets": followed_dweets},
    )


def register(request):
    if request.method == "GET":
        return render(
            request,
            'dwitter/register.html',
            {'form': CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('dashboard'))
