from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from login.models import Site_User
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse

#Create your models here.

class Subject(models.Model):
    sub_id = models.AutoField(primary_key=True)
    sem = models.PositiveIntegerField()
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Student(models.Model):
    s_id  = models.OneToOneField(Site_User,on_delete=models.CASCADE,primary_key=True)
    sem = models.IntegerField()
    div = models.CharField(max_length=1)
    batch = models.CharField(max_length=2)
    cpi = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)

    def Name(self):
        return self.s_id.user.first_name +" " +self.s_id.user.last_name

    def __str__(self):
        return self.s_id.user.first_name +" " +self.s_id.user.last_name

class Team(models.Model):
    leader_id = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    subject_id = models.ForeignKey(Subject,on_delete=models.CASCADE)

    class Meta():
        unique_together = ('leader_id_id','subject_id_id')

    def Leader(self):
            return self.leader_id.s_id

    def Subject(self):
                return self.subject_id.name
    def __str__(self):
        return str(self.leader_id)

class Project_Rules(models.Model):
    pr_rule_id = models.AutoField(primary_key=True)
    min_team = models.PositiveIntegerField(validators=[MinValueValidator(2)])
    max_team = models.PositiveIntegerField(validators=[MinValueValidator(2)])
    is_cross_divsion = models.BooleanField(default=False)
    is_cross_batch = models.BooleanField(default=False)
    last_date = models.DateTimeField(default=timezone.now()+timedelta(days=7))

    def __str__(self):
        return "Rule"

class Project(models.Model):
    pr_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    rule_id = models.ForeignKey(Project_Rules,on_delete=models.CASCADE)
    sub_id = models.ForeignKey(Subject,on_delete=models.CASCADE)
    is_allocated = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('stu_dashboard:preferencelist')

    def __str__(self):
        return self.title

class Teaches(models.Model):
    teach_id = models.AutoField(primary_key=True)
    fac_id_id  = models.ForeignKey(Site_User,on_delete=models.CASCADE,related_name='faculty_id')
    sub_id = models.ForeignKey(Subject,on_delete=models.CASCADE)

    def __str__(self):
        return self.fac_id.user.username + " teaches " + self.sub_id.name

class Team_Student(models.Model):
    team_id = models.ForeignKey(Team,on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)


    class Meta:
        unique_together = ('team_id', 'student_id')

    def Team(self):
        return self.team_id

    def Student(self):
            return self.student_id

    def __str__(self):
        return str(self.student_id)

class TeamPreference(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    prefernce = models.PositiveIntegerField(validators=[MaxValueValidator(3)])
    class Meta:
        unique_together = ('team','project')

    def Team(self):
        return self.team

    def Project(self):
        return self.project

    def Priority(self):
        return self.prefernce

    def __str__(self):
        return str(self.project)

class AllocatedProject(models.Model):
    allocated_id = models.AutoField(primary_key=True)
    project =  models.ForeignKey(Project,on_delete=models.CASCADE)
    team =  models.ForeignKey(Team,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project)
