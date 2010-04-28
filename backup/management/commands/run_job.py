from django.core.management import call_command
from django.core.management.base import BaseCommand

from backup.models import BackupJob

class Command(BaseCommand):
    help = 'Runs a specific job. THe job will only run if it is not currently running.'
    args = "job.id"
    
    def handle(self, *args, **options):
        try:
            job_id = args[0]
        except IndexError:
            sys.stderr.write("This command requires a single argument: a job id to run.\n")
            return

        try:
            job = BackupJob.objects.get(pk=job_id)
        except Job.DoesNotExist:
            sys.stderr.write("The requested Job does not exist.\n")
            return
        
        # Run the job and wait for it to finish
        job.handle_run()
