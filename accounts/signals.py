from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Customer


def customer_profile(sender, instance, created, **kwargs):
	if created:
        # Whenever someone makes a new account, he by default, goes in the "customer" group.
		group = Group.objects.get(name='customer')
		instance.groups.add(group)
        # When a new user creates a account, his name is automatically registered as a customer.
		Customer.objects.create(
			user=instance,
			name=instance.username,
			)
		print('Profile created!')

post_save.connect(customer_profile, sender=User)
