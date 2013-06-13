# -*- coding: utf-8 -*-
from builder.jobmng.models import Job,Build,Vcs,Setting
from django.contrib import admin

class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'type','vcs_type')
    save_as = True

class BuildAdmin(admin.ModelAdmin):    
    list_display = ('job','create_time', 'version','success','code','phrase')
    list_filter = ('job', 'success')
    search_fields = ('code','ver')

class VcsAdmin(admin.ModelAdmin):    
    list_display = ('job', 'name', 'address','work_copy')
    #单元素的turple，必须加逗号
    list_filter = ('job',)
    save_as = True
            
admin.site.register(Job, JobAdmin)
admin.site.register(Vcs, VcsAdmin)
admin.site.register(Build, BuildAdmin)
admin.site.register(Setting)



