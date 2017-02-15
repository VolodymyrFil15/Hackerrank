from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class domain(models.Model):
    domain_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.domain_name


class subdomain(models.Model):
    father_domain_name = models.ForeignKey(domain)
    subdomain_name = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.father_domain_name) + '/' + str(self.subdomain_name)


class task(models.Model):
    choices = (('Easy','Easy'), ('Medium', 'Medium'), ('Hard','Hard'))
    father_domain_name = models.ForeignKey(domain)
    father_subdomain_name = models.ForeignKey(subdomain)
    task_name = models.CharField(max_length = 50)
    max_score = models.IntegerField()
    difficulty = models.CharField(max_length = 10, choices = choices, default = 'Easy')
    people_tried = models.IntegerField(default = 0)
    people_succeed = models.IntegerField(default = 0)
    success_rate = models.FloatField(max_length = 4, default = 0)
    task_text = models.TextField(max_length=15000)

    def __str__(self):
        return str(self.task_name).replace('_', " ")


class Test(models.Model):
    father_task_name = models.ForeignKey(task, blank = True)
    test_input = models.TextField(max_length=15000, blank = True)
    test_output = models.TextField(max_length = 15000)

    def __str__(self):
        return str(self.father_task_name)


class TestsLog(models.Model):
    username = models.CharField(max_length = 30)
    timestamp = models.DateTimeField(auto_now = True)
    domain = models.CharField(max_length = 30)
    subdomain = models.CharField(max_length = 30)
    task = models.CharField(max_length = 30)
    result = models.BooleanField()


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    python3 = models.IntegerField(default = 0)
    cpp = models.IntegerField(default = 0)
    c = models.IntegerField(default = 0)
    java = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.user)
