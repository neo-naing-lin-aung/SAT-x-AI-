from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from .forms import EditUsernameForm, CustomPasswordChangeForm


def register(request):
    """Register a new user."""
    if request.method == "GET":
        # Show registration form.
        form = UserCreationForm()
    else:
        # Process the completed form.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            form.save()

            # Redirect the user to log in page 
            return redirect("accounts:login")
        
    # Display the registration form 
    context = {"form": form}
    return render(request, "registration/register.html", context)


def edit_profile(request):
    """Render Edit Profile Page."""
    if request.method == "GET":
        username_form = EditUsernameForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    else:
        # Process completed forms
        action = request.POST.get("action")

        if action == "edit_username":
            username_form = EditUsernameForm(
                request.POST, 
                instance=request.user,
            )

            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Username updated successfully!")
                return redirect("accounts:edit_profile")

        elif action == "change_password":
            password_form = CustomPasswordChangeForm(
                request.POST, 
                request.user,
            )

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully!")
                return redirect("accounts:edit_profile")

    context = {"username_form": username_form, "password_form": password_form}
    return render(request, "registration/edit_profile.html", context)