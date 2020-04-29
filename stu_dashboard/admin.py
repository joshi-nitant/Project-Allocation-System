from django.contrib import admin
from stu_dashboard.models import Student,Project,Project_Rules,Subject,Teaches,Team,Team_Student,TeamPreference,AllocatedProject
from django.contrib.admin import AdminSite
# Register your models here.

class MyAdminSite(AdminSite):
    site_title = 'CE DEPARTMENT'
    site_header= 'Administration'
    index_title= 'CE DEPARTMENT'

myadminSite = MyAdminSite();
class StudentAdmin(admin.ModelAdmin):
    list_display = ('Name','sem','div','batch','cpi','rank')
    list_editable = ('sem','div','batch','cpi','rank')

class AllocatedProjectAdmin(admin.ModelAdmin):
    list_display = ('project','team')
    #list_editable = ('project','team')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('Leader','Subject')

class Team_StudentAdmin(admin.ModelAdmin):
    list_display = ('Student','Team')

class TeamPreferenceAdmin(admin.ModelAdmin):
    list_display = ('Team','project','prefernce')
    list_editable = ('project','prefernce')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','description','is_allocated','is_admin','sub_id','rule_id')
    list_editable = ('is_allocated','is_admin','rule_id')

class ProjectRuleAdmin(admin.ModelAdmin):
    list_display = ('min_team','max_team','is_cross_batch','is_cross_divsion','last_date')
    #list_editable = ('is_allocated','is_admin','rule_id')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name','sem')
    #list_editable = ('is_allocated','is_admin','rule_id')

admin.site.register(Student,StudentAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Project_Rules,ProjectRuleAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Teaches)
admin.site.register(Team,TeamAdmin)
admin.site.register(Team_Student,Team_StudentAdmin)
admin.site.register(TeamPreference,TeamPreferenceAdmin)
admin.site.register(AllocatedProject, AllocatedProjectAdmin)
