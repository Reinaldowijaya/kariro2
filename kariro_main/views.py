# Create your views here.
from django.shortcuts import render,render_to_response, get_object_or_404,redirect,HttpResponseRedirect,Http404
from kariro_main.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from kariro_main.forms import applicant_form ,ResumeForm, SkillForm
from django.forms.models import modelformset_factory,inlineformset_factory
from django.views.generic import ListView,DetailView,UpdateView
from actstream.models import user_stream

class Jobs(ListView):

	queryset = Job_Vacancy.objects.order_by('posted')[:5]
	context_object_name = 'latest_job_vacancy'
	template_name = 'jobs.html'

class Jobs_Detail(DetailView):

	model = Job_Vacancy
	context_object_name = "id"
	template_name = 'jobs_detail.html'

@login_required
def profile(request,applicantform = None,educationform = None):

	applicant = request.user.get_profile().applicant

	if applicant.signup == True:
		return HttpResponseRedirect('/')

	EducationFormSet = inlineformset_factory(Applicant,Education,extra=1)
	educationform = EducationFormSet(instance=applicant,prefix="education")
	applicantform = applicant_form(instance=applicant,prefix="applicant")
	# educationform = education_form(instance=applicant,prefix="education")
	if request.method == "POST":
		applicantform = applicant_form(request.POST,instance=applicant,prefix="applicant")
		educationform = EducationFormSet(request.POST,instance=applicant,prefix="education")
		# educationform = education_form(request.POST,instance=applicant,prefix="education")

		if applicantform.is_valid() and educationform.is_valid() :
			applicantform.save()
			applicant.signup = True
			applicant.save()
			educationform.save()

			return HttpResponseRedirect('/')

	return render(request,
					'signup_profile.html',
					{'applicant_form': applicantform,'educationformset':educationform,})

@login_required
def user_profile(request,resumeform = None, educationform = None,workform=None ,skillform = None):

	applicant = request.user.get_profile().applicant

	if applicant.signup == False:
		return HttpResponseRedirect(reverse('kariro_main.views.profile', ))
	#Creation of forms
	EducationFormSet = inlineformset_factory(Applicant,Education,extra=1,exclude=('applicant',))
	WorkFormSet =  inlineformset_factory(Applicant,Work_Experience,extra=1,exclude=('applicant',))

	#pass form argument
	resumeform = ResumeForm(instance=applicant)
	educationformset = EducationFormSet(instance=applicant)
	workformset=WorkFormSet(instance=applicant)
	skillform = SkillForm()

	if request.method == "POST":
		#update education
		if 'education' in request.POST:
			educationformset = EducationFormSet(request.POST,instance = applicant)

			if educationformset.is_valid():
				educationformset.save()
				return HttpResponseRedirect(reverse('kariro_main.views.user_profile', ))

		#update work
		elif 'work' in request.POST:
			workformset = WorkFormSet(request.POST,instance = applicant)

			if workformset.is_valid():
				workformset.save()
				return HttpResponseRedirect(reverse('kariro_main.views.user_profile'))

		elif 'skillform' in request.POST:
			#update skill
			skillform = SkillForm(data=request.POST)

			if skillform.is_valid():
				skill_name = skillform.cleaned_data['name']
				new_skill = Skill.objects.get_or_create(name=skill_name)[0]
				applicant.skill.add(new_skill)
				return HttpResponseRedirect(reverse('kariro_main.views.user_profile'))
		else:
			#update resume
			resumeform = ResumeForm(data=request.POST)

			if resumeform.is_valid():

				applicant.headline = resumeform.cleaned_data['headline']
				applicant.summary = resumeform.cleaned_data['summary']
				applicant.save()

				return HttpResponseRedirect(reverse('kariro_main.views.user_profile'))

	return render(request, 'userprofile.html', {'userprofile':applicant,'resumeform':resumeform,'educationformset':educationformset,'workformset':workformset,'skillform':skillform})

@login_required
def dashboard(request):
	applicant = request.user
	newsfeed=user_stream(applicant)
	return render(request,	'user_dashboard.html',{'newsfeed': newsfeed,'applicant':applicant})

