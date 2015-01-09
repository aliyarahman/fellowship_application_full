from app.models import *
from django.contrib.auth.models import User
from app.views import generate_password


# Clear pre-existing users
users = User.objects.all()
users.delete()

# Add applicants
user1 = User(first_name = "Fake", last_name = "Applicant", email = "applicant@fakemail.com", username = "applicant@fakemail.com")
user1.set_password(generate_password())
user1.save()
user1.applicant = 
