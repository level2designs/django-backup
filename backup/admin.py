from django import forms
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.management import get_commands
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.forms.util import flatatt
from django.http import HttpResponseRedirect, Http404
from django.template.defaultfilters import linebreaks
from django.utils import dateformat
from django.utils.datastructures import MultiValueDict
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ungettext, get_date_formats, ugettext_lazy as _

from backup.models import *

from datetime import datetime

admin.site.register(Client)
admin.site.register(BackupServer)
admin.site.register(Directory)

class HTMLWidget(forms.Widget):
    def __init__(self,rel=None, attrs=None):
        self.rel = rel
        super(HTMLWidget, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        if self.rel is not None:
            key = self.rel.get_related_field().name
            obj = self.rel.to._default_manager.get(**{key: value})
            related_url = '../../../%s/%s/%d/' % (self.rel.to._meta.app_label, self.rel.to._meta.object_name.lower(), value)
            value = "<a href='%s'>%s</a>" % (related_url, escape(obj))
            
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe("<div%s>%s</div>" % (flatatt(final_attrs), linebreaks(value)))


class DatabaseAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Database

class DatabaseAdmin(admin.ModelAdmin):
    form = DatabaseAdminForm

admin.site.register(Database, DatabaseAdmin)

class BackupJobAdmin(admin.ModelAdmin):
    actions = ['run_selected_jobs']
    
    list_display = ('backup_server', 'client', 'frequency', 'get_timeuntil', 'last_run', 'last_run_successful', 'is_running', 'run_button')
    list_filter = ('last_run_successful', 'frequency', 'disabled')
    filter_horizontal = ('subscribers', 'databases', 'directories')
    fieldsets = (
            ('Job Details', {
                'classes': ('wide',),
                'fields': ('backup_server', 'client', 'directories', 'databases')
            }),
            ('E-mail subscriptions', {
                'classes': ('wide',),
                'fields': ('subscribers',)
            }),
            ('Frequency options', {
                'classes': ('wide',),
                'fields': ('force_run', 'disabled', 'frequency', 'next_run')
            }),
        )
    
    def get_timeuntil(self, obj):
        format = get_date_formats()[1]
        value = capfirst(dateformat.format(obj.next_run, format))
        return "%s<br /><span class='mini'>(%s)</span>" % (value, obj.get_timeuntil())
    get_timeuntil.admin_order_field = 'next_run'
    get_timeuntil.allow_tags = True
    get_timeuntil.short_description = _('next scheduled run')
        
    def run_button(self, obj):
        on_click = "window.location='%d/run/?inline=1';" % obj.id
        return '<input type="button" onclick="%s" value="Run" />' % on_click
    
    run_button.allow_tags = True
    run_button.short_description = 'Run'

    def run_job_view(self, request, pk):
        """
        Runs the specified job.
        """
        try:
            job = BackupJob.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404
        # Rather than actually running the Job right now, we
        # simply force the Job to be run by the next cron job
        job.force_run = True
        job.save()
        request.user.message_set.create(message=_('The job "%(job)s" has been scheduled to run.') % {'job': job})        
        if 'inline' in request.GET:
            redirect = request.path + '../../'
        else:
            redirect = request.REQUEST.get('next', request.path + "../")
        return HttpResponseRedirect(redirect)

    def get_urls(self):
        urls = super(BackupJobAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(.+)/run/$', self.admin_site.admin_view(self.run_job_view), name="backup_job_run")
        )
        return my_urls + urls

    def run_selected_jobs(self, request, queryset):
        rows_updated = queryset.update(force_run=True)
        if rows_updated == 1:
            message_bit = "1 job was"
        else:
            message_bit = "%s jobs were" % rows_updated
        self.message_user(request, "%s successfully set to run." % message_bit)
    run_selected_jobs.short_description = "Run selected jobs"

admin.site.register(BackupJob, BackupJobAdmin)