

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Application
from .form import ApplicationForm

# Candidate: Submit new application
@login_required
def home(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            return redirect('home')
    else:
        form = ApplicationForm()
    return render(request, 'app1/home.html', {'form': form})

# Candidate: My Applications
@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'app1/my_applications.html', {'applications': applications})

# Candidate: Edit Application
@login_required
def edit_application(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if application.status != 'submitted':
        return render(request, 'cannot_edit.html', {'application': application})
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return redirect('my_applications')
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'app1/edit_application.html', {'form': form})

# Recruiter: Dashboard
@staff_member_required
def recruiter_dashboard(request):
    applications = Application.objects.filter(job__recruiter=request.user).order_by('-updated_at')
    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        application = get_object_or_404(
            Application,
            pk=app_id,
            job__recruiter=request.user
        )

        application.status = new_status
        application.save()
        return redirect('recruiter_dashboard')

    return render(request, 'app1/recruiter_dashboard.html', {'applications': applications})


@staff_member_required
def view_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    if application.status == 'submitted':
        application.status = 'under_review'
        application.save()
    
    return render(request, 'app1/view_application.html', {'application': application})