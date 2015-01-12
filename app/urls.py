from django.conf.urls import patterns, url, include
from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^forgot_password/$', views.forgot_password, name='forgot_password'),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    url(r'^forgot_password_confirmation/$', views.forgot_password_confirmation, name='forgot_password_confirmation'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^index/$', views.index, name='index'),
    url(r'^applicant_index/$', views.applicant_index, name='applicant_index'),
    url(r'^applicant_index_complete/$', views.applicant_index_complete, name='applicant_index_complete'),
    url(r'^createaccount/$', views.createaccount, name='createaccount'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^tech/$', views.tech, name='tech'),
    url(r'^shortanswers/$', views.shortanswers, name='shortanswers'),
    url(r'^recommenders/$', views.recommenders, name='recommenders'),
    url(r'^finalsubmission/$', views.finalsubmission, name='finalsubmission'),
    url(r'^edit_recommender_info/(?P<recommender_id>\d+)/$', views.edit_recommender_info, name='edit_recommender_info'),
    url(r'^send_recommender_reminder/(?P<recommender_id>\d+)/$', views.send_recommender_reminder, name='send_recommender_reminder'),
    url(r'^reminder_sent/$', views.reminder_sent, name='reminder_sent'),
    url(r'^replace_recommender/(?P<recommender_id>\d+)/$', views.replace_recommender, name='replace_recommender'),
    url(r'^rec_index/$', views.rec_index, name='rec_index'),
    url(r'^recommend/(?P<recommendation_id>\d+)/$', views.recommend, name='recommend'),
    url(r'^submit_recommendation/(?P<recommendation_id>\d+)/$', views.submit_recommendation, name='submit_recommendation'),
    url(r'^eval_index/$', views.eval_index, name='eval_index'),
    url(r'^evaluate/(?P<evaluation_id>\d+)/$', views.evaluate, name='evaluate'),
    url(r'^staff_index_applicants/$', views.staff_index_applicants, name='staff_index_applicants'),
    url(r'^staff_index_evaluators/$', views.staff_index_evaluators, name='staff_index_evaluators'),
    url(r'^staff_index_recommenders/$', views.staff_index_recommenders, name='staff_index_recommenders'),
    url(r'^staff_index_staff/$', views.staff_index_staff, name='staff_index_staff'),
    url(r'^assign_evaluator/(?P<applicant_id>\d+)/$', views.assign_evaluator, name='assign_evaluator'),
)