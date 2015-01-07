from django.db import models
from django.contrib.auth.models import User
import datetime
from django_countries.fields import CountryField


# Django has a built-in User model that works well with the out-of-the-box authentication functions, so we are using it/them.
# That model is created via User.objects.create(username, email, password), and can then also hold first_name and last_name.


class Applicant(models.Model):
    user = models.OneToOneField(User)
    role = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    country = CountryField()
    zipcode = models.CharField(max_length=10)
    dob = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    languages = models.TextField()
    communities = models.TextField()
    working_now = models.TextField()
    school_now = models.TextField()
    time_commitment = models.TextField()
    past_applicant = models.IntegerField(null=True, blank=True)
    referral = models.CharField(max_length=45)

    #  Tech responses
    tech1b = models.IntegerField(null=True, blank=True)
    tech2b = models.IntegerField(null=True, blank=True)
    tech3b = models.IntegerField(null=True, blank=True)
    tech4b = models.IntegerField(null=True, blank=True)
    tech5b = models.IntegerField(null=True, blank=True)
    tech6b = models.IntegerField(null=True, blank=True)
    tech7b = models.IntegerField(null=True, blank=True)
    tech8b = models.IntegerField(null=True, blank=True)
    tech9b = models.IntegerField(null=True, blank=True)
    tech10b = models.IntegerField(null=True, blank=True)
    tech11b = models.IntegerField(null=True, blank=True)
    tech12b = models.IntegerField(null=True, blank=True)
    tech13b = models.IntegerField(null=True, blank=True)
    tech14b = models.IntegerField(null=True, blank=True)
    tech15b = models.IntegerField(null=True, blank=True)
    tech16b = models.IntegerField(null=True, blank=True)
    tech1s = models.IntegerField(null=True, blank=True)
    tech2s = models.IntegerField(null=True, blank=True)
    tech3s = models.IntegerField(null=True, blank=True)
    tech1c = models.IntegerField(null=True, blank=True)
    tech2c = models.IntegerField(null=True, blank=True)
    tech3c = models.IntegerField(null=True, blank=True)
    tech4c = models.IntegerField(null=True, blank=True)
    tech5c = models.IntegerField(null=True, blank=True)


    #  Shortanswer responses
    shortanswer1 = models.TextField()
    shortanswer2 = models.TextField()
    shortanswer3 = models.TextField()
    shortanswer4 = models.TextField()
    shortanswer5 = models.TextField()
    shortanswer6 = models.TextField()
    shortanswer7 = models.TextField()
    shortanswer8 = models.TextField()
    shortanswer9 = models.TextField()
    shortanswer10 = models.TextField()
    shortanswer11 = models.TextField()
    shortanswer12 = models.TextField()
    shortanswer13 = models.TextField()
    shortanswer14 = models.TextField()
    anything_else = models.TextField()

    # Recommender info
    rec1firstname = models.CharField(max_length=45)
    rec1lastname = models.CharField(max_length=45)
    rec1email = models.CharField(max_length=45)
    rec1relationship = models.CharField(max_length=140)
    rec2firstname = models.CharField(max_length=45)
    rec2lastname = models.CharField(max_length=45)
    rec2email = models.CharField(max_length=45)
    rec2relationship = models.CharField(max_length=140)
    rec3firstname = models.CharField(max_length=45)
    rec3lastname = models.CharField(max_length=45)
    rec3email = models.CharField(max_length=45)
    rec3relationship = models.CharField(max_length=140)

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())

    def is_authenticated(self):
        return True

    def __unicode__(self):
        return self.user.email

    def profile_complete(self):
        if self.referral:
            return True

    def tech_questions_complete(self):
        if self.tech1b:
            return True

    def short_answers_complete(self):
        if self.shortanswer1:
            return True

    def recommenders_complete(self):
        if self.rec1email:
            return True

    def application_complete(self):
        if self.profile_complete and self.tech_questions_complete and self.short_answers_complete and self.recommenders_complete:
            return True

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



class Staff(models.Model):
    user = models.OneToOneField(User)
    role = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())

    def __unicode__(self):
        return self.user.email