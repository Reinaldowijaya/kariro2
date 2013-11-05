from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
		if request.user.get_profile().type() == "A":
			path = "/"
		elif request.user.get_profile().type() == "C":
			path = "/company/dashboard/"
		else:
			path = "/"
		return path