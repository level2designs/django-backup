# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BackupJob'
        db.create_table('backup_backupjob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('backup_server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backup.BackupServer'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backup.Client'])),
            ('directory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backup.Directory'], null=True, blank=True)),
            ('database', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backup.Database'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('backup', ['BackupJob'])

        # Adding model 'Database'
        db.create_table('backup_database', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backup.Client'])),
            ('db_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('backup', ['Database'])

        # Adding model 'Directory'
        db.create_table('backup_directory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backup.Client'])),
            ('path', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('backup', ['Directory'])


    def backwards(self, orm):
        
        # Deleting model 'BackupJob'
        db.delete_table('backup_backupjob')

        # Deleting model 'Database'
        db.delete_table('backup_database')

        # Deleting model 'Directory'
        db.delete_table('backup_directory')


    models = {
        'backup.backupjob': {
            'Meta': {'object_name': 'BackupJob'},
            'backup_server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backup.BackupServer']"}),
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
