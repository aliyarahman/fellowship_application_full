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
from app.forms import ForgotPasswordForm, ResetPasswordForm, CreateAccountForm, ProfileForm, TechForm, ShortAnswersForm, RecommendersForm, EditRecommenderForm, ChangeRecommenderForm, RecommendationForm, EvaluationForm, AssignEvaluatorForm
from django.core.mail import send_mail


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


def logout_view(request):
    logout(request)
    return render(request, 'logged_out.html')


def forgot_password(request):
    if user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        form = ForgotPasswordForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email = email).first()
            if user:
                new_password = generate_password()
                user.set_password(new_password)
                user.save()
                message_text = "Your Code for Progress application portal password has been reset. Please go to http://apply.codeforprogress.org and use the following information to log in. You can change your password once you've successfully logged in using your temporary password.\n\n\tUsername: "+email+"\n\tPassword: "+new_password+"\n\nThe Code for Progress team"
                send_mail('Your temporary password', message_text, 'Code for Progress', [email], fail_silently=False)
            return HttpResponseRedirect(reverse('forgot_password_confirmation'))
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form':form})


def forgot_password_confirmation(request):
    if user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'forgot_password_confirmation.html')


def generate_password():
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return password


@login_required
def reset_password(request):
    user = User.objects.get(id = request.user.id)
    if request.method == "POST":
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            user.set_password(new_password)
            user.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form':form})


def faq(request):
    return render(request, 'faq.html')


@login_required
def index(request):
    try:
        if request.user.applicant:
            return HttpResponseRedirect(reverse('applicant_index'))
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
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            applicant = Applicant(user = user, role = 1)
            applicant.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = CreateAccountForm()
    return render(request, 'create_account.html', {'form':form})


@login_required
def applicant_index(request):
    user = User.objects.get(id = request.user.id)
    try:
        applicant = user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'applicant_index.html', {'user': user})


@login_required
def applicant_index_complete(request):
    user = User.objects.get(id = request.user.id)
    try:
        applicant = user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
    if not applicant.application_complete():
        return HttpResponseRedirect(reverse('applicant_index'))
    return render(request, 'applicant_index_complete.html', {'user': user})


@login_required
def profile(request):
    user = User.objects.get(id = request.user.id)
    try:
        user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
    applicant = user.applicant
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            applicant.city = form.cleaned_data.get('city')
            applicant.state = form.cleaned_data.get('state')
            applicant.country = form.cleaned_data.get('country')
            applicant.zipcode = form.cleaned_data.get('zipcode')
            applicant.phone = form.cleaned_data.get('phone')
            applicant.dob = form.cleaned_data.get('dob')
            applicant.languages = form.cleaned_data.get('languages')
            applicant.communities = form.cleaned_data.get('communities')
            applicant.working_now = form.cleaned_data.get('working_now')
            applicant.school_now = form.cleaned_data.get('school_now')
            applicant.time_commitment = form.cleaned_data.get('time_commitment')
            applicant.past_applicant = form.cleaned_data.get('past_applicant')
            applicant.referral = form.cleaned_data.get('referral')
            applicant.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        userinfo = model_to_dict(user)
        applicationinfo = model_to_dict(applicant)
        allinfo = dict(userinfo.items() + applicationinfo.items())
        form = ProfileForm(initial=allinfo)
    return render(request, 'profile.html', {'form':form})


@login_required
def tech(request):
    try:
        request.user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = TechForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id = request.user.id)
            applicant = user.applicant
            applicant.tech1b = form.cleaned_data.get('tech1b')
            applicant.tech2b = form.cleaned_data.get('tech2b')
            applicant.tech3b = form.cleaned_data.get('tech3b')
            applicant.tech4b = form.cleaned_data.get('tech4b')
            applicant.tech5b = form.cleaned_data.get('tech5b')
            applicant.tech6b = form.cleaned_data.get('tech6b')
            applicant.tech7b = form.cleaned_data.get('tech7b')
            applicant.tech8b = form.cleaned_data.get('tech8b')
            applicant.tech9b = form.cleaned_data.get('tech9b')
            applicant.tech10b = form.cleaned_data.get('tech10b')
            applicant.tech11b = form.cleaned_data.get('tech11b')
            applicant.tech12b = form.cleaned_data.get('tech12b')
            applicant.tech13b = form.cleaned_data.get('tech13b')
            applicant.tech14b = form.cleaned_data.get('tech14b')
            applicant.tech15b = form.cleaned_data.get('tech15b')
            applicant.tech16b = form.cleaned_data.get('tech16b')
            applicant.tech1s = form.cleaned_data.get('tech1s')
            applicant.tech2s = form.cleaned_data.get('tech2s')
            applicant.tech3s = form.cleaned_data.get('tech3s')
            applicant.tech1c = form.cleaned_data.get('tech1c')
            applicant.tech2c = form.cleaned_data.get('tech2c')
            applicant.tech3c = form.cleaned_data.get('tech3c')
            applicant.tech4c = form.cleaned_data.get('tech4c')
            applicant.tech5c = form.cleaned_data.get('tech5c')

            applicant.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        user = User.objects.get(id = request.user.id)
        applicant = user.applicant
        techinfo = model_to_dict(applicant)
        form = TechForm(initial=techinfo)
    return render(request, 'tech.html', {'form':form})


@login_required
def shortanswers(request):
    try:
        request.user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
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
            applicant.shortanswer9 = form.cleaned_data.get('shortanswer9')
            applicant.shortanswer10 = form.cleaned_data.get('shortanswer10')
            applicant.shortanswer11 = form.cleaned_data.get('shortanswer11')
            applicant.shortanswer12 = form.cleaned_data.get('shortanswer12')
            applicant.shortanswer13 = form.cleaned_data.get('shortanswer13')
            applicant.anything_else = form.cleaned_data.get('anything_else')
            applicant.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        user = User.objects.get(id = request.user.id)
        applicant = user.applicant
        essayinfo = model_to_dict(applicant)
        form = ShortAnswersForm(initial=essayinfo)
    return render(request, 'shortanswers.html', {'form':form})


@login_required
def recommenders(request):
    try:
        request.user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = RecommendersForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id = request.user.id)
            applicant = user.applicant
            applicant.rec1firstname = form.cleaned_data.get('rec1firstname')
            applicant.rec1lastname = form.cleaned_data.get('rec1lastname')
            applicant.rec1email = form.cleaned_data.get('rec1email')
            applicant.rec1relationship = form.cleaned_data.get('rec1relationship')
            applicant.rec2firstname = form.cleaned_data.get('rec2firstname')
            applicant.rec2lastname = form.cleaned_data.get('rec2lastname')
            applicant.rec2email = form.cleaned_data.get('rec2email')
            applicant.rec2relationship = form.cleaned_data.get('rec2relationship')
            applicant.rec3firstname = form.cleaned_data.get('rec3firstname')
            applicant.rec3lastname = form.cleaned_data.get('rec3lastname')
            applicant.rec3email = form.cleaned_data.get('rec3email')
            applicant.rec3relationship = form.cleaned_data.get('rec3relationship')
            applicant.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        user = User.objects.get(id = request.user.id)
        applicant = user.applicant
        recommenderinfo = model_to_dict(applicant)
        form = RecommendersForm(initial=recommenderinfo)
    return render(request, 'recommenders.html', {'form':form})


@login_required
def finalsubmission(request):
    try:
        request.user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(id = request.user.id)
    if request.method == "POST":
        user.applicant.application_submitted = 1
        user.applicant.save()
        # send email to recommenders
        # send confirmation email to applicant
        return HttpResponseRedirect(reverse('applicant_index'))
    return render(request, 'finalsubmission.html')


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
def replace_recommender(request, recommender_id):
    try:
        request.user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(id = request.user.id)
    recommender = Recommender.objects.get(id = recommender_id)
    if request.method == "POST":
        form = ChangeRecommenderForm(data=request.POST)
        if form.is_valid():
            recommender.delete()
            new_first_name = form.cleaned_data.get('ref_first_name')
            last_name = form.cleaned_data.get('ref_last_name')
            email = form.cleaned_data.get('ref_email')
            relationship = form.cleaned_data.get('ref_relationship')
            add_recommender(email, first_name, last_name, relationship, user.applicant)
            return HttpResponseRedirect(reverse('applicant_index'))
    else:
        applicant = user.applicant
        applicantinfo = model_to_dict(applicant)
        recommenderinfo = model_to_dict(recommender)
        allinfo = dict(applicantinfo.items() + recommenderinfo.items())
        form = ChangeRecommenderForm(initial=allinfo)
    return render(request, "replace_recommender.html", {'form' : form, 'recommender' : recommender})


def edit_recommender_info(request, recommender_id):
    try:
        request.user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(id = request.user.id)
    recommender = Recommender.objects.get(id = recommender_id)
    if request.method == "POST":
        form = ChangeRecommenderForm(data=request.POST)
        if form.is_valid():
            recommender.user.first_name = form.cleaned_data.get('ref_first_name')
            recommender.user.last_name = form.cleaned_data.get('ref_last_name')
            recommender.user.email = form.cleaned_data.get('ref_email')
            recommender.relationship = form.cleaned_data.get('ref_relationship')
            recommender.save()
            return HttpResponseRedirect(reverse('applicant_index'))
    else:
        recommenderinfo = model_to_dict(recommender)
        form = EditRecommenderForm(initial=recommenderinfo)
    return render(request, "edit_recommender_info.html", {'form': form, 'recommender': recommender})

@login_required
def send_recommender_reminder(request, recommender_id):
    try:
        request.user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(id = request.user.id)
    applicant = user.applicant
    recommender = Recommender.objects.get(id = recommender_id)
    if request.method == "POST":
        pass
        #send_email
    return render(request, "send_recommender_reminder.html")


@login_required
def reminder_sent(request):
    try:
        request.user.applicant
    except:
        return HttpResponseRedirect(reverse('index'))
    return render(request, "reminder_sent.html")



# Section III: Views for recommender functionality
# ================================================

@login_required
def rec_index(request):
    user = User.objects.get(id = request.user.id)
    try:
        user.recommender
    except:
        return HttpResponseRedirect(reverse('index'))
    recommender = user.recommender
    recommendations = recommender.recommendation_set.all()
    return render(request, 'rec_index.html', {'recommender':recommender,'recommendations':recommendations})

@login_required
def submit_recommendation(request, recommendation_id):
    recommendation = Recommendation.objects.get(id = recommendation_id)    
    if request.method == "POST":
        recommendation.submitted = 1
        recommendation.save()
        # Send confirmation email to recommender
        return HttpResponseRedirect(reverse('rec_index'))
    return render(request, 'submit_recommendation.html', {'recommendation':recommendation})

@login_required
def recommend(request, recommendation_id):#pass in the student this is for
    try:
        request.user.recommender
    except:
        return HttpResponseRedirect(reverse('index'))
    recommendation = Recommendation.objects.get(id = recommendation_id) #look up the recommendation that is for
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommendation.known_applicant = form.cleaned_data.get('known_applicant')
            recommendation.commitment_to_justice_rating = form.cleaned_data.get('commitment_to_justice_rating')
            recommendation.commitment_to_justice = form.cleaned_data.get('commitment_to_justice')
            recommendation.problem_solving_rating = form.cleaned_data.get('problem_solving_rating')
            recommendation.problem_solving = form.cleaned_data.get('problem_solving')
            recommendation.obstacles_rating = form.cleaned_data.get('obstacles_rating')
            recommendation.obstacles = form.cleaned_data.get('obstacles')
            recommendation.teaching_rating = form.cleaned_data.get('teaching_rating')
            recommendation.teaching = form.cleaned_data.get('teaching')
            recommendation.community = form.cleaned_data.get('teaching')
            recommendation.curiosity_rating = form.cleaned_data.get('curiosity_rating')
            recommendation.curiosity = form.cleaned_data.get('curiosity')
            recommendation.help_rating = form.cleaned_data.get('help_rating')
            recommendation.help = form.cleaned_data.get('help')
            recommendation.accommodations = form.cleaned_data.get('accommodations')
            recommendation.support = form.cleaned_data.get('support')
            recommendation.anything_else = form.cleaned_data.get('anything_else')
            recommendation.save()
            return HttpResponseRedirect(reverse('rec_index'))
    else:
        recommendationinfo = model_to_dict(recommendation)
        form = RecommendationForm(initial=recommendationinfo)
    return render(request, 'recommendation.html', {'form':form, 'recommendation':recommendation})



# Section IV: Views for evaluator funtionality
# ============================================

@login_required
def eval_index(request):
    try:
        request.user.evaluator
    except:
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(id = request.user.id)
    evaluator = user.evaluator
    evaluations = evaluator.evaluation_set.all()
    return render(request, 'eval_index.html', {'evaluations': evaluations})


@login_required
def evaluate(request, evaluation_id):#pass in the student this is for
    try:
        request.user.evaluator
    except:
        return HttpResponseRedirect(reverse('index'))
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
    try:
        request.user.staff
    except:
        return HttpResponseRedirect(reverse('index'))    
    applicants = Applicant.objects.all()
    return render(request, "staff_index_applicants.html", {'applicants':applicants})


@login_required
def staff_index_evaluators(request):
    try:
        request.user.staff
    except:
        return HttpResponseRedirect(reverse('index'))
    evaluators = Evaluator.objects.all()
    return render(request, "staff_index_evaluators.html", {'evaluators':evaluators})


@login_required
def staff_index_recommenders(request):
    try:
        request.user.staff
    except:
        return HttpResponseRedirect(reverse('index'))
    recommenders = Recommender.objects.all()
    return render(request, "staff_index_recommenders.html", {'recommenders':recommenders})


@login_required
def staff_index_staff(request):
    try:
        request.user.staff
    except:
        return HttpResponseRedirect(reverse('index'))
    staff = Staff.objects.all()
    return render(request, "staff_index_staff.html", {'staff':staff})


@login_required
def assign_evaluator(request, applicant_id):
    try:
        request.user.staff
    except:
        return HttpResponseRedirect(reverse('index'))
    applicant = Applicant.objects.get(id = applicant_id)
    evaluators = Evaluator.objects.all()
    return render(request, "assign_evaluator.html", {'applicant': applicant, 'evaluators':evaluators})