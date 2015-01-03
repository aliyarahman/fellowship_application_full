# Import resources
import urlparse
import string
import random
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from app.models import Applicant, Evaluator, Recommender, Staff, Recommendation, Evaluation
from app.forms import ForgotPasswordForm, ResetPasswordForm, CreateAccountForm, ProfileForm, TechForm, ShortAnswersForm, RecommendersForm, ChangeRecommenderForm, RecommendationForm, EvaluationForm, AssignEvaluatorForm


# Section I: Views for all users
# ==============================

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'logged_out.html')


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            new_password = generate_password()
            user.set_password(new_password)
            user.save()
            # Send email
            return HttpResponseRedirect(reverse('login_view'))
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form':form})


def generate_password():
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return password


@login_required
def reset_password(request, user_id):
    user = User.objects.get(id = user_id)
    if request.method == "POST":
        form = ResetPasswordForm(data=request.POST)
        form.validate_email()
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            user.set_password(new_password)
            user.save()
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'user':user, 'form':form})


def faq(request):
    return render(request, 'faq.html')


@login_required
def index(request):
    try:
        if request.user.applicant:
            return HttpResponseRedirect(reverse('createprofile'))
    except:
        pass
    try:
        if request.user.recommender:
            return HttpResponseRedirect(reverse('rec_index'))
    except:
        pass
    try:
        if request.user.evaluator:
            return HttpResponseRedirect(reverse('eval_index'))
    except:
        pass
    try:
        if request.user.staff:
            return HttpResponseRedirect(reverse('staff_index_applicants'))
    except:
        pass



# Section II: Views for Applicant functionality
# =============================================

def createaccount(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('profile'))
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            email = username
            user = User.objects.create_user(username, email, password)
            user.first_name = form.cleaned_data.get('first_names')
            user.last_name = form.cleaned_data.get('last_names')
            user.save()
            applicant = Applicant(user = user, role = 1)
            applicant.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = CreateAccountForm()
    return render(request, 'create_account.html', {'form':form})

#@login_required
def profile(request):
    user = User.objects.get(id = request.user.id)
    applicant = user.applicant
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_names')
            user.last_name = form.cleaned_data.get('last_names')
            user.email = form.cleaned_data.get('email')
            user.save()
            applicant.city = form.cleaned_data.get('city')
            applicant.state = form.cleaned_data.get('state')
            applicant.country = form.cleaned_data.get('country')
            applicant.zipcode = form.cleaned_data.get('zipcode')
            applicant.phone = form.cleaned_data.get('phone')
            applicant.dob = form.cleaned_data.get('dob')
            applicant.pastapplicant = form.cleaned_data.get('pastapplicant')
            applicant.referral = form.cleaned_data.get('referral')
            return HttpResponseRedirect(reverse('tech'))
    else:
        userinfo = model_to_dict(user)
        applicationinfo = model_to_dict(applicant)
        allinfo = dict(userinfo.items() + applicationinfo.items())
        form = ProfileForm(initial=allinfo)
    return render(request, 'profile.html', {'form':form})


@login_required
def tech(request):
    if request.method == 'POST':
        form = TechForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id = request.user.id)
            applicant = user.applicant
            applicant.tech1 = form.clean.get('tech1')
            applicant.tech2 = form.clean.get('tech2')
            applicant.tech3 = form.clean.get('tech3')
            applicant.save()
            return HttpResponseRedirect(reverse('shortanswers'))
    else:
        user = User.objects.get(id = request.user.id)
        applicant = user.applicant
        techinfo = model_to_dict(applicant)
        form = TechForm(initial=techinfo)
    return render(request, 'tech.html', {'form':form})


@login_required
def shortanswers(request):
    if request.method == 'POST':
        form = ShortAnswersForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id = request.user.id)
            applicant = user.applicant
            applicant.shortanswer1 = form.cleaned_data.get('shortanswer1')
            applicant.shortanswer2 = form.cleaned_data.get('shortanswer2')
            applicant.shortanswer3 = form.cleaned_data.get('shortanswer3')
            applicant.shortanswer4 = form.cleaned_data.get('shortanswer4')
            applicant.shortanswer5 = form.cleaned_data.get('shortanswer5')
            applicant.shortanswer6 = form.cleaned_data.get('shortanswer6')
            applicant.shortanswer7 = form.cleaned_data.get('shortanswer7')
            applicant.shortanswer8 = form.cleaned_data.get('shortanswer8')
            applicant.anything_else = form.cleaned_data.get('anythingelse')
            applicant.save()
            return HttpResponseRedirect(reverse('recommenders'))
    else:
        user = User.objects.get(id = request.user.id)
        applicant = user.applicant
        essayinfo = model_to_dict(applicant)
        form = ShortAnswersForm(initial=essayinfo)
    return render(request, 'shortanswers.html', {'form':form})


@login_required
def recommenders(request):
    if request.method == 'POST':
        form = RecommendersForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id = request.user.id)
            applicant = user.applicant
            applicant.ref1firstname = form.cleaned_data.get('ref1firstname')
            applicant.ref1lastname = form.cleaned_data.get('ref1lastname')
            applicant.ref1email = form.cleaned_data.get('ref1email')
            applicant.ref1relationship = form.cleaned_data.get('ref1relationship')
            applicant.ref2firstname = form.cleaned_data.get('ref2firstname')
            applicant.ref2lastname = form.cleaned_data.get('ref2lastname')
            applicant.ref2email = form.cleaned_data.get('ref2email')
            applicant.ref2relationship = form.cleaned_data.get('ref2relationship')
            applicant.ref3firstname = form.cleaned_data.get('ref3firstname')
            applicant.ref3lastname = form.cleaned_data.get('ref3lastname')
            applicant.ref3email = form.cleaned_data.get('ref3email')
            applicant.ref3relationship = form.cleaned_data.get('ref3relationship')
            applicant.save()
            return HttpResponseRedirect(reverse('finalsubmission'))
    else:
        user = User.objects.get(id = request.user.id)
        applicant = user.applicant
        recommenderinfo = model_to_dict(applicant)
        form = RecommendersForm(initial=recommenderinfo)
    return render(request, 'recommenders.html', {'form':form})

@login_required
def finalsubmission(request):
    user = User.objects.get(id = request.user.id)
    return render(request, 'finalsubmission.html')

@login_required
def received(request):
    user = User.objects.get(id = request.user.id)
    add_recommender(user.applicant.ref1email, user.applicant.ref1firstname, user.applicant.ref1lastname, user.applicant.ref1relationship, applicant)
    add_recommender(user.applicant.ref2email, user.applicant.ref2firstname, user.applicant.ref2lastname, user.applicant.ref2relationship, applicant)
    add_recommender(user.applicant.ref3email, user.applicant.ref3firstname, user.applicant.ref3lastname, user.applicant.ref3relationship, applicant)
    logout(request)
    return render(request, 'received.html')


def add_recommender(email, first_name, last_name, relationship, applicant):
    recommender = User.objects.filter(email = email).first()
    if not recommender:
        recommender = User(username = email, first_name = first_name, last_name = last_name, email = email, password = generate_password())
        recommender.save()
    r = Recommender(user = recommender, role=2, relationship=relationship)
    r.save()
    r.applicants.add(applicant)
    recommendation = Recommendation(applicant = applicant, recommender = r)
    recommendation.save()


@login_required
def my_recommenders(request, recommender):
    user = User.objects.get(id = request.user.id)
    if request.method == "POST":
        form = ChangeRecommenderForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('ref_first_name')
            last_name = form.cleaned_data.get('ref_last_name')
            email = form.cleaned_data.get('ref_email')
            relationship = form.cleaned_data.get('ref_relationship')
            add_recommender(email, first_name, last_name, relationship, user.applicant)
            recommender.delete()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ChangeRecommenderForm()
    return render(request, "my_recommenders.html", form = form, recommender = recommender)




# Section III: Views for recommender functionality
# ================================================

@login_required
def rec_index(request):
    user = User.objects.get(id = request.user.id)
    recommender = user.recommender
    recommendations = recommender.recommendation_set.all()
    return render(request, 'rec_index.html', {'recommendations':recommendations})


@login_required
def recommend(request, recommendation_id):#pass in the student this is for
    recommendation = Recommendation.objects.get(id = recommendation_id) #look up the recommendation that is for
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommendation.known_applicant = form.cleaned_data.get('KnownApplicant')
            recommendation.problem_solving_rating = form.cleaned_data.get('problem_solving_rating')
            recommendation.problem_solving = form.cleaned_data.get('problem_solving')
            recommendation.obstacles_rating = form.cleaned_data.get('obstacles_rating')
            recommendation.obstacles = form.cleaned_data.get('obstacles')
            recommendation.community_rating = form.cleaned_data.get('community_rating')
            recommendation.community = form.cleaned_data.get('community')
            recommendation.accomodations_rating = form.cleaned_data.get('accomodations_rating')
            recommendation.accomodations = form.cleaned_data.get('accomodations')
            recommendation.anything_else = form.cleaned_data.get('anything_else')
            recommendation.save()
            return HttpResponseRedirect(reverse('rec_index'))
    else:
        recommendationinfo = model_to_dict(recommendation)
        form = RecommenderForm(initial=recommendationinfo)
    return render(request, 'recommendation.html', {'form':form})



# Section IV: Views for evaluator funtionality
# ============================================

@login_required
def eval_index(request):
    user = User.objects.get(id = request.user.id)
    evaluator = user.evaluator
    evaluations = evaluator.evaluation_set.all()
    return render(request, 'eval_index.html', {'evaluations': evaluations})


@login_required
def evaluate(request, evaluation_id):#pass in the student this is for
    evaluation = Evaluation.objects.get(id = evaluation_id)
    applicant = evaluation.applicant
    recommendations = applicant.recommendation_set.all() 
    if request.method == 'POST':
        form = EvaluatorForm(request.POST)
        if form.is_valid():
            evaluation.criteria_1_rating = form.cleaned_data.get('criteria1rating')
            evaluation.criteria_2_rating = form.cleaned_data.get('criteria2rating')
            evaluation.criteria_3_rating = form.cleaned_data.get('criteria3rating')
            evaluation.criteria_4_rating = form.cleaned_data.get('criteria4rating')
            evaluation.criteria_5_rating = form.cleaned_data.get('criteria5rating')
            evaluation.notes = form.cleaned_data.get('notes')
            evaluation.recommend = form.cleaned_data.get('recommend')
            evaluation.save()
            return HttpResponseRedirect(reverse('eval_index'))
    else:
        evaluationinfo = model_to_dict(evaluation)
        form = EvaluatorForm(initial=evaluationinfo)
    return render(request, 'evaluate.html', {'applicant': applicant, 'form':form, 'recommendations': recommendations})





# Section V: Views for staff functionality
# ========================================

@login_required
def staff_index_applicants(request):
    applicants = Applicant.objects.all()
    return render(request, "staff_index_applicants.html", {'applicants':applicants})


@login_required
def staff_index_evaluators(request):
    evaluators = Evaluator.objects.all()
    return render(request, "staff_index_evaluators.html", {'evaluators':evaluators})


@login_required
def staff_index_recommenders(request):
    recommenders = Recommender.objects.all()
    return render(request, "staff_index_recommenders.html", {'recommenders':recommenders})


@login_required
def staff_index_staff(request):
    staff = Staff.objects.all()
    return render(request, "staff_index_staff.html", {'staff':staff})


@login_required
def assign_evaluator(request, applicant_id):
    applicant = Applicant.objects.get(id = applicant_id)
    evaluators = Evaluator.objects.all()
    return render(request, "assign_evaluator.html", {'applicant': applicant, 'evaluators':evaluators})
#### Need to update this functionality to actually add the evaluator whose button is pressed ###
    #if request.method == 'POST':
        #e_id = form.cleaned_data.get('evaluator')
        #e = Evaluator.objects.get(id = e)
        #Recommendation(applicant=applicant, evaluator = e)
        #recommendation.save()