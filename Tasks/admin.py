from django.contrib import admin
from .models import *
# Register your models here.


class SubdomainView(admin.ModelAdmin):
    list_display = ['subdomain_name', 'father_domain_name']
    list_display_links = ['subdomain_name']

class TaskView(admin.ModelAdmin):
    list_display = ['task_name', 'father_domain_name', 'father_subdomain_name']
    list_display_links = ['task_name', 'father_domain_name', 'father_subdomain_name']
    exclude = ('people_tried', 'people_succeed', 'success_rate')
    search_fields = ('task_name',)


admin.site.register(domain)
admin.site.register(subdomain, SubdomainView)
admin.site.register(task, TaskView)
admin.site.register(Test)
admin.site.register(User)
#admin.site.register(TestsLog)

