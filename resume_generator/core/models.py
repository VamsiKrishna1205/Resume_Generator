import datetime
from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True, max_length=255)
    created_at = models.DateTimeField(default=datetime.datetime(2024, 1, 1))
    file = models.FileField(upload_to='resumes/',null=True, blank=True) 

    def __str__(self):
        return self.name

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work_experience')
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    descriptions = models.TextField()

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.degree} from {self.institution_name}"

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50)

    def __str__(self):
        return self.skill_name
    
class Hobby(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='hobbies')
    hobby_name = models.CharField(max_length=100)

    def __str__(self):
        return self.hobby_name

class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')
    language_name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50)

    def __str__(self):
        return self.language_name
    
    
class GitHubProfile(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='github_profiles', null=True, blank=True)
    github_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.github_link 
