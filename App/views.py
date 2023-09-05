from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from . forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from . models import Record

def home(request):
    return render(request, 'App/home.html')

# Register a User
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')

    context = {'form': form}
    return render(request, 'App/register.html', context=context)

# Login a User
def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, "Wrong Credentials")
                return redirect('login')

    context = {'form': form}
    return render(request, 'App/login.html', context=context)

# User Logout
def user_logout(request):
    try:
        auth.logout(request)
        messages.success(request, "Youre successfully logged out!")
        return redirect('login')
    except:
        return redirect('login')

# Dashboard
@login_required(login_url='login')
def dashboard(request):
    records = Record.objects.all()
    context = {'records': records}
    return render(request, 'App/dashboard.html', context=context)

# Add a record
@login_required(login_url='login')
def create_record(request):
    form = CreateRecordForm()

    if request.method == 'POST':
        form = CreateRecordForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'The record was created successfully!')
            return redirect('dashboard')
        
    context = {'form': form}
    return render(request, 'App/create-record.html', context=context)

# Update a record
@login_required(login_url='login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request, 'The record was updated successfully!')
            return redirect('dashboard')
        
    context = {'form': form}
    return render(request, 'App/update-record.html', context=context)

# Read or View Individual Records
@login_required(login_url='login')
def view_record(request, pk):
    all_records = Record.objects.get(id=pk)

    context = {'record': all_records}

    return render(request, 'App/view-record.html', context=context)

# Delete a View
@login_required(login_url='login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)

    record.delete()
    messages.success(request, 'The record was deleted!')

    return redirect('dashboard')

# Search records
def search_records(request):
    if request.method == 'POST':
        query = request.POST['query']

        records = Record.objects.filter(Q(first_name__icontains = query) | Q(last_name__icontains = query) | Q(email__icontains = query) | Q(phone__icontains = query) | Q(address__icontains = query) | Q(city__icontains = query) | Q(province__icontains = query) | Q(country__icontains = query))

        return render(request, 'App/dashboard.html', context = {'query': query, 'records': records})
    
    return render(request, 'App/dashboard.html')
