from django.contrib import admin
from .models import *

	
class JobAdmin(admin.ModelAdmin):
	list_display = ('name', 'company')
	
admin.site.register(Company)
admin.site.register(UserProfile)
admin.site.register(Job_Vacancy, JobAdmin)
admin.site.register(Applicant)
admin.site.register(Education)
admin.site.register(Work_Experience)
admin.site.register(Achievement)
admin.site.register(Application)
admin.site.register(Location)
admin.site.register(Job_Type)
admin.site.register(Language)
admin.site.register(Skill)
admin.site.register(Industry)
admin.site.register(Institution)
admin.site.register(Course)

