from django.contrib import admin
from .models import Resume, WorkExperience, Education, Skill, Hobby, Language, GitHubProfile

admin.site.register(Resume)
admin.site.register(WorkExperience)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Hobby)
admin.site.register(Language)
admin.site.register(GitHubProfile)