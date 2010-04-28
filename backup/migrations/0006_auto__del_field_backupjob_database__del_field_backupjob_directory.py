# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'BackupJob.database'
        db.delete_column('backup_backupjob', 'database_id')

        # Deleting field 'BackupJob.directory'
        db.delete_column('backup_backupjob', 'directory_id')

        # Adding M2M table for field directory on 'BackupJob'
        db.create_table('backup_backupjob_directory', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('backupjob', models.ForeignKey(orm['backup.backupjob'], null=False)),
            ('directory', models.ForeignKey(orm['backup.directory'], null=False))
        ))
        db.create_unique('backup_backupjob_directory', ['backupjob_id', 'directory_id'])

        # Adding M2M table for field database on 'BackupJob'
        db.create_table('backup_backupjob_database', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('backupjob', models.ForeignKey(orm['backup.backupjob'], null=False)),
            ('database', models.ForeignKey(orm['backup.database'], null=False))
        ))
        db.create_unique('backup_backupjob_database', ['backupjob_id', 'database_id'])


    def backwards(self, orm):
        
        # Adding field 'BackupJob.database'
        db.add_column('backup_backupjob', 'database', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backup.Database'], null=True, blank=True), keep_default=False)

        # Adding field 'BackupJob.directory'
        db.add_column('backup_backupjob', 'directory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backup.Directory'], null=True, blank=True), keep_default=False)

        # Removing M2M table for field directory on 'BackupJob'
        db.delete_table('backup_backupjob_directory')

        # Removing M2M table for field database on 'BackupJob'
        db.delete_table('backup_backupjob_database')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'backup.backupjob': {
            'Meta': {'object_name': 'BackupJob'},
            'backup_server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backup.BackupServer']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backup.Client']"}),
            'database': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['backup.Database']", 'null': 'True', 'blank': 'True'}),
            'directory': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['backup.Directory']", 'null': 'True', 'blank': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'force_run': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.CharField', [], {'default': "'DAILY'", 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_running': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_run': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_run_successful': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'next_run': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 4, 23, 21, 46, 2, 19563)', 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'backup.backupserver': {
            'Meta': {'object_name': 'BackupServer'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'backup.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'backup.database': {
            'Meta': {'object_name': 'Database'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backup.Client']"}),
            'db_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'backup.directory': {
            'Meta': {'object_name': 'Directory'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backup.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['backup']
