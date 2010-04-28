from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Runs all jobs that are due.'
    
    def handle(self, *args, **options):
        from backup.models import BackupJob
        procs = []
        for job in BackupJob.objects.all():
            p = job.run(False)
            if p is not None:
                procs.append(p)
        for p in procs:
            p.wait()
