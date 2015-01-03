from django.db import models
from django.contrib.auth.models import User
import datetime
from django_countries.fields import CountryField


# Django has a built-in User model that works well with the out-of-the-box authentication functions, so we are using it/them.
# That model is created via User.objects.create(username, email, password), and can then also hold first_name and last_name.


class Staff(models.Model):
    user = models.OneToOneField(User)
    role = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())

    def __unicode__(self):
        return self.user.email


class Applicant(models.Model):
    user = models.OneToOneField(User)
    role = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    country = CountryField()
    zipcode = models.CharField(max_length=10)
    dob = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    pastapplicant = models.IntegerField(null=True, blank=True)
    referral = models.CharField(max_length=45)

    #  Tech responses
    tech1 = models.IntegerField(null=True, blank=True)
    tech2 = models.IntegerField(null=True, blank=True)
    tech3 = models.IntegerField(null=True, blank=True)
    
    #  Shortanswer responses
    shortanswer1 = models.TextField()
    shortanswer2 = models.TextField()
    shortanswer3 = models.TextField()
    shortanswer4 = models.TextField()
    shortanswer5 = models.TextField()
    shortanswer6 = models.TextField()
    shortanswer7 = models.TextField()
    shortanswer8 = models.TextField()
    anything_else = models.TextField()

    # Recommender info
    ref1firstname = models.CharField(max_length=45)
    ref1lastname = models.CharField(max_length=45)
    ref1email = models.CharField(max_length=45)
    ref1relationship = models.CharField(max_length=140)
    ref2firstname = models.CharField(max_length=45)
    ref2lastname = models.CharField(max_length=45)
    ref2email = models.CharField(max_length=45)
    ref2relationship = models.CharField(max_length=140)
    ref3firstname = models.CharField(max_length=45)
    ref3lastname = models.CharField(max_length=45)
    ref3email = models.CharField(max_length=45)
    ref3relationship = models.CharField(max_length=140)

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())

    def is_authenticated(self):
        return True

    def __unicode__(self):
        return self.user.email

    def get_id(self):
        return self.id

    def num_evaluators(self):
        evals = self.evaluation_set.all()
        return len(evals)

    def has_evaluations(self):
        evaluations = self.evaluation_set.all()
        return evaluations

    def average_score(self):
        evaluations = self.evaluation_set.all()
        total_score = 0.00
        num_evals = len(evaluations)
        for e in evaluations:
            if e.criteria_1_rating:
                total_score+=(e.criteria_1_rating+e.criteria_2_rating+e.criteria_3_rating+e.criteria_4_rating+e.criteria_5_rating)
        average_long = float(total_score)/float(num_evals)
        return round(average_long,3)


class Recommender(models.Model):
    user = models.OneToOneField(User)
    role = models.IntegerField(null=True, blank=True)
    relationship = models.CharField(max_length=140, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())

    def __unicode__(self):
        return self.user.email

    def has_recommendations(self):
        recommendations = self.recommendation_set.all()
        return recommendations



class Recommendation(models.Model):
    applicant = models.ForeignKey(Applicant)
    recommender = models.ForeignKey(Recommender)
    known_applicant = models.TextField()
    problem_solving_rating = models.IntegerField(default=0)
    problem_solving = models.TextField()
    obstacles_rating = models.IntegerField(default=0)
    obstacles = models.TextField()
    community_rating = models.IntegerField(default=0)
    community = models.TextField()
    accomodations_rating = models.IntegerField(default=0)
    accomodations = models.TextField()
    anything_else = models.TextField()

    def __unicode__(self):
        return "Recommendation " + str(self.id)

    def is_complete(self):
        if self.known_applicant and self.problem_solving_rating and self.obstacles_rating and self.community_rating and self.accomodations_rating:
            return True
        return False


class Evaluator(models.Model):
    user = models.OneToOneField(User)
    role = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())

    def __unicode__(self):
        return self.user.email

    def num_applicants(self):
        evals = self.evaluation_set.all()
        return len(evals)

    def has_evaluations(self):
        evaluations = self.evaluation_set.all()
        return evaluations



class Evaluation(models.Model):
    applicant = models.ForeignKey(Applicant)
    evaluator = models.ForeignKey(Evaluator)
    criteria_1_rating = models.IntegerField(null=True, blank=True)
    criteria_2_rating = models.IntegerField(null=True, blank=True)
    criteria_3_rating = models.IntegerField(null=True, blank=True)
    criteria_4_rating = models.IntegerField(null=True, blank=True)
    criteria_5_rating = models.IntegerField(null=True, blank=True)
    recommend = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def is_complete(self):
        if self.criteria_1_rating:
            return True
        return False

    def __unicode__(self):
        return "Evaluation "+ str(self.id)