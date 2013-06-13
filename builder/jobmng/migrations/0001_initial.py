# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Setting'
        db.create_table('jobmng_setting', (
            ('key', self.gf('django.db.models.fields.CharField')(default='key', max_length=200, primary_key=True)),
            ('need_login', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('server_url', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('smtp_server', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('smtp_port', self.gf('django.db.models.fields.IntegerField')(default=587)),
            ('smtp_username', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('smtp_password', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('smtp_tls', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('jobmng', ['Setting'])

        # Adding model 'Job'
        db.create_table('jobmng_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=1024, blank=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('type', self.gf('django.db.models.fields.CharField')(default='standard', max_length=32)),
            ('state', self.gf('django.db.models.fields.CharField')(default='normal', max_length=32)),
            ('schedule', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('vcs_type', self.gf('django.db.models.fields.CharField')(default='none', max_length=32)),
            ('cmd', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('cmd_dir', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('process_for_kill', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('artifact', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('success_exp', self.gf('django.db.models.fields.CharField')(default='True', max_length=1024)),
            ('phrase_exp', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('success_email', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('fail_email', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal('jobmng', ['Job'])

        # Adding model 'Vcs'
        db.create_table('jobmng_vcs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobmng.Job'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('work_copy', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('trigger_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('wait_time', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('clean', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('revert', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('jobmng', ['Vcs'])

        # Adding model 'Build'
        db.create_table('jobmng_build', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobmng.Job'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('running', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('phrase', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('artifact', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
        ))
        db.send_create_signal('jobmng', ['Build'])


    def backwards(self, orm):
        
        # Deleting model 'Setting'
        db.delete_table('jobmng_setting')

        # Deleting model 'Job'
        db.delete_table('jobmng_job')

        # Deleting model 'Vcs'
        db.delete_table('jobmng_vcs')

        # Deleting model 'Build'
        db.delete_table('jobmng_build')


    models = {
        'jobmng.build': {
            'Meta': {'object_name': 'Build'},
            'artifact': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobmng.Job']"}),
            'phrase': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'running': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'jobmng.job': {
            'Meta': {'object_name': 'Job'},
            'artifact': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'cmd': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'cmd_dir': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {}),
            'fail_email': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'phrase_exp': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'process_for_kill': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'schedule': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '32'}),
            'success_email': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'success_exp': ('django.db.models.fields.CharField', [], {'default': "'True'", 'max_length': '1024'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'standard'", 'max_length': '32'}),
            'vcs_type': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '32'})
        },
        'jobmng.setting': {
            'Meta': {'object_name': 'Setting'},
            'key': ('django.db.models.fields.CharField', [], {'default': "'key'", 'max_length': '200', 'primary_key': 'True'}),
            'need_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'server_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'smtp_password': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'smtp_port': ('django.db.models.fields.IntegerField', [], {'default': '587'}),
            'smtp_server': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'smtp_tls': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'smtp_username': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'jobmng.vcs': {
            'Meta': {'object_name': 'Vcs'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'clean': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jobmng.Job']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'revert': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trigger_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'wait_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'work_copy': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['jobmng']
