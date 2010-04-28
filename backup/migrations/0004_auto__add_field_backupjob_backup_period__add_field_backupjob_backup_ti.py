# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'BackupJob.backup_period'
        db.add_column('backup_backupjob', 'backup_period', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)

        # Adding field 'BackupJob.backup_time'
        db.add_column('backup_backupjob', 'backup_time', self.gf('django.db.models.fields.TimeField')(default='00:00:00'), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'BackupJob.backup_period'
        db.delete_column('backup_backupjob', 'backup_period')

        # Deleting field 'BackupJob.backup_time'
        db.delete_column('backup_backupjob', 'backup_time')


    models = {
        'backup.backupjob': {
            'Meta': {'object_name': 'BackupJob'},
            'backup_period': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'backup_server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backup.BackupServer']"}),
            'backup_time': ('django.db.models.fields.TimeField', [], {'default': "''"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backup.Client']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'database': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backup.Database']", 'null': 'True', 'blank': 'True'}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backup.Directory']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        }
    }

    complete_apps = ['backup']
