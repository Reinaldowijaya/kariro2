from django import forms
from django.utils.html import strip_tags
from kariro_main.models import Applicant,Location,Job_Type,Education,Institution,Course,Skill
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class applicant_form(forms.ModelForm):
	
	location = forms.CharField(max_length=100)
	
	def __init__(self, *args, **kwargs):
		super(applicant_form, self).__init__(*args, **kwargs)
		self.fields['birth_date'].required = True
		self.fields['contact'].required = True
		self.fields['location'].required = True
		
	def is_valid(self):
		form = super(applicant_form, self).is_valid()
		for f in self.errors.iterkeys():
			if f != '__all__':
				self.fields[f].widget.attrs.update({'class': 'error ribbitText'})
		return form
		
	def save(self):
		location_name = self.cleaned_data['location']
		location = Location.objects.get_or_create(name=location_name)[0]
		self.instance.location = location
		return super(applicant_form,self).save()
		
	class Meta:
		fields = ['birth_date', 'contact',]
		model = Applicant
		

# class education_form(forms.ModelForm):

	# location = forms.CharField(max_length=100)
	# institution = forms.CharField(max_length=100)
	# course = forms.CharField(max_length=100)
	
	# def __init__(self, *args, **kwargs):
		# super(education_form, self).__init__(*args, **kwargs)
		# self.fields['location'].required = True
		# self.fields['institution'].required = True
		# self.fields['course'].required = True
		# self.fields['level'].required = True
		# self.fields['ipk'].required = True
		# self.fields['ipk_max'].required = True
		# self.fields['start_date'].required = True
		# self.fields['end_date'].required = True
		# self.fields['description'].required = True
		
	# def save(self):
		# location_name = self.cleaned_data['location']
		# location = Location.objects.get_or_create(name=location_name)[0]
		# self.instance.location = location
		
		# institution_name = self.cleaned_data['institution']
		# institution = Institution.objects.get_or_create(name=institution_name)[0]
		# self.instance.institution = institution
		
		# course_name = self.cleaned_data['course']
		# course = Course.objects.get_or_create(name=course_name)[0]
		# self.instance.course = course
		
		# return super(education_form,self).save()
		
	# class Meta:
		# exclude = ['location', 'course','institution','applicant','id',]
		# model = Education
	
class user_form(UserCreationForm):
	
	email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name'}))
	last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name'}))
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username'}))
	password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))
	
	def is_valid(self):
		form = super(user_form, self).is_valid()
		for f, error in self.errors.iteritems():
			if f != '__all_':
				self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
		return form
		
	class Meta:
		fields = ['email', 'username', 'first_name', 'last_name', 'password1',
				'password2']
		model = User
	
	def save(self, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.username = self.cleaned_data['username']
		user.set_password(self.cleaned_data['password1']) 
		user.save()
		
		
class ResumeForm(forms.ModelForm):

    class Meta:
		model = Applicant
		fields = ('headline','summary',)
		labels = {
			'headline': ('Judul'),
			'summary':('Deskripsi'),
			'skill':('Skill'),
        }
		help_texts = {
			'headline': ('Judul'),
			'summary':('Deskripsi pendek'),
			'skill':('Skill yang kamu punya '),
			}
        
class SkillForm(forms.ModelForm):
		
	class Meta:
		model = Skill
	