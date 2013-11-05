from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
from django.core.urlresolvers import reverse
from django.db.models import ImageField, signals
from django.dispatch import dispatcher
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.shortcuts import redirect
import datetime
import os

import hashlib
def get_company_logo_path(instance, filename):
    return os.path.join("company",str(instance.user.username), filename)
	
class TimeStampedModel (models.Model):
	
	created = models.DateTimeField(
				auto_now_add=True)
	modified = models.DateTimeField( 
				auto_now=True)
	class Meta:
		abstract = True
		
# class Company(TimeStampedModel):
	# user = models.OneToOneField(User)
	# company_name = models.CharField(max_length=100)
	# slug = models.SlugField(blank=True)
	# address = models.CharField(max_length=100)
	# location = models.ForeignKey('Location')
	# contact = models.CharField(max_length=20)
	# description = models.TextField()
	# employee = models.CharField(max_length=10)
	# benefit = models.CharField(max_length=100)
	# bahasa = models.CharField(max_length=100)
	# industry = models.ForeignKey('Industry',blank=True)
	# logo = models.ImageField(upload_to=get_company_logo_path , blank=True)	
	
	# def save(self, *args, **kwargs):
		# if not self.id:
            # # Newly created object, so set slug
			# #testslug = self.company_name + " " + self.company.company_name
			# self.slug = slugify(self.company_name)
		# return super(Company, self).save(*args, **kwargs)
		
	# def get_absolute_url(self): 
		# return reverse('company_detail',None, kwargs={'pk':self.id, 'slug':self.slug})
		
	# def __unicode__(self):
		# return self.company_name

class Job_Vacancy (TimeStampedModel):
	name=models.CharField(max_length = 50)
	id = models.AutoField(primary_key=True)
	slug=models.SlugField(blank=True)
	posted=models.DateField(auto_now_add=True)
	responsibilities = HTMLField()
	salary = models.CharField(max_length = 20)
	job_type = models.ForeignKey('Job_Type')
	company = models.ForeignKey('Company')
	location = models.ForeignKey('Location')
	
	#requirements
	min_age=models.IntegerField(blank = True,null=True)
	max_age=models.IntegerField(blank = True,null=True)
	gender = models.CharField(max_length=1,blank=True,null=True)
	experience = models.IntegerField(blank = True,null=True)
	education_level = models.CharField (max_length = 50,blank = True,null=True)
	prefered_institution = models.ManyToManyField('Institution',blank = True,null=True)
	course = models.ManyToManyField('Course',blank = True,null=True)
	level = models.CharField (max_length = 50,blank = True,null=True)
	ipk = models.DecimalField(max_digits=2,decimal_places=1,blank = True,null=True)
	skill = models.ManyToManyField('Skill',blank = True,null=True)
	language = models.ManyToManyField('Language',blank = True,null=True)
	description = HTMLField()
	
	def __unicode__(self):
		return self.name
	#Create slug
	def save(self, *args, **kwargs):
		if not self.id:
            # Newly created object, so set slug
			testslug = self.name + " " + self.company.company_name
			self.slug = slugify(testslug)
		return super(Job_Vacancy, self).save(*args, **kwargs)
	#Create Url
	def get_absolute_url(self): 
		"""Construct the absolute URL for this Item."""
		return reverse('jobs_detail',None, kwargs={'pk':self.id})
		
def get_applicant_logo_path(instance, filename):
    return os.path.join("applicant",str(instance.user.username), filename)
	

# class Applicant (TimeStampedModel):
	# user = models.OneToOneField(User)
	# birth_date = models.DateField(blank = True,null=True)
	# location = models.ForeignKey('Location',blank = True,null=True)
	# contact = models.IntegerField(max_length=20,blank = True,null=True)
	# expected_salary = models.IntegerField(max_length=20,blank = True,null=True)
	# logo = models.ImageField(upload_to=get_applicant_logo_path , null=True,blank=True)	
	# job_type=models.ManyToManyField('Job_Type',blank = True,null=True)
	# gender = models.CharField(max_length=1,blank=True,null=True)
	
	# #Resume
	# headline = models.CharField(max_length = 100 , blank = True,null=True)
	# summary = models.TextField(blank = True,null=True)
	# skill = models.ManyToManyField('Skill',blank = True,null=True)
	# status = models.TextField(blank = True,null=True)
	# language = models.ManyToManyField('Language',blank = True,null=True)
	# resume_external = models.FileField(upload_to=get_applicant_logo_path , blank=True,null=True)
	# signup=models.BooleanField(default = False)
	
	# def __unicode__(self):
		# return self.user.username
		
	# def done_profile(self):
		# return self.signup

# def create_applicant(sender, instance, created, **kwargs):
    # if created:
       # Applicant.objects.create(user=instance)
# post_save.connect(create_applicant, sender=User)
	
class Achievement (TimeStampedModel):
	applicant = models.ForeignKey(Applicant)
	location = models.ForeignKey('Location')
	description = models.TextField()
	headline = models.CharField(max_length = 50)
	date = models.DateField(help_text="")
	def __unicode__(self):
		return self.headline

class Education(TimeStampedModel):
	applicant = models.ForeignKey(Applicant)
	institution = models.ForeignKey('Institution')
	course = models.ForeignKey('Course')
	level = models.CharField (max_length = 50)
	location = models.ForeignKey('Location')
	description = models.TextField()
	ipk = models.DecimalField(max_digits=2,decimal_places=1,blank = True,null=True)
	ipk_max = models.DecimalField(max_digits=2,decimal_places=1,blank = True,null=True)
	start_date = models.DateField(blank = True,null=True)
	end_date = models.DateField(help_text="Diisi dengan bulan dan tahun kelulusan",blank = True,null=True)
	def __unicode__(self):
		return self.applicant.userprofile.user.username

def get_institution_logo_path(instance, filename):
    return os.path.join("institution",str(instance.institution.name), filename)
	
class Institution(TimeStampedModel):
	name = models.CharField(max_length = 50)
	logo = models.ImageField(upload_to=get_institution_logo_path , null=True,blank=True)	
	def __unicode__(self):
		return self.name
		
class Course(TimeStampedModel):
	name = models.CharField(max_length = 50)
	def __unicode__(self):
		return self.name

class Work_Experience(TimeStampedModel): 
	applicant = models.ForeignKey(Applicant)
	location = models.ForeignKey('Location')
	description = models.TextField()
	company_name = models.ForeignKey('Company',blank = True,null=True)
	position = models.CharField(max_length = 50,blank = True,null=True)
	start_date = models.DateField(blank = True,null=True)
	end_date = models.DateField(help_text="Diisi dengan bulan dan tahun kelulusan",null=True,blank=True)
	present = models.BooleanField(default= False)
	def __unicode__(self):
		return self.company_name
	
class Application (TimeStampedModel):
	id = models.AutoField(primary_key=True)
	applicant = models.ForeignKey('Applicant')
	job_vacancy = models.ForeignKey('Job_Vacancy')
	matching = models.IntegerField(blank=True)
	
	def __unicode__(self):
		return self.applicant.userprofile.user.username
		
	def save(self, *args, **kwargs):
		if not self.id:
			matching = 0
			final = 0
			job = self.job_vacancy
			applicant = self.userprofile.applicant

			if job.min_age and job.max_age:
				age = (datetime.date.today() - applicant.birth_date).days/365
				if job.min_age - 1 <=  age <= job.max_age + 1:
					matching += 20
				final+=20
			else:
				if job.min_age:			
					if job.min_age - 1 <=  age:
						matching += 20
					final+=10
				if job.max_age:
					if age <= job.max_age + 1:
						matching += 20
					final+=10
					
			if job.gender:
				if job.gender == applicant.gender:
					matching += 20
				final+=20
			
			if job.experience:
				experience = (datetime.date.today() - (applicant.work_experience_set.all().order_by('start_date')[0].start_date)).days/365
				if experience >= job.experience - 1:
					matching += 10
				final+=10
			
			if job.education_level:
				
				education = applicant.education_set.all().order_by(-'level')[0]
				if education.level >= job.education_level:
					matching += 50
				final+=50
				
				if job.course:
					education_course = applicant.education.course.values_list('pk', flat = True)
					if job.course.filter(pk__in=education_course).exist():
						matching += 30
					final += 30
				
				if job.ipk:
					if education.ipk >= job.ipk:
						matching += 20
					final += 20
			
			if job.skill:
			
				applicant_skill = applicant.skill.values_list('pk', flat=True)
				matching += job.skill.filter(pk__in=applicant_skill).count() * 5
				final += job.skill.count() *5 
				
			if job.language:
			
				applicant_language = applicant.language.values_list('pk', flat=True)
				matching += job.language.filter(pk__in=applicant_language).count() * 5
				final += job.language.count() *5 
			
			matching = matching*100/final
			self.matching = matching
			
		return super(Application, self).save(*args, **kwargs)
		
class Location(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __unicode__(self):
		return self.name
		
class Job_Type(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __unicode__(self):
		return self.name
		
class Skill(models.Model):
	name = models.CharField(max_length=50,blank=True,null=True)
	def __unicode__(self):
		return self.name
		
class Language(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __unicode__(self):
		return self.name
	
class Industry(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __unicode__(self):
		return self.name
