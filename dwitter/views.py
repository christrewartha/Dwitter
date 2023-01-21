from django.shortcuts import render, redirect
from .forms import DweetForm
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
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")

    followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")

    return render(
        request,
        "dwitter/dashboard.html",
        {"form": form, "dweets": followed_dweets},
    )
