from django.shortcuts import render
from django.views.generic import ListView,UpdateView,CreateView,TemplateView,DeleteView
from stu_dashboard.models import Student,Subject,Project_Rules,Project,Team,Team_Student,TeamPreference,AllocatedProject
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import re
from django.db import IntegrityError
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

#########################################
def checkIfLeader(request):
    user_id = request.session['user_id']
    subject_id = request.session['sub_id']

    leader_list = Team.objects.filter(subject_id_id__exact=subject_id)
    is_leader = leader_list.filter(leader_id_id__exact=user_id)
    is_member = Team_Student.objects.filter(student_id_id__exact=user_id).filter(team_id_id__in=leader_list)

    if len(is_leader) or (not len(is_member)):
        return True
    else:
        return False

def checkOnlyLeader(request):
    user_id = request.session['user_id']
    subject_id = request.session['sub_id']

    leader_list = Team.objects.filter(subject_id_id__exact=subject_id)
    if leader_list:
        is_leader = leader_list.filter(leader_id_id__exact=user_id)
        if is_leader:
            return True
        else:
            return False
    else:
        return False

# Create your views here.
class SubjectExistsMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.session.has_key('sub_id'):
            return HttpResponseRedirect(reverse('stu_dashboard:dashboard'))
        else:
            return super().dispatch(request, *args, **kwargs)

class PreferenceValidationMixin:

    def dispatch(self, request, *args, **kwargs):
        subject = Subject.objects.get(sub_id__exact=request.session['sub_id'])
        try:
            team = Team.objects.filter(subject_id_id__exact=request.session['sub_id'])
            user_team = Team_Student.objects.filter(team_id_id__in=team).filter(student_id_id__exact=request.session['user_id']).get()

        except Exception as e:
            messages.error(request,"Sorry you do not belong to any team for this subject")
            return HttpResponseRedirect(reverse('stu_dashboard:ProjectList',kwargs={'subject':subject.name}))

        if not checkIfLeader(request):
            messages.error(request,"Sorry you are not leader of this team")
            return HttpResponseRedirect(reverse('stu_dashboard:ProjectList',kwargs={'subject':subject.name}))

        current_preference = TeamPreference.objects.filter(team_id__exact=user_team.team_id)
        if len(current_preference)==3:
            messages.error(request,"You have already made 3 prefernce for this subject.Go to prefernce for any changes")
            return HttpResponseRedirect(reverse('stu_dashboard:ProjectList',kwargs={'subject':subject.name}))

        return super().dispatch(request, *args, **kwargs)

class LeaderCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        if not checkIfLeader(request):
            return HttpResponseRedirect(reverse('stu_dashboard:TeamList'))
        else:
            return super().dispatch(request, *args, **kwargs)

class OnlyLeaderCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        if not checkOnlyLeader(request):
            return HttpResponseRedirect(reverse('stu_dashboard:preferencelist'))
        else:
            return super().dispatch(request, *args, **kwargs)

class SubjectListView(LoginRequiredMixin,ListView):
    login_url = 'index'
    redirect_field_name = ''
    model = Subject
    context_object_name = 'subject_list'
    template_name = 'stu_dashboard/dashboard.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.has_key('sub_id'):
            del self.request.session['sub_id']
        if self.request.session.has_key('rule_id'):
            del self.request.session['rule_id']
        if self.request.session.has_key('update_student'):
            del self.request.session['update_student']
        user_id = self.request.session['user_id']
        student = Student.objects.get(pk=user_id)
        inner_query = Project.objects.values('sub_id')
        subjects = Subject.objects.filter(sub_id__in=inner_query).filter(sem=student.sem).values('name')
        context['sub_list'] = subjects
        return context

class ProjectListView(LoginRequiredMixin,ListView):
    login_url = 'index'
    redirect_field_name = ''
    model = Project
    context_object_name = 'project_list'
    template_name = 'stu_dashboard/project_list.html'
    subject_name = None
    paginate_by = 2

    def get_queryset(self,**kwargs):
        self.subject_name = self.kwargs['subject']
        return super().get_queryset(**kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        subject_name = self.subject_name.upper()
        subject_id = Subject.objects.filter(name__exact=subject_name).values('sub_id')
        self.request.session['sub_id'] = subject_id[0]['sub_id']
        project_list = Project.objects.filter(sub_id__in=subject_id).filter(is_admin__exact=True)
        project_rule_id = project_list.values('rule_id')[0]
        self.request.session['rule_id'] = project_rule_id['rule_id']
        project_rule = Project_Rules.objects.filter(pr_rule_id__exact=project_rule_id['rule_id'])


        ###########Pagination####################
        paginator = Paginator(project_list, self.paginate_by)
        print(paginator.count )
        page = self.request.GET.get('page')
        print(page)

        try:
            paginate_list = paginator.page(page)
            print("try")
            print(paginate_list.object_list)
        except PageNotAnInteger:
            paginate_list = paginator.page(1)
            print("PageNotAnInteger")
        except EmptyPage:
            print(paginator.num_pages)
            paginate_list = paginator.page(paginator.num_pages)
            print("EmptyPage")
        print(paginate_list.has_next())
        #############

        ##retrive current preferences for this team of this subject
        try:
            team = Team.objects.filter(subject_id_id__exact=self.request.session['sub_id'])
            team_student = Team_Student.objects.filter(team_id_id__in=team).filter(student_id__exact=self.request.session['user_id']).get()
            team_preference = TeamPreference.objects.filter(team_id__exact=team_student.team_id)
            current_preference = 3 - len(team_preference.values('pk'))
            print("Allowed prefernce = "+str(current_preference))
        except Exception as e:
            current_preference = 3
        #####
        print("Allowed prefernce = "+str(current_preference))
        context['allowed_project'] = current_preference
        context['project_rules'] = project_rule
        context['project_list'] = paginate_list

        if page is not None:
            context['current_page'] = (int(page)-1)*self.paginate_by
        else:
            context['current_page'] = 0
        context['page_obj'] = paginate_list
        return context

class TeamListView(LoginRequiredMixin,SubjectExistsMixin,ListView):
    login_url = 'index'
    redirect_field_name = ''
    model = Team
    context_object_name = 'team_list'
    template_name = 'stu_dashboard/team_list.html'


    def get_context_data(self,**kwargs):
        print("Inside team list view")
        context = super().get_context_data(**kwargs)
        user_id = self.request.session['user_id']
        team = Team_Student.objects.filter(student_id__exact=user_id).values('team_id')
        subject_id = Team.objects.filter(id__in=team).filter(subject_id_id__exact=self.request.session['sub_id']).values('subject_id_id','id','leader_id_id','id')
        print(subject_id)
        if len(subject_id)==0:
                msg = 'You do not belong to any team for this subject'
                context['msg'] = msg
        else:
            team_leader = Team_Student.objects.filter(student_id_id__exact=subject_id[0]['leader_id_id']).filter(team_id_id__exact=subject_id[0]['id']).get()
            print(team_leader)
            member_list = Team_Student.objects.filter(team_id_id__exact=subject_id[0]['id']).exclude(student_id_id__exact=subject_id[0]['leader_id_id'])
            context['member_list'] = member_list

            if user_id == subject_id[0]['leader_id_id']:
                is_leader = True
                ###Check For the minimum team memeber to determine whether delete should be enabled or not
                current_member = len(member_list)+1
                project_rule = Project_Rules.objects.get(pk=self.request.session['rule_id'])
                if current_member == project_rule.min_team:
                    disable_delete = True
                else:
                    disable_delete = False

                ##diable add
                if current_member == project_rule.max_team:
                    disable_add = True
                else:
                    disable_add = False
                ##############
                context['disable_delete'] = disable_delete
                context['disable_add'] = disable_add
            else:
                is_leader = False

            context['leader'] = team_leader
            context['is_leader'] = is_leader
        return context

class StudentListView(LoginRequiredMixin,SubjectExistsMixin,LeaderCheckMixin,CreateView):
    login_url = 'index'
    redirect_field_name = ''
    model = Team
    fields = ['leader_id']
    context_object_name = 'student_list'
    template_name = 'stu_dashboard/student_list.html'
    update_pk = None

    def get(self, request, *args, **kwargs):
        print("Inside Student List View")
        print(dir(kwargs))
        if(kwargs.get('pk')):
             self.update_pk = Team_Student.objects.get(pk=kwargs['pk'])
        resp = super().get(request,*args, **kwargs)
        return resp

    def get_context_data(self,**kwargs):
        print("Inside StudentListView get_context_data")
        url_Regex  = re.compile(r'/dashboard/team/update/\d')

        context = super().get_context_data(**kwargs)
        login_student = Student.objects.get(s_id_id=self.request.session['user_id'])

        project_rule = Project_Rules.objects.filter(pr_rule_id__exact=self.request.session['rule_id']).values('is_cross_batch','is_cross_divsion','max_team','min_team')[0]
        print(project_rule)
        ##get all teams of particular subject
        subject_team = Team.objects.filter(subject_id_id__exact=self.request.session['sub_id']).values('id')
        print(subject_team)

        if len(subject_team):
            team_student = Team_Student.objects.filter(team_id_id__in=subject_team).values('student_id_id')
            print(team_student)
            student_list = Student.objects.exclude(s_id_id__in=team_student)
            print(student_list)
        else:
            student_list = Student.objects.all()
        print(student_list)
        if(project_rule['is_cross_batch']):
            remain_student_list = student_list.filter(div__exact=login_student.div)
        elif(project_rule['is_cross_divsion']):
            remain_student_list = student_list.filter(sem__exact=login_student.sem)
        else:
            remain_student_list = student_list.filter(batch__exact=login_student.batch)
        context['min_member'] = project_rule['min_team']-1
        ##update logic
        inner_query = Team.objects.filter(subject_id_id__exact=self.request.session['sub_id']).filter(leader_id_id__exact=self.request.session['user_id']).values('id')
        print(len(inner_query))
        if len(inner_query):
            print(inner_query)
            existing_students = Team_Student.objects.filter(team_id_id__exact=inner_query[0]['id'])
            existing_students = len(existing_students)
        else:
            existing_students = 1
        total_existing_students = existing_students
        print(total_existing_students)
        #update logic
        if url_Regex.search(self.request.path) is not None:
            context['is_update'] = True
            context['update_pk'] = self.update_pk
            self.request.session['update_student'] = self.update_pk.id
            context['max_member'] = 1
        else:
            context['max_member'] = project_rule['max_team']-(total_existing_students-1)-1
        ##end of update logic

        context['leader'] = login_student
        context['student_list'] = remain_student_list
        print(remain_student_list.values('s_id_id'))
        return context

class TeamStudentDeleteView(LoginRequiredMixin,SubjectExistsMixin,LeaderCheckMixin,DeleteView):
    login_url = 'index'
    redirect_field_name = ''
    model = Team_Student


    def delete(self, request, *args, **kwargs):
        delete_student_instance = Team_Student.objects.get(pk=kwargs['pk'])
        print(delete_student_instance.student_id_id)
        team_id = delete_student_instance.team_id_id
        delete_student_instance.delete()
        team_leader = Team.objects.get(pk=team_id)
        print(team_leader.leader_id_id)

        if team_leader.leader_id_id==delete_student_instance.student_id_id:
            #Delete all students of that team
            Team_Student.objects.filter(team_id_id__exact=team_id).delete()
            #Also delete all the prefernce
            TeamPreference.objects.filter(team_id__exact=team_leader.id).delete()
            #Delete Team Leader enetry from Team
            team_leader.delete()
        return HttpResponseRedirect(reverse_lazy('stu_dashboard:TeamList'))

##############To CHANGE LEADER###############
class TeamMemberListView(LoginRequiredMixin,SubjectExistsMixin,LeaderCheckMixin,ListView):
    login_url = 'index'
    redirect_field_name = ''
    model = Team
    context_object_name = 'team_list'
    template_name = 'stu_dashboard/team_leader_change.html'
    team_id = None

    def get(self, request, *args, **kwargs):
        self.team_id = kwargs['pk']
        resp = super().get(request,*args,**kwargs)
        return resp

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        team_member = Team_Student.objects.filter(team_id_id__exact=self.team_id).exclude(student_id_id=self.request.session['user_id'])
        if len(team_member):
            context['team_member'] = team_member
        else:
            context['no_member'] = True
        return context
    # get_context_data(self,**kwargs):
class ProjectCreateView(LoginRequiredMixin,SubjectExistsMixin,PreferenceValidationMixin,CreateView):
    model = Project
    fields = ('title','description')

    def form_valid(self, form):
        form.instance.sub_id_id = self.request.session['sub_id']
        form.instance.is_allocated = False
        form.instance.rule_id_id = self.request.session['rule_id']
        form.instance.created_by = self.request.user
        form.instance.is_admin = False
        form.save()
        team = Team.objects.filter(subject_id_id__exact=self.request.session['sub_id'])
        user_team = Team_Student.objects.filter(team_id_id__in=team).filter(student_id_id__exact=self.request.session['user_id']).get()
        current_preference = TeamPreference.objects.filter(team_id__exact=user_team.team_id)
        if len(current_preference)==0:
            intialPreference = 1
        else:
            seq = [x['prefernce'] for x in current_preference.values('prefernce')]
            intialPreference = max(seq) + 1
        team_preference = TeamPreference(project_id=form.instance.pk,team_id=user_team.team_id_id,prefernce=intialPreference)
        team_preference.save()

        return super().form_valid(form)



@login_required(login_url=reverse_lazy('login:index'),redirect_field_name='') #
def addTeam(request):
    if not checkIfLeader(request):

        HttpResponseRedirect(reverse('stu_dashboard:TeamList'))
    if request.method=='POST':

        ##update logic
        if request.session.has_key('update_student'):
            team_student = Team_Student.objects.get(id=request.session['update_student'])
            new_student = request.POST['team_student[]']
            team_student.student_id_id = new_student
            team_student.save()
            del request.session['update_student']
            #saving leader
        else:
            team_members = request.POST.getlist('team_student[]')
            print(team_members)
            t = Team.objects.filter(subject_id_id__exact=request.session['sub_id']).filter(leader_id_id__exact=request.session['user_id'])
            if not len(t):
                team  = Team(leader_id_id=request.session['user_id'],subject_id_id=request.session['sub_id'])
                team.save()
                t = team
                Team_Student(student_id_id=request.session['user_id'],team_id=team).save()
            else:
                t = t[0]
            #saving team memeber
            for team_member in team_members:
                stu_id = User.objects.get(id=team_member).id
                print(stu_id)
                member = Team_Student(student_id_id=stu_id,team_id=t)
                member.save()
    print("Inside add team function view")
    return HttpResponseRedirect(reverse('stu_dashboard:TeamList'))


class TeamPreferenceDeleteView(LoginRequiredMixin,SubjectExistsMixin,OnlyLeaderCheckMixin,DeleteView):
    login_url = 'index'
    redirect_field_name = ''
    model = TeamPreference
    success_url = reverse_lazy('stu_dashboard:preferencelist')

    def delete(self,request,*args,**kwargs):
        team_preference_delete = TeamPreference.objects.get(pk=kwargs['pk'])
        all_team_preference = TeamPreference.objects.filter(team_id=team_preference_delete.team_id)


        for team_preference in all_team_preference:
            if team_preference.prefernce-team_preference_delete.prefernce > 0:
                team_preference.prefernce = team_preference.prefernce - 1
                team_preference.save()

        project = Project.objects.get(pr_id__exact=team_preference.project_id)

        if project.is_admin == False:
            project.delete()
        team_preference_delete.delete()
        return HttpResponseRedirect(reverse_lazy('stu_dashboard:preferencelist'))


@login_required(redirect_field_name='')#
def changeLeader(request):

    if not checkIfLeader(request):
        HttpResponseRedirect(reverse('stu_dashboard:TeamList'))
    if request.method=='POST':
        new_leader = request.POST['new_leader[]']
        team_student = Team_Student.objects.get(id=new_leader)
        team = Team.objects.get(id=team_student.team_id_id)
        team.leader_id_id = team_student.student_id_id
        team.save()

    return HttpResponseRedirect(reverse('stu_dashboard:TeamList'))

@login_required(redirect_field_name='')
def allocated(request):
    context={}
    if not request.session.has_key('sub_id'):
        return HttpResponseRedirect(reverse('stu_dashboard:dashboard'))

    subject = Subject.objects.get(sub_id__exact=request.session['sub_id'])
    try:
        team = Team.objects.filter(subject_id_id__exact=request.session['sub_id'])
        print(team)
        user_team = Team_Student.objects.filter(team_id_id__in=team).filter(student_id_id__exact=request.session['user_id']).get()
        print(user_team.team_id_id)
        allocated_project = AllocatedProject.objects.filter(team_id__exact=user_team.team_id_id).get()  
        print(allocated_project)
        if(allocated_project):
            print("Here")
            context['project'] = allocated_project

        else:
            context['project'] = None

        print(context['project'])
        return render(request,'stu_dashboard/allocated_project.html',context)

    except Exception as e:
        print(e)
        messages.error(request,"Sorry you do not belong to any team for this subject")
        return HttpResponseRedirect(reverse('stu_dashboard:ProjectList',kwargs={'subject':subject.name}))

@login_required(redirect_field_name='')
def preferenceList(request):
    context = {}
    if not request.session.has_key('sub_id'):
        return HttpResponseRedirect(reverse('stu_dashboard:dashboard'))

    subject = Subject.objects.get(sub_id__exact=request.session['sub_id'])

    try:
        team = Team.objects.filter(subject_id_id__exact=request.session['sub_id'])
        user_team = Team_Student.objects.filter(team_id_id__in=team).filter(student_id_id__exact=request.session['user_id']).get()

    except Exception as e:
        messages.error(request,"Sorry you do not belong to any team for this subject")
        return HttpResponseRedirect(reverse('stu_dashboard:ProjectList',kwargs={'subject':subject.name}))

    if checkOnlyLeader(request):
        is_leader = True
    else:
        is_leader = False


    #####################IF USER HAS CLICKED ON ADD PREFERNCE###########################
    if request.method=='POST':
        ##########CHECK IF USER BELONG TO ANY TEAM###########################
        if not user_team:
            messages.error(request,"Sorry you do not belong to any team for this subject")
            return HttpResponseRedirect(reverse('stu_dashboard:ProjectList',kwargs={'subject':subject.name}))

        ##########CHECK IF USER IS LEADER###########################
        if not checkIfLeader(request):
                messages.error(request,"Sorry you are not leader of this team")
                return HttpResponseRedirect(reverse('stu_dashboard:ProjectList',kwargs={'subject':subject.name}))

        ##########CHECK IF ALREADY 3 PREFERNCE ARE DONE ###########################
        current_preference = TeamPreference.objects.filter(team_id__exact=user_team.team_id)
        if len(current_preference)==3:
            messages.error(request,"You have already made 3 prefernce for this subject.Go to prefernce for any changes")
            return HttpResponseRedirect(reverse('stu_dashboard:ProjectList',kwargs={'subject':subject.name}))

        if len(current_preference)==0:
            intialPreference = 1
        else:
            seq = [x['prefernce'] for x in current_preference.values('prefernce')]
            intialPreference = max(seq) + 1
        project_list = request.POST.getlist('project_list[]')

        try:
            for project in project_list:
                team_preference = TeamPreference(project_id=project,team_id=user_team.team_id_id,prefernce=intialPreference)
                team_preference.save()
                intialPreference = intialPreference + 1
        except IntegrityError as e:
            messages.error(request,"Definition already Added")
            return HttpResponseRedirect(request.POST['next'])
    ##retrive current preferences for this team of this subject
    try:
        team = Team.objects.filter(subject_id_id__exact=request.session['sub_id'])
        print(team)
        team_student = Team_Student.objects.filter(team_id_id__in=team).filter(student_id__exact=request.session['user_id']).get()
        team_preference = TeamPreference.objects.filter(team_id__exact=team_student.team_id_id)
        print(team_preference.values('pk'))
        context['prefernce_list'] = team_preference
        current_preference = len(team_preference.values('pk'))
    except Exception as e:
        current_preference = 0
        ####
    if current_preference==0:
        messages.error(request,"You have not made any prefernce for this subject.")
        return HttpResponseRedirect(reverse('stu_dashboard:ProjectList',kwargs={'subject':subject.name}))

    if current_preference==3:
        disable_add = True
    else:
        disable_add = False

    if current_preference==1:
        disable_delete = True
    else:
        disable_delete = False

    ##get all the prefernce
    context['current_preference'] = current_preference
    context['subject_name'] = subject.name
    context['disable_add'] = disable_add
    context['disable_delete'] = disable_delete
    context['is_leader'] = is_leader

    return render(request,'stu_dashboard/project_preferences.html',context)
