from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic import View
from .forms import *
from .models import *
from tester import *


def on_challenge_enter(domain, subdomain, challenge, user):
    hist = TestsLog.objects.filter(domain=domain, subdomain=subdomain, task=challenge, username = user)
    if hist:
        return hist[0]
    else:
        z = challenge
        z.people_tried += 1
        z.success_rate = round(z.people_succeed / z.people_tried * 100, 2)
        z.save()
        q = TestsLog(domain=domain, subdomain=subdomain, task=challenge.task_name, username=user, result = False)
        q.save()
        return q


def challenges(request, domain_name, subdomain_name):
    subs = list(map(lambda x: x.subdomain_name,
                    subdomain.objects.filter(father_domain_name__domain_name__exact = domain_name)))

    context = {'subdomains': subs,
               'challenges': task.objects.filter(father_domain_name__domain_name__exact = domain_name).filter(
                   father_subdomain_name__subdomain_name__exact = subdomain_name),
               'domain': domain_name,
               'subdomain': subdomain_name,
               }
    return render(request, 'challenges.html', context)


def domains_list(request):
    qs = list(domain.objects.all())
    context = {
        'domains': qs,
    }
    z = subdomain.objects.all()
    for i in context['domains']:
        for j in z:
            if j.father_domain_name == i:
                context[i] = j

    return render(request, 'domains.html', context)


def challenge(request, domain_name, subdomain_name, challenge_name):
    cur_task = task.objects.filter(father_domain_name__domain_name__exact=domain_name).filter(
        task_name__exact=challenge_name).get()
    task_form = TaskForm(request.POST or None)

    context = {
        'name': cur_task,
        'task': cur_task.task_text,
        'subdomain': subdomain_name,
        'domain': domain_name,
        'form': task_form,
    }
    if request.user.is_authenticated:
        finished = on_challenge_enter(domain_name, subdomain_name, cur_task, request.user.username)

        if request.method == 'POST':
            if task_form.is_valid():
                code = (TaskForm.clean(task_form)['code'])
            tests_set = cur_task.test_set.all()
            tests = []
            for i in tests_set:
                tests.append([i.test_input.replace('\r', ''), i.test_output.replace('\r', '')])

            filename = str(request.user.username) + '_' + challenge_name
            result = TestProducer(tests, code, filename, domain_name).tests_result
            context['have_result'] = True
            if result[0]:
                solved = True
                for i in result[1]:
                    if not i:
                        solved = False
                if solved:
                    if not finished.result:
                        z = cur_task
                        z.people_succeed += 1
                        z.success_rate = round(z.people_succeed / z.people_tried * 100, 2)
                        z.save()
                        finished.result = True
                        finished.save()
                        q = User.objects.get(user = request.user)
                        if domain_name == 'python3':
                            q.python3 = q.python3 + cur_task.max_score
                        elif domain_name == 'cpp':
                            q.cpp = q.cpp + cur_task.max_score
                        elif domain_name == 'c':
                            q.c = q.c + cur_task.max_score
                        elif domain_name == 'java':
                            q.java = q.java + cur_task.max_score
                        q.save()
                        context['points'] = "You received " + str(cur_task.max_score) + ' points'
                    else:
                        context['points'] = "You have finished this task earlier, so you will not receive any points"
                context['solved'] = solved
                context['result'] = list(enumerate(result[1]))

            else:
                context['error'] = result[1]
    else:
        context['have_result'] = True
        context['error'] = "You don't have permissions to submit. Please Log In."
    return render(request, 'task.html', context)


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit = False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    q = User(user=user)
                    q.save()
                    return redirect('/challenges/')

        return render(request, self.template_name, {'form': form})


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username, password = password)
        if user:
           login(request, user)

    if request.method == 'GET':
        return render(request, 'registration.html', {'form': form, 'login': True})
    else:
        return redirect(next)


def logout_view(request):
    logout(request)
    return redirect('/challenges/')
