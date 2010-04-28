from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timesince import timeuntil
from django.utils.translation import ungettext, ugettext, ugettext_lazy as _

from backup.utils import *

import os
import re
import subprocess
import sys
import traceback
import shlex

from datetime import datetime
from dateutil import rrule

RRULE_WEEKDAY_DICT = {"MO":0,"TU":1,"WE":2,"TH":3,"FR":4,"SA":5,"SU":6}

class Client(models.Model):
    name = models.CharField(_("name"), max_length=255, default="")
    description = models.CharField(_("description"), max_length=255, default="")
    address = models.CharField(_("hostname or IP address"), max_length=255, default="")
    username = models.CharField(_("username to client"), max_length=255, default="", help_text=_('The client will be accessed using this username. Remember this must correspond to the SSH key that is setup for the backup server and backup client.'))
    database_dump_path = models.CharField(_('Database Dump Path'), max_length=255, null=True, blank=True, default="", help_text=_('Location of database dumps on client.  This is where the most recent database dumps will be stored on the client, so that rdiff-backup can be used to back them up (full and incrementally) on the backup server'))
    
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.address)

class BackupServer(models.Model):
    name = models.CharField(_("name"), max_length=255, default="")
    description = models.CharField(_("description"), max_length=255, default="")
    address = models.CharField(_("hostname or IP address"), max_length=255, default="")
    username = models.CharField(_("username to server"), max_length=255, default="", help_text=_('The backup jobs will be run using this username. Remember this must correspond to the SSH key that is setup for the web server and backup server.'))
    backup_store_path = models.CharField(_("Backup Store Path"), max_length=255, default="", help_text=_("Where backup files are stored on the backup server."))
    
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.address)
        
class Directory(models.Model):
    client = models.ForeignKey(Client)
    path = models.CharField(_("path"), max_length=255, default="")

    def __unicode__(self):
        return u'"%s" on "%s"' % (self.path, self.client.name)

class Database(models.Model):
    client = models.ForeignKey(Client)
    db_name = models.CharField(_("Database Name"), max_length=255, default="")
    username = models.CharField(_("Datause Username"), max_length=255, default="")
    password = models.CharField(_("Database Password"), max_length=255, default="")

    def __unicode__(self):
        return u'"%s" on "%s"' % (self.db_name, self.client.name)
        
class BackupJob(models.Model):
    freqs = (   ("YEARLY", _("Yearly")),
                ("MONTHLY", _("Monthly")),
                ("WEEKLY", _("Weekly")),
                ("DAILY", _("Daily")),
                ("HOURLY", _("Hourly")),
                ("MINUTELY", _("Minutely"))
            )
    
    backup_server = models.ForeignKey(BackupServer)
    client = models.ForeignKey(Client)
    directories = models.ManyToManyField(Directory, null=True, blank=True)
    databases = models.ManyToManyField(Database, null=True, blank=True)
    disabled = models.BooleanField(default=False, help_text=_('If checked this job will never run.'))
    frequency = models.CharField(_("frequency"), choices=freqs, max_length=10, default="DAILY")
    next_run = models.DateTimeField(_("next run"), blank=True, null=True, help_text=_("If you don't set this it will be determined automatically"), default=datetime.now())
    last_run = models.DateTimeField(_("last run"), editable=False, blank=True, null=True)
    last_run_successful = models.BooleanField(default=True, blank=False, null=False, editable=False)
    is_running = models.BooleanField(default=False, editable=False)
    subscribers = models.ManyToManyField(User, blank=True)
    pid = models.IntegerField(blank=True, null=True, editable=False)
    force_run = models.BooleanField(default=False)
    
    class Meta:
            ordering = ('disabled', 'next_run',)
    
    def __unicode__(self):     
        if self.disabled:    
            return u'Backup of "%s" on "%s" (disabled)' % (self.client.name, self.backup_server.name)
        
        return u'Backup of "%s" on "%s"' % (self.client.name, self.backup_server.name)
        
    def save(self, force_insert=False, force_update=False):
        if not self.disabled:
            if self.pk:
                j = BackupJob.objects.get(pk=self.pk)
            else:
                j = self
            if not self.next_run:
                self.next_run = self.rrule.after(datetime.now())
            if self.force_run:
                self.next_run = datetime.now()
        else:
            self.next_run = None

        super(BackupJob, self).save(force_insert, force_update)
    
    def get_timeuntil(self):
        """
        Returns a string representing the time until the next
        time this Job will be run.
        """
        if self.disabled:
            return _('never (disabled)')

        delta = self.next_run - datetime.now()
        if delta.days < 0:
            # The job is past due and should be run as soon as possible
            return _('due')
        elif delta.seconds < 60:
            # Adapted from django.utils.timesince
            count = lambda n: ungettext('second', 'seconds', n)
            return ugettext('%(number)d %(type)s') % {'number': delta.seconds,
                                                      'type': count(delta.seconds)}
        return timeuntil(self.next_run)
    get_timeuntil.short_description = _('time until next run')
    timeuntil = property(get_timeuntil)
        
    def get_rrule(self):
        """
        Returns the rrule objects for this Job.
        """
        frequency = eval('rrule.%s' % self.frequency)
        return rrule.rrule(frequency, dtstart=self.last_run)
    rrule = property(get_rrule)

    def is_due(self):
        reqs =  (self.next_run <= datetime.now() and self.disabled == False and self.is_running == False)
        return (reqs or self.force_run)
    
    def run(self, wait=True):
        """
        Runs this ``Job``.  If ``wait`` is ``True`` any call to this function will not return
        untill the ``Job`` is complete (or fails).  This actually calls the management command
        ``run_job`` via a subprocess.  If you call this and want to wait for the process to
        complete, pass ``wait=True``.

        A ``Log`` will be created if there is any output from either stdout or stderr.

        Returns the process, a ``subprocess.Popen`` instance, or None.
        """
        if not self.disabled:
            if not self.check_is_running() and self.is_due():
                p = subprocess.Popen(['python', get_manage_py(), 'run_job', str(self.pk)])
                if wait:
                    p.wait()
                return p
        return None
        
    def handle_run(self):
        """
        foreach directory:
            run rdiff-backup [username]@[address]::[path] [jobid - address]/directories[path]
            log completion for each directory
        foreach database:
            run ssh [username]@[address] 'mysqldump --user [db_user] --password=[db_pass] [database_name] > [database_dump_path]/[database_name].sql
            run rdiff-backup [username]@[address]::[database_dump_path] [jobid - address]/databases
            log completion for each database
        
        when full job completes, log completion and then email supervisors
        """
                
        backup_server_username = self.backup_server.username.strip()
        backup_server_host = self.backup_server.address.strip()
        
        run_date = datetime.now()
        self.is_running = True
        self.pid = os.getpid()
        self.save()
        
        # start backup

        if self.directories:
            for directory in self.directories.all():
                backup_server_path = "%s/%s-%s/directories%s" % (self.backup_server.backup_store_path.strip(), self.pk, self.client.address.strip(), directory.path.strip())
                
                # Make the backup directory if it doesn't exist
                run_make_backup_dir(self.backup_server, backup_server_path)
                
                # run the backup
                run_directory_backup(self.backup_server, self.client, directory.path, backup_server_path)
        
        if self.databases:
            for database in self.databases.all():                            
                # run the db backup
                run_database_backup(self.backup_server, self.client, database)
            
            backup_server_path = "%s/%s-%s/databases" % (self.backup_server.backup_store_path.strip(), self.pk, self.client.address.strip())
            
            # Make the backup directory if it doesn't exist
            run_make_backup_dir(self.backup_server, backup_server_path)
            
            #run rdiff of db dump dir
            run_directory_backup(self.backup_server, self.client, self.client.database_dump_path.strip(), backup_server_path)
            
        # backup finsihed
        
        self.last_run_successful = True
        self.is_running = False
        self.pid = None
        self.last_run = run_date
        
        # If this was a forced run, then don't update the
        # next_run date
        if self.force_run:
            self.force_run = False
        else:
            self.next_run = self.rrule.after(run_date)
        self.save()
        
    def check_is_running(self):
        """
        This function actually checks to ensure that a job is running.
        Currently, it only supports `posix` systems.  On non-posix systems
        it returns the value of this job's ``is_running`` field.
        """
        status = False
        if self.is_running and self.pid is not None:
            # The Job thinks that it is running, so
            # lets actually check
            if os.name == 'posix':
                # Try to use the 'ps' command to see if the process
                # is still running
                pid_re = re.compile(r'%d ([^\r\n]*)\n' % self.pid)
                p = subprocess.Popen(["ps", "-eo", "pid args"], stdout=subprocess.PIPE)
                p.wait()
                # If ``pid_re.findall`` returns a match it means that we have a
                # running process with this ``self.pid``.  Now we must check for
                # the ``run_command`` process with the given ``self.pk``
                try:
                    pname = pid_re.findall(p.stdout.read())[0]
                except IndexError:
                    pname = ''
                if pname.find('run_job %d' % self.pk) > -1:
                    # This Job is still running
                    return True
                else:
                    # This job thinks it is running, but really isn't.
                    self.is_running = False
                    self.pid = None
                    self.save()
            else:
                # TODO: add support for other OSes
                return self.is_running
        return False

    
    
