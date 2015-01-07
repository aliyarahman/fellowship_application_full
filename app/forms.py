from django import forms
from django.forms import CharField, Form, PasswordInput, IntegerField, ChoiceField, BooleanField, FileField, Textarea, RadioSelect, EmailField, DateField, FileField
from django.contrib.auth.models import User
from app.models import User, Recommendation, Evaluation
from django.forms.extras.widgets import SelectDateWidget
from django_countries.fields import CountryField
from django_countries import countries


def unique_user(form, field):
     users = User.query.filter_by(email=field.data)
     if users and users.count() > 0:
         raise ValidationError('The email address you provided is already in use.')


class CreateAccountForm(Form):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = CharField(required=True)
    password = CharField(widget=PasswordInput(), required=True)
    retype_password = CharField(widget=PasswordInput(), required=True)


class ProfileForm(Form):
    first_name = CharField(required=True)
    last_name = CharField(required=True)    
    email = CharField(required=True)
    city = CharField(required=True)
    state = CharField(required=True)
    country = ChoiceField(required=False, choices=countries)
    zipcode = CharField(required=True)
    phone = CharField(required=True)
    dob = CharField(required=True)
    languages = CharField(required=False, widget=forms.Textarea)
    communities = CharField(required=False, widget=forms.Textarea)
    working_now = CharField(required=False, widget=forms.Textarea)
    school_now = CharField(required=False, widget=forms.Textarea)
    past_applicant = ChoiceField(choices=(('','Select...'),('1', 'No'),('2', 'Yes')), required=True)
    referral = CharField(required=False, widget=forms.Textarea)
    

class TechForm(Form):
    tech1b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech2b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech3b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech4b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech5b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech6b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech7b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech8b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech9b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech10b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech11b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech12b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech13b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech14b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech15b = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech1s = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech2s = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech3s = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech1c = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech2c = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech3c = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech4c = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech5c = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))


class ShortAnswersForm(Form):
    shortanswer1 = CharField(widget=Textarea(), required=False)
    shortanswer2 = CharField(widget=Textarea(), required=False)
    shortanswer3 = CharField(widget=Textarea(), required=False)
    shortanswer4 = CharField(widget=Textarea(), required=False)
    shortanswer5 = CharField(widget=Textarea(), required=False)
    shortanswer6 = CharField(widget=Textarea(), required=False)
    shortanswer7 = CharField(widget=Textarea(), required=False)
    shortanswer8 = CharField(widget=Textarea(), required=False)
    anything_else = CharField(widget=Textarea(), required=False)


class RecommendersForm(Form):
    rec1firstname = CharField(required=True)
    rec1lastname = CharField(required=True)
    rec1email = CharField(required=True)
    rec1relationship = CharField(required=True)
    rec2firstname = CharField(required=True)
    rec2lastname = CharField(required=True)
    rec2email = CharField(required=True)
    rec2relationship = CharField(required=True)
    rec3firstname = CharField(required=True)
    rec3lastname = CharField(required=True)
    rec3email = CharField(required=True)
    rec3relationship = CharField(required=True)


class RecommendationForm(Form):
    known_applicant = CharField(required=True)
    problem_solving_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    problem_solving = CharField(required=True)
    obstacles_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    obstacles = CharField(required=True)
    community_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    community = CharField(required=True)
    accomodations_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    accomodations = CharField(required=True)
    anything_else = CharField(widget=Textarea(), required=False)


class EvaluationForm(Form):
    criteria_1_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    criteria_2_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    criteria_3_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    criteria_4_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    criteria_5_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    notes = CharField(required=False, widget=Textarea())
    recommend = ChoiceField(choices=(('','Select...'),('1', 'No'),('2', 'Yes')), required=True)


class ChangeRecommenderForm(Form):
    ref_first_name = CharField(required=True)
    ref_last_name = CharField(required=True)
    ref_email = EmailField(required=True)
    ref_relationship = CharField(required=True)


class ForgotPasswordForm(Form):
    email = EmailField(required=True)


class ResetPasswordForm(Form):
    password = CharField(widget=PasswordInput(), required=True)
    password_confirmation = CharField(widget=PasswordInput(), required=True)


class AssignEvaluatorForm(Form):
    evaluator_email = EmailField(required=True)
