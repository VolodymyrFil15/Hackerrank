from django.shortcuts import render
from Tasks.models import User



def homepage(request):

    context = {

    }
    return render(request, 'homepage.html', context)


def leaderboard(request, domain):
    q = []
    if domain == 'python3':
        a = User.objects.extra(order_by = ['-python3'])[:10]
        for i in a:
            q.append([i.user, i.python3])
    elif domain == 'cpp':
        a = User.objects.extra(order_by = ['-cpp'])[:10]
        for i in a:
            q.append([i.user, i.cpp])
    elif domain == 'c':
        a = User.objects.extra(order_by = ['-c'])[:10]
        for i in a:
            q.append([i.user, i.c])
    elif domain == 'java':
        a = User.objects.extra(order_by = ['-java'])[:10]
        for i in a:
            q.append([i.user, i.java])

    context = {
        'users': q,
        'domain': domain,
    }
    return render(request, 'Leaderboard.html', context)