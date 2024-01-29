from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Report
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

from guardian.shortcuts import assign_perm, get_perms

@login_required
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'reports/report_list.html', {'reports': reports})


@permission_required('auth.add_user', raise_exception=True)
def create_account(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_view')  # Redirect to a success page or wherever you want
    else:
        form = CustomUserCreationForm()
    return render(request, 'reports/create_account.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('report_list')  # redirect to the main page after login
        else:
            # Return an 'invalid login' error message.
            return render(request, 'reports/sign_in.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'reports/sign_in.html')

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('report_list')  # redirect to the main page after sign up
    else:
        form = UserCreationForm()
    return render(request, 'reports/sign_up.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('sign_in') 

@login_required
def create_report(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        report = Report.objects.create(author=request.user, content=content)
        assign_perm('view_report', request.user, report)
        assign_perm('edit_report', request.user, report)
        assign_perm('delete_report', request.user, report)
        return redirect('report_list')
    return render(request, 'reports/create_report.html')

@login_required
def edit_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if report.author != request.user:
        return render(request, 'reports/access_denied.html')

    if request.method == 'POST':
        report.content = request.POST.get('content')
        report.save()
        return redirect('report_detail', report_id=report.id)
    return render(request, 'reports/edit_report.html', {'report': report})

    
@login_required
def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if report.author != request.user:
        return render(request, 'reports/access_denied.html')
    if request.method == 'POST':
        report.delete()
        return redirect('report_list')
    return render(request, 'reports/confirm_delete.html', {'report': report})

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'reports/report_detail.html', {'report': report})
