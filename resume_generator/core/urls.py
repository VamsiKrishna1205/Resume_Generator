from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create/', views.create_resume, name='create_resume'),
    path('resumes/', views.view_resumes, name='view_resumes'),
    path('resumes/<int:resume_id>/download/', views.download_resume, name='download_resume'),
    path('send-resume-email/<int:resume_id>/', views.send_resume_email, name='send_resume_email'),

    
    # Resume
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_details'),
    path('resume/<int:resume_id>/edit_personal/', views.edit_personal_details, name='edit_personal_details'),
    path('resume/<int:resume_id>/delete/', views.delete_resume, name='delete_resume'),

    # Work Experience
    path('resume/<int:resume_id>/experience/add/', views.add_experience, name='add_experience'),
    path('experience/<int:experience_id>/edit/', views.edit_experience, name='edit_experience'),
    path('experience/<int:experience_id>/delete/', views.delete_experience, name='delete_experience'),

    # Education
    path('resume/<int:resume_id>/education/add/', views.add_education, name='add_education'),
    path('education/<int:education_id>/edit/', views.edit_education, name='edit_education'),
    path('education/<int:education_id>/delete/', views.delete_education, name='delete_education'),

    # Skills
    path('resume/<int:resume_id>/skills/add/', views.add_skill, name='add_skill'),
    path('skill/<int:skill_id>/edit/', views.edit_skill, name='edit_skill'),
    path('skill/<int:skill_id>/delete/', views.delete_skill, name='delete_skill'),
    
    
    # hobby
    path('resume/<int:resume_id>/add_hobby/', views.add_hobby, name='add_hobby'),
    path('hobby/<int:hobby_id>/edit/', views.edit_hobby, name='edit_hobby'),
    path('hobby/<int:hobby_id>/delete/', views.delete_hobby, name='delete_hobby'),
    
    # language
    path('resume/<int:resume_id>/add_language/', views.add_language, name='add_language'),
    path('language/<int:language_id>/edit/', views.edit_language, name='edit_language'),
    path('language/<int:language_id>/delete/', views.delete_language, name='delete_language'),
    
    # GitHub profile
    path('resume/<int:resume_id>/add_github_profile/', views.add_github_profile, name='add_github_profile'),
    path('github_profile/<int:github_profile_id>/edit/', views.edit_github_profile, name='edit_github_profile'),
    path('github_profile/<int:github_profile_id>/delete/', views.delete_github_profile, name='delete_github_profile'),
]