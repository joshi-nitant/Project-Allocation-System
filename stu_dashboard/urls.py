from django.conf.urls import url
from django.urls import path
from stu_dashboard import views
app_name = 'stu_dashboard'

urlpatterns = [
    url(r'^$',views.SubjectListView.as_view(),name='dashboard'),
    url(r'^projectlist/(?P<subject>[\w]+)/$',views.ProjectListView.as_view(),name='ProjectList'),
    url(r'^team/add/member',views.addTeam,name='AddTeam'),
    url(r'^team/add/',views.StudentListView.as_view(),name='TeamAdd'),
    url(r'^team/delete/(?P<pk>\d+)/$',views.TeamStudentDeleteView.as_view(),name='DeleteMember'),
    url(r'^team/update/leader/(?P<pk>\d+)/$',views.TeamMemberListView.as_view(),name='ChangeLeader'),
    url(r'^team/update/leader/change',views.changeLeader,name="FinalLeader"),
    url(r'^team/update/(?P<pk>\d+)/$',views.StudentListView.as_view(),name='UpdateMember'),
    url(r'^team/',views.TeamListView.as_view(),name='TeamList'),
    url(r'^projectlist/preference/delete/(?P<pk>\d+)/$',views.TeamPreferenceDeleteView.as_view(),name='DeletePreference'),
    url(r'projectlist/preference',views.preferenceList,name='preferencelist'),
    url(r'projectlist/allocated',views.allocated,name='Allocated'),
    url(r'projectlist/create',views.ProjectCreateView.as_view(),name='AddProject'),
]
