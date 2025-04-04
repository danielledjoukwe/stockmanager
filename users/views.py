from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def users_login(request):
    """
    View for handling user login
    """
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Handle login form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            messages.success(request, f'Bienvenue, {username}!')
            return redirect('dashboard')
        else:
            # Authentication failed
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    # Display login page
    return render(request, 'auth/login.html')

@login_required
def dashboard(request):
    """
    View for the main dashboard (requires login)
    """
    return render(request, 'tableau_de_bord/tableau_de_bord.html')

def logout_user(request):
    """
    View for handling user logout
    """
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')
