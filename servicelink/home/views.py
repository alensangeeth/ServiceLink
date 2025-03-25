from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from .models import User,ServiceProvider, Category
from .forms import SignupForm, LoginForm, ServiceProviderForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.urls import reverse  

from django.http import HttpResponse
# def index(request):
#     print("User authenticated:", request.user.is_authenticated)
#     return render(request, "home.html")


def service(request):
    return render(request, 'service.html')

def booking(request):
    return HttpResponse("booking page")

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(email=email)  # Get user by email
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
                return redirect("login")

            # ✅ Check password and authenticate properly
            if check_password(password, user.password):
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # Required for custom users
                login(request, user)  # ✅ This logs the user in properly

                request.session["user_role"] = user.role  # Keep role if needed
                messages.success(request, "Login successful!")
                return redirect("home")  # Redirect to home or dashboard

            else:
                messages.error(request, "Invalid email or password.")
                return redirect("login")
        else:
            messages.error(request, "Invalid form input.")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})




@login_required
def index(request):
    full_name = request.user.full_name if request.user.full_name else request.user.email
    return render(request, 'home.html', {'full_name': full_name})




def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():  # ✅ Check if email exists
            messages.error(request, "Email already registered. Please log in.")
            return redirect('signup')  # Redirect back to signup page

        if form.is_valid():
            user = form.save()  # Saves user with hashed password

            # ✅ Authenticate user (using email instead of username)
            user = authenticate(email=user.email, password=form.cleaned_data['password'])

            if user:
                login(request, user)  # ✅ Log the user in
                return redirect('service')  # ✅ Redirect to service page

        else:
            print("Form errors:", form.errors)  # Debugging: See form errors
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})
    
# Custom authentication backend for ServiceProvider
class ServiceProviderBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            provider = ServiceProvider.objects.get(email=email)
            if provider.password == password:  # Replace with hashed password check
                return provider
        except ServiceProvider.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return ServiceProvider.objects.get(pk=user_id)
        except ServiceProvider.DoesNotExist:
            return None

def providersignup(request):
    if request.method == "POST":
        form = ServiceProviderForm(request.POST)
        if form.is_valid():
            category_id = form.cleaned_data["category_id"]

            try:
                category = Category.objects.get(category_id=category_id)
            except Category.DoesNotExist:
                category = None

            if category:
                provider = ServiceProvider(
                    company_name=form.cleaned_data["company_name"],
                    email=form.cleaned_data["email"],
                    password=make_password(form.cleaned_data["password"]),  # ✅ Hash password
                    phone=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                    category=category,
                    verified=False,
                )

                provider.save()  # ✅ Ensure the provider is saved before accessing provider.id

                # ✅ Store provider in session (since it's not Django's auth user)
                request.session['provider_id'] = provider.pk  # Using .pk instead of .id
                request.session['provider_email'] = provider.email  # Optional for display
                
                return redirect("service")  # Redirect after successful signup

    else:
        form = ServiceProviderForm()

    return render(request, "providersignup.html", {"form": form})

def providerlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            provider = ServiceProvider.objects.get(email=email)
            print("✅ Provider Found:", provider.company_name)
            print("Stored Hashed Password:", provider.password)  # Debugging

            if check_password(password, provider.password):  # ✅ Correctly compare hashed password
                request.session["provider_id"] = provider.provider_id
                request.session["provider_email"] = provider.email

                print("✅ Login Successful, Redirecting...")  # Debugging
                return redirect("service")  
            else:
                print("❌ Incorrect Password")  # Debugging
                messages.error(request, "Invalid email or password!")

        except ServiceProvider.DoesNotExist:
            print("❌ Provider Not Found")  # Debugging
            messages.error(request, "Provider does not exist!")

    return render(request, "providerlogin.html")


def user_logout(request):
    logout(request)  # Logs out the user
    request.session.flush()  # Clears all session data
    return redirect(reverse('home'))  # Redirect to home page after logout

# def user_logout(request):
#     logout(request)  # Logs out the user
#     return redirect('/')  # Explicitly redirect to home page

def provider_logout(request):
    if "provider_id" in request.session:
        del request.session["provider_id"]  # Remove provider session
    return redirect("home")  # Redirect to homepage

# List all service providers
def service_provider_list(request):
    providers = ServiceProvider.objects.all()
    return render(request, 'service_providers/list.html', {'providers': providers})

# Create a new service provider
def add_service_provider(request):
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_provider_list')
    else:
        form = ServiceProviderForm()
    return render(request, 'service_providers/form.html', {'form': form})

# Edit an existing service provider
def edit_service_provider(request, provider_id):
    provider = get_object_or_404(ServiceProvider, pk=provider_id)
    if request.method == 'POST':
        form = ServiceProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('service_provider_list')
    else:
        form = ServiceProviderForm(instance=provider)
    return render(request, 'service_providers/form.html', {'form': form})

# Delete a service provider
def delete_service_provider(request, provider_id):
    provider = get_object_or_404(ServiceProvider, pk=provider_id)
    provider.delete()
    return redirect('service_provider_list')

