from django import forms
from django.forms import CharField, Form, PasswordInput, IntegerField, ChoiceField, BooleanField, FileField, Textarea, RadioSelect, EmailField, DateField, FileField
from django.contrib.auth.models import User
from app.models import User, Applicant, Recommender, Recommendation, Evaluation
from django.forms.extras.widgets import SelectDateWidget
from django_countries.fields import CountryField
from django_countries import countries


# Adds the 'Select' placeholder to fields using countries
places = ()
select = ('','Select...')
places +=select,
for c in countries:
    places +=c,


class CreateAccountForm(Form):
    first_name = CharField(required=True, max_length=45)
    last_name = CharField(required=True, max_length=45)
    email = EmailField(required=True, max_length=45)
    password = CharField(widget=PasswordInput(), required=True, max_length=45)
    retype_password = CharField(widget=PasswordInput(), required=True, max_length=45)

    def clean_password(self):
        if self.data['password'] != self.data['retype_password']:
            raise forms.ValidationError("The two passwords you typed don't quite match!")
        if len(self.data['password'])<8:
            raise forms.ValidationError("Please enter a password that's at least 8 characters long.")
        return self.data['password']

    def clean_email(self):
        email = self.data['email']
        user = User.objects.filter(username = email).first()
        recommender = Recommender.objects.filter(user = user).first()
        applicant = Applicant.objects.filter(user = user).first()
        if recommender:
            raise forms.ValidationError("This email address is already associated with a recommender's account. We ask that applicants do not also serve as recommenders for the same calendar year.")
        if applicant:
            raise forms.ValidationError("We already have an account registered for this email address!") 
        return self.data['email']



class ProfileForm(Form):
    first_name = CharField(required=True, max_length=45)
    last_name = CharField(required=True, max_length=45)
    city = CharField(required=False, max_length=45)
    state = CharField(required=False, max_length=45)
    country = ChoiceField(required=False, choices=places)
    zipcode = CharField(required=False, max_length=10)
    dob = CharField(required=False, max_length=15)
    phone = CharField(required=False, max_length=15)
    languages = CharField(required=False, widget=forms.Textarea)
    communities = CharField(required=False, widget=forms.Textarea)
    working_now = CharField(required=False, widget=forms.Textarea)
    school_now = CharField(required=False, widget=forms.Textarea)
    time_commitment = CharField(required=False, widget=forms.Textarea)
    past_applicant = ChoiceField(choices=(('0','Select...'),('1', 'No'),('2', 'Yes')), required=False)
    referral = CharField(required=False, widget=forms.Textarea)



class TechForm(Form):
    tech1b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech2b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech3b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech4b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech5b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech6b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech7b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech8b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech9b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech10b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech11b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech12b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech13b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech14b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech15b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech16b = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech1s = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech2s = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech3s = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech1c = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech2c = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech3c = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech4c = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech5c = ChoiceField(required=False, choices=(('','Select...'),('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))


class ShortAnswersForm(Form):
    shortanswer1 = CharField(widget=Textarea(), required=False)
    shortanswer2 = CharField(widget=Textarea(), required=False)
    shortanswer3 = CharField(widget=Textarea(), required=False)
    shortanswer4 = CharField(widget=Textarea(), required=False)
    shortanswer5 = CharField(widget=Textarea(), required=False)
    shortanswer6 = CharField(widget=Textarea(), required=False)
    shortanswer7 = CharField(widget=Textarea(), required=False)
    shortanswer8 = CharField(widget=Textarea(), required=False)
    shortanswer9 = CharField(widget=Textarea(), required=False)
    shortanswer10 = CharField(widget=Textarea(), required=False)
    shortanswer11 = CharField(widget=Textarea(), required=False)
    shortanswer12 = CharField(widget=Textarea(), required=False)
    shortanswer13 = CharField(widget=Textarea(), required=False)
    anything_else = CharField(widget=Textarea(), required=False)


class RecommendersForm(Form):
    rec1firstname = CharField(required=False, max_length=45)
    rec1lastname = CharField(required=False, max_length=45)
    rec1email = EmailField(required=False, max_length=45)
    rec1relationship = CharField(max_length=140, required=False)
    rec2firstname = CharField(required=False, max_length=45)
    rec2lastname = CharField(required=False, max_length=45)
    rec2email = EmailField(required=False, max_length=45)
    rec2relationship = CharField(max_length=140, required=False)
    rec3firstname = CharField(required=False, max_length=45)
    rec3lastname = CharField(required=False, max_length=45)
    rec3email = EmailField(required=False, max_length=45)
    rec3relationship = CharField(max_length=140, required=False)

    def clean_rec1email(self):
        if self.data['rec1email'] == self.data['rec2email'] or self.data['rec1email'] == self.data['rec3email']:
            raise forms.ValidationError("Please give us a different email address for each recommender.")
        user = User.objects.filter(email = self.data['rec1email']).first()
        applicant = Applicant.objects.filter(user = user).first()
        if applicant:
            raise forms.ValidationError("This email address is already associated with an applicant's account. We ask that applicants do not serve as recommenders for the fellowship application.")
        return self.data['rec1email']


    def clean_rec2email(self):
        if self.data['rec2email'] == self.data['rec3email']:
            raise forms.ValidationError("Please give us a different email address for each recommender.")
        user = User.objects.filter(email = self.data['rec2email']).first()
        applicant = Applicant.objects.filter(user = user).first()
        if applicant:
            raise forms.ValidationError("This email address is already associated with an applicant's account. We ask that applicants do not serve as recommenders for the fellowship application.")
        return self.data['rec2email']


    def clean_rec3email(self):
        user = User.objects.filter(email = self.data['rec3email']).first()
        applicant = Applicant.objects.filter(user = user).first()
        if applicant:
            raise forms.ValidationError("This email address is already associated with an applicant's account. We ask that applicants do not serve as recommenders for the fellowship application.")
        return self.data['rec3email']



class RecommendationForm(Form):
    known_applicant = CharField(widget=Textarea(), required=False)
    commitment_to_justice_rating = ChoiceField(choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    commitment_to_justice = CharField(widget=Textarea(), required=False)
    problem_solving_rating = ChoiceField(choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    problem_solving = CharField(widget=Textarea(), required=False)
    obstacles_rating = ChoiceField(choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    obstacles = CharField(widget=Textarea(), required=False)
    teaching_rating = ChoiceField(choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    teaching = CharField(widget=Textarea(), required=False)
    curiosity_rating = ChoiceField(choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    curiosity = CharField(widget=Textarea(), required=False)
    help_rating = ChoiceField(choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    help = CharField(widget=Textarea(), required=False)
    accommodations = CharField(widget=Textarea(), required=False)
    support = CharField(widget=Textarea(), required=False)
    anything_else = CharField(widget=Textarea(), required=False)


class EvaluationForm(Form):
    criteria_1_rating = ChoiceField(widget=RadioSelect, choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    criteria_2_rating = ChoiceField(widget=RadioSelect, choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    criteria_3_rating = ChoiceField(widget=RadioSelect, choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    criteria_4_rating = ChoiceField(widget=RadioSelect, choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    criteria_5_rating = ChoiceField(widget=RadioSelect, choices=(('','Select...'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    notes = CharField(required=False, widget=Textarea())
    recommend = ChoiceField(choices=(('','Select...'),('1', 'No'),('2', 'Yes')), required=True)


class EditRecommenderForm(Form):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = EmailField(required=True)
    relationship = CharField(required=True)


class ForgotPasswordForm(Form):
    email = EmailField(required=True)


class ResetPasswordForm(Form):
    password = CharField(widget=PasswordInput(), required=True)
    password_confirmation = CharField(widget=PasswordInput(), required=True)

    def clean_password(self):
        if self.data['password'] != self.data['password_confirmation']:
            raise forms.ValidationError("The two passwords you typed don't quite match!")
        if len(self.data['password'])<8:
            raise forms.ValidationError("Please enter a password that's at least 8 characters long.")
        return self.data['password']



class AssignEvaluatorForm(Form):
    evaluator_email = EmailField(required=True)
