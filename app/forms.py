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
    first_names = CharField(required=True)
    last_names = CharField(required=True)
    email = CharField(required=True)
    password = CharField(widget=PasswordInput(), required=True)
    retype_password = CharField(widget=PasswordInput(), required=True)


class ProfileForm(Form):
    first_names = CharField(required=True)
    last_names = CharField(required=True)    
    email = CharField(required=True)
    city = CharField(required=True)
    state = CharField(required=True)
    country = ChoiceField(required=False, choices=countries)
    zipcode = IntegerField(required=True)
    phone = CharField(required=True)
    dob = CharField(required=True)
    pastapplicant = ChoiceField(choices=(('','Select...'),('1', 'No'),('2', 'Yes')), required=True)
    referral = CharField(required=False, widget=forms.Textarea)
    
    def validate_password(self, field):
        user = self.get_user()

        if not user and self.password.data == '':
            raise ValidationError("Please enter a password")

        # hack to prevent overwrite of password with blank on profile update
        if user and (self.password.data == '' or self.password.data == None):
            self.password.data = user.password
            self.retypepassword.data = user.password

        if self.password.data != self.retypepassword.data:
            raise ValidationError("Your passwords don't match - try retyping them.")

        if len(self.password.data) < 8:
            raise ValidationError("Your password is a little short - pick one that's at least 8 characters long.")



class TechForm(Form):
    tech1 = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
    tech2 = ChoiceField(required=True, choices=(('1', '1'),('2', '2'),('3', '3'),('4', '4'), ('5', '5')))
#    ab540 = ChoiceField(choices=(('','Select...'),('1', 'No'),('2', 'Yes')), required=False)

class ScholarshipForm(Form):
    awardcycle = CharField(required=True)
    plannedcollegename =CharField(required=True)
    plannedcollegecity = CharField(required=True)
    plannedcollegestate = CharField(required=True)
    plannedcollegetype = ChoiceField(choices=(('','Select...'),('1', 'Community College'),('2', 'Four-year College'),('3', 'Graduate School'), ('4', 'Professional/Technical')))
    plannedcommunitycollegelevel = ChoiceField(choices=(('','Select...'),('1', 'Freshman'),('2', 'Sophomore'),('3', '3rd year or more')))
    plannedtraditionalcollegelevel = ChoiceField(choices=(('','Select...'),('1', 'Freshman'),('2', 'Sophomore'),('3', 'Junior'),('4','Senior'),('5','Graduating Senior')))
    plannedmajor = CharField(required=True)
    receivingyear = CharField(required=False)


class DocumentsForm(Form):
    cv_or_resume = FileField(required=False)
    student_mailing_resume = ChoiceField(choices=(('','Select...'),('1', 'No'),('2', 'Yes')), required=False)
    student_emailing_resume = ChoiceField(choices=(('','Select...'),('1', 'No'),('2', 'Yes')), required=False)
    transcript = FileField(required=False)
    student_mailing_transcript = ChoiceField(choices=(('','Select...'),('1', 'No'),('2', 'Yes')), required=False)
    student_emailing_transcript = ChoiceField(choices=(('','Select...'),('1', 'No'),('2', 'Yes')), required=False)
    college_sending_transcript = ChoiceField(choices=(('','Select...'),('1', 'No'),('2', 'Yes')), required=False)

class EssayForm(Form):
    essaytext1 = CharField(widget=Textarea(), required=False)
    essaytext2 = CharField(widget=Textarea(), required=False)


class RecommendersForm(Form):
    ref1firstname = CharField(required=True)
    ref1lastname = CharField(required=True)
    ref1email = CharField(required=True)
    ref1title = CharField(required=True)
    ref1organization = CharField(required=True) 
    ref2firstname = CharField(required=True)
    ref2lastname = CharField(required=True)
    ref2email = CharField(required=True)
    ref2title = CharField(required=True)
    ref2organization = CharField(required=True) 

class RecommendationForm(Form):
    known_applicant = CharField(required=True)
    problem_solving_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    problem_solving = CharField(required=True)
    obstacles_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
    obstacles = CharField(required=True)
    communit_rating = ChoiceField(widget=RadioSelect, choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')), required=False)
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