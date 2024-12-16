from django import forms
from .models import Resume, WorkExperience, Education, Skill,Hobby, Language, GitHubProfile

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'email', 'phone_number', 'address', 'file']

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company_name', 'start_date', 'end_date', 'descriptions']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution_name', 'start_date', 'end_date', 'description']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'proficiency']

class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        fields = ['hobby_name']

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language_name', 'proficiency']

class GitHubProfileForm(forms.ModelForm):
    class Meta:
        model = GitHubProfile
        fields = ['github_link']
