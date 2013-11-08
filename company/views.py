from django.shortcuts import render,render_to_response, get_object_or_404,redirect,HttpResponseRedirect,Http404
from kariro_main.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,UpdateView
from company.forms import CompanyForm,JobForm
from actstream import action
from actstream.actions import follow, unfollow
from actstream.models import following, followers

class Company_List(ListView):
	queryset = Company.objects.order_by('company_name')[:10]
	context_object_name = 'company_list'
	template_name = 'company.html'

def Company_Detail (request,pk = "", slug = ""):

	try:
		company = Company.objects.get(pk = pk)
	except Company.DoesNotExist:
		raise Http404

	if request.method == "POST":
		if 'follow' in request.POST:
			follow_id = request.POST.get('follow', False)
			if follow_id:
				try:
					company_id = Company.objects.get(pk=follow_id)
					follow(request.user, company_id)
					#request.user.get_profile().applicant
				except Company.DoesNotExist:
					return render(request, 'company_detail.html', {'id': company,'follow':False })
		else:
			unfollow_id = request.POST.get('unfollow', False)
			if unfollow_id:
				try:
					company_id = Company.objects.get(pk=unfollow_id)
					unfollow(request.user, company_id)
					#request.user.get_profile().applicant
				except Company.DoesNotExist:
					return render(request, 'company_detail.html', {'id': company,'follow':True })
	if followers(company):
		print followers(company)
		return render(request, 'company_detail.html', {'id': company,'follow':False })
	return render(request, 'company_detail.html', {'id': company,'follow':True })

@login_required
def Company_Dashboard(request):

	if request.user.get_profile().type() != "C":
		return redirect ("/")

	company = request.user.get_profile().company

	return render(request, 'dashboard.html', {'company':company})

@login_required
def Company_Profile(request,company_form = None):

	if request.user.get_profile().type() != "C":
		return redirect ("/")

	company = request.user.get_profile().company
	company_form = CompanyForm(instance=company)

	if request.method == "POST":
		company_form = CompanyForm(data=request.POST,instance=company)

		if company_form.is_valid():
			company_form.save()
			return HttpResponseRedirect(reverse('company.views.Company_Profile'))

	return render(request, 'company_profile.html', {'companyform':company_form,'company':company})

@login_required
def Company_Job(request):

	if request.user.get_profile().type() != "C":
		return redirect ("/")

	company = request.user.get_profile().company
	job_list = company.job_vacancy_set.all()

	return render(request, 'company_job.html', {'job_list':job_list,'company':company})

@login_required
def Post_Job(request):

	if request.user.get_profile().type() != "C":
		return redirect ("/")

	company = request.user.get_profile().company
	job_form = JobForm()

	if request.method == "POST":
		job_form = JobForm(data=request.POST)

		if job_form.is_valid():
			job_vacancy = job_form.save(commit = False)
			job_vacancy.company = company
			job_vacancy.save()
			action.send(company, verb='posted', action_object=job_vacancy)
			return HttpResponseRedirect(reverse('company.views.Company_Job'))

	return render(request, 'job_new.html', {'job_form':job_form,'company':company})

@login_required
def Company_Job_Detail(request,job_id):

	if request.user.get_profile().type() != "C":
		return redirect ("/")

	company = request.user.get_profile().company
	job = Job_Vacancy.objects.get(pk = job_id)

	if company != job.company:
		raise Http404

	applications = job.application_set.all().order_by('matching')

	return render(request, 'company_job_detail.html', {'applications':applications,'job':job})

@login_required
def Edit_Job(request,job_id):

	if request.user.get_profile().type() != "C":
		return redirect ("/")

	company = request.user.get_profile().company
	job = Job_Vacancy.objects.get(pk = job_id)

	if company != job.company:
		raise Http404

	job_form = JobForm(instance = job)

	if request.method == "POST":
		job_form = JobForm(data=request.POST,instance = job)

		if job_form.is_valid():
			job_vacancy = job_form.save(commit = False)
			job_vacancy.save()
			return HttpResponseRedirect(reverse('company.views.Edit_Job',args=(job.id,) ))

	return render(request, 'edit_job.html', {'job_form':job_form,'job':job})
