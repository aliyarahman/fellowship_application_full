from app.models import *
from django.contrib.auth.models import User
from app.views import generate_password


# Clear pre-existing data
users = User.objects.all()
users.delete()
applicants = Applicant.objects.all()
applicants.delete()
recommenders = Recommender.objects.all()
recommenders.delete()
recommendations = Recommendation.objects.all()
recommendations.delete()

# Add applicant with blank application
user1 = User(first_name = "Fake", last_name = "Applicant", email = "applicant1@fakemail.com", username = "applicant1@fakemail.com")
#user1.set_password(generate_password())
user1.set_password('abc123')
user1.save()
applicant1 = Applicant(role=1, user = user1)
applicant1.save()


# Add recommender
user2 = User(first_name = "Fake", last_name = "Recommender", email = "recommender1@fakemail.com", username = "recommender1@fakemail.com")
user2.set_password('abc123')
user2.save()
recommender1 = Recommender(role=1, user = user2)
recommender1.save()

#Add recommendation to link applicant and recommender
recommendation1 = Recommendation(applicant = applicant1, recommender = recommender1)
recommendation1.save()