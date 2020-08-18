from django.http import HttpResponse
from django.shortcuts import redirect


'''
This decorator restricts the logged in users from going to the register and the login page.
'''
def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


'''
This decorator restricts the customers from viewing the "dashboard" and "products" page.
'''
def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator


'''
Because our dashboard is set to the home URL, whenever a user logged in as a customer tries to go back
or refreshes the page, he is sent to that dashboard from which they are restricted. So, this decorator
is not an ideal way to fix this but a quick duct tape fix.
'''
def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user-page')

		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function
