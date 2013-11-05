from django import forms
from kariro_main.models import Company,Job_Vacancy

class CompanyForm(forms.ModelForm):

    class Meta:
		model = Company
		exclude = ('userprofile','slug',)

class JobForm(forms.ModelForm):

    class Meta:
		model = Job_Vacancy
		exclude = ('posted','slug','company',)
