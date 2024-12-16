from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
from .forms import ResumeForm, WorkExperienceForm, EducationForm, SkillForm, HobbyForm, LanguageForm, GitHubProfileForm
from django.template.loader import render_to_string
from .models import Resume,WorkExperience,Education,Skill,Hobby,Language,  GitHubProfile
from django.core.mail import EmailMessage


@login_required
def dashboard_view(request):
    return render(request, 'core/dashboard.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'core/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'core/signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Signup successful! You can now log in.')
        return redirect('login')  

    return render(request, 'core/signup.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request) 
    return redirect('login')            

@login_required
def create_resume(request):
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        work_experience_form = WorkExperienceForm(request.POST)
        education_form = EducationForm(request.POST)
        skill_form = SkillForm(request.POST)
        hobby_form = HobbyForm(request.POST)
        language_form = LanguageForm(request.POST)
        github_profile_form = GitHubProfileForm(request.POST)

        print('Resume Form Valid:', resume_form.is_valid())
        print('Work Experience Form Valid:', work_experience_form.is_valid())
        print('Education Form Valid:', education_form.is_valid())
        print('Skill Form Valid:', skill_form.is_valid())
        print('Hobby Form Valid:', hobby_form.is_valid())
        print('Language Form Valid:', language_form.is_valid())
        print('GitHub Profile Form Valid:', github_profile_form.is_valid())

        if all([
            resume_form.is_valid(),
            work_experience_form.is_valid(),
            education_form.is_valid(),
            skill_form.is_valid(),
            hobby_form.is_valid(),
            language_form.is_valid(),
            github_profile_form.is_valid()
        ]):
            # Save the resume
            resume = resume_form.save()

            # Save work experience and link it to the resume
            work_experience = work_experience_form.save(commit=False)
            work_experience.resume = resume
            work_experience.save()

            # Save education and link it to the resume
            education = education_form.save(commit=False)
            education.resume = resume
            education.save()

            # Save skill and link it to the resume
            skill = skill_form.save(commit=False)
            skill.resume = resume
            skill.save()

            # Save hobbies (optional) and link it to the resume
            if hobby_form.cleaned_data.get('hobby_name'):
                hobby = hobby_form.save(commit=False)
                hobby.resume = resume
                hobby.save()

            # Save languages (optional) and link it to the resume
            if language_form.cleaned_data.get('language_name'):
                language = language_form.save(commit=False)
                language.resume = resume
                language.save()

            # Save GitHub profile (optional) and link it to the resume
            if github_profile_form.cleaned_data.get('github_link'):
                github_profile = github_profile_form.save(commit=False)
                github_profile.resume = resume
                github_profile.save()

            messages.success(request, 'Resume created successfully!')
            return redirect('resume_details', resume_id=resume.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        resume_form = ResumeForm()
        work_experience_form = WorkExperienceForm()
        education_form = EducationForm()
        skill_form = SkillForm()
        hobby_form = HobbyForm()
        language_form = LanguageForm()
        github_profile_form = GitHubProfileForm()

    return render(request, 'core/create_resume.html', {
        'resume_form': resume_form,
        'work_experience_form': work_experience_form,
        'education_form': education_form,
        'skill_form': skill_form,
        'hobby_form': hobby_form,
        'language_form': language_form,
        'github_profile_form': github_profile_form,
    })

@login_required
def resume_detail(request, resume_id):
    resume = Resume.objects.get(id=resume_id)
    return render(request, 'core/resume_detail.html', {'resume': resume})

@login_required
def edit_personal_details(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    
    # Handle POST request
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()  
            return redirect('resume_details', resume_id=resume.id)  
    else:
        form = ResumeForm(instance=resume)
    
    return render(request, 'core/edit_personal_details.html', {'form': form})

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    resume.delete()
    return redirect('dashboard')

@login_required
def view_resumes(request):
    resumes = Resume.objects.all()
    print(f"resumes : {resumes} ")  
    return render(request, 'core/view_resumes.html', {'resumes': resumes})

@login_required
def download_resume(request, resume_id):    
    resume = get_object_or_404(Resume, id=resume_id)
    html_string = render_to_string('core/resume_pdf.html', {'resume': resume})
    pdf = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.name}_Resume.pdf"'
    return response

@login_required
def add_experience(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.resume = resume
            experience.save()
            return redirect('resume_details', resume_id=resume.id)
    else:
        form = WorkExperienceForm()
    return render(request, 'core/add_experience.html', {'form': form, 'resume_id': resume_id})


@login_required
def edit_experience(request, experience_id):
    experience = get_object_or_404(WorkExperience, id=experience_id)
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('resume_details', resume_id=experience.resume.id)
    else:
        form = WorkExperienceForm(instance=experience)
    return render(request, 'core/edit_experience.html', {'form': form, 'resume_id': experience.resume.id})

@login_required
def delete_experience(request, experience_id):
    experience = get_object_or_404(WorkExperience, id=experience_id)
    resume_id = experience.resume.id
    experience.delete()
    return redirect('resume_details', resume_id=resume_id)


@login_required
def add_education(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.resume = resume
            education.save()
            return redirect('resume_details', resume_id=resume.id)
    else:
        form = EducationForm()
    return render(request, 'core/add_education.html', {'form': form, 'resume_id': resume_id})


@login_required
def edit_education(request, education_id):
    education = get_object_or_404(Education, id=education_id)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('resume_details', resume_id=education.resume.id)
    else:
        form = EducationForm(instance=education)
    return render(request, 'core/edit_education.html', {'form': form, 'resume_id': education.resume.id})

@login_required
def delete_education(request, education_id):
    education = get_object_or_404(Education, id=education_id)
    resume_id = education.resume.id
    education.delete()
    return redirect('resume_details', resume_id=resume_id)


@login_required
def add_skill(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()
            return redirect('resume_details', resume_id=resume.id)
    else:
        form = SkillForm()
    return render(request, 'core/add_skill.html', {'form': form, 'resume_id': resume_id})


@login_required
def edit_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('resume_details', resume_id=skill.resume.id)
    else:
        form = SkillForm(instance=skill)
    return render(request, 'core/edit_skill.html', {'form': form, 'resume_id': skill.resume.id})


@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    resume_id = skill.resume.id
    skill.delete()
    return redirect('resume_details', resume_id=resume_id)



@login_required
def add_hobby(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        form = HobbyForm(request.POST)
        if form.is_valid():
            hobby = form.save(commit=False)
            hobby.resume = resume  
            hobby.save()
            messages.success(request, 'Hobby added successfully!')
            return redirect('resume_details', resume_id=resume.id)
    else:
        form = HobbyForm()

    return render(request, 'core/add_hobby.html', {'form': form, 'resume': resume})

@login_required
def edit_hobby(request, hobby_id):
    hobby = get_object_or_404(Hobby, id=hobby_id)
    resume = hobby.resume
    if request.method == 'POST':
        form = HobbyForm(request.POST, instance=hobby)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hobby updated successfully!')
            return redirect('resume_details', resume_id=resume.id)
    else:
        form = HobbyForm(instance=hobby)

    return render(request, 'core/edit_hobby.html', {'form': form, 'resume': resume})

@login_required
def delete_hobby(request, hobby_id):
    hobby = get_object_or_404(Hobby, id=hobby_id)
    resume = hobby.resume
    hobby.delete()
    messages.success(request, 'Hobby deleted successfully!')
    return redirect('resume_details', resume_id=resume.id)



@login_required
def add_language(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = form.save(commit=False)
            language.resume = resume  
            language.save()
            messages.success(request, 'Language added successfully!')
            return redirect('resume_details', resume_id=resume.id)
    else:
        form = LanguageForm()

    return render(request, 'core/add_language.html', {'form': form, 'resume': resume})

@login_required
def edit_language(request, language_id):
    language = get_object_or_404(Language, id=language_id)
    resume = language.resume
    if request.method == 'POST':
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            messages.success(request, 'Language updated successfully!')
            return redirect('resume_details', resume_id=resume.id)
    else:
        form = LanguageForm(instance=language)

    return render(request, 'core/edit_language.html', {'form': form, 'resume': resume})

@login_required
def delete_language(request, language_id):
    language = get_object_or_404(Language, id=language_id)
    resume = language.resume
    language.delete()
    messages.success(request, 'Language deleted successfully!')
    return redirect('resume_details', resume_id=resume.id)

@login_required
def add_github_profile(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        form = GitHubProfileForm(request.POST)
        if form.is_valid():
            github_profile = form.save(commit=False)
            github_profile.resume = resume  # Associate the profile with the resume
            github_profile.save()
            return redirect('resume_details', resume_id=resume.id)  # Redirect to resume details
        else:
            print(form.errors)  # Debug: Check for any validation errors
    else:
        form = GitHubProfileForm()
    return render(request, 'core/add_github_profile.html', {'form': form, 'resume': resume})

@login_required
def edit_github_profile(request, github_profile_id):
    github_profile = get_object_or_404(GitHubProfile, id=github_profile_id)
    resume = github_profile.resume
    if request.method == 'POST':
        form = GitHubProfileForm(request.POST, instance=github_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'GitHub Profile updated successfully!')
            return redirect('resume_details', resume_id=resume.id)
    else:
        form = GitHubProfileForm(instance=github_profile)

    return render(request, 'core/edit_github_profile.html', {'form': form, 'resume': resume})

@login_required
def delete_github_profile(request, github_profile_id):
    github_profile = get_object_or_404(GitHubProfile, id=github_profile_id)
    resume = github_profile.resume
    github_profile.delete()
    messages.success(request, 'GitHub Profile deleted successfully!')
    return redirect('resume_details', resume_id=resume.id)



def send_resume_via_email(recipient_email, resume_file_path):
    subject = "Your Resume"
    body = "Please find your resume attached."
    email = EmailMessage(subject, body, 'thammanavamsi721@gmail.com', [recipient_email])
    email.attach_file(resume_file_path)
    email.send()

def send_resume_email(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)

        if not resume.file:
            return JsonResponse({'error': 'No file associated with this resume.'}, status=400)

        resume_file_path = resume.file.path
        recipient_email = request.POST.get('email') 

        send_resume_via_email(recipient_email, resume_file_path)
        return JsonResponse({'success': 'Email sent successfully.'})
    except Resume.DoesNotExist:
        return JsonResponse({'error': 'Resume not found.'}, status=404)
    