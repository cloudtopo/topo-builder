# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Job.topo_url_create_build'
        db.delete_column('jobmng_job', 'topo_url_create_build')

        # Adding field 'Job.custom_cmd1_name'
        db.add_column('jobmng_job', 'custom_cmd1_name', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True), keep_default=False)

        # Adding field 'Job.custom_cmd1_cmd'
        db.add_column('jobmng_job', 'custom_cmd1_cmd', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True), keep_default=False)

        # Adding field 'Job.custom_cmd1_path'
        db.add_column('jobmng_job', 'custom_cmd1_path', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True), keep_default=False)

        # Adding field 'Job.custom_cmd2_name'
        db.add_column('jobmng_job', 'custom_cmd2_name', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True), keep_default=False)

        # Adding field 'Job.custom_cmd2_cmd'
        db.add_column('jobmng_job', 'custom_cmd2_cmd', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True), keep_default=False)

        # Adding field 'Job.custom_cmd2_path'
        db.add_column('jobmng_job', 'custom_cmd2_path', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True), keep_default=False)

        # Adding field 'Job.custom_cmd3_name'
        db.add_column('jobmng_job', 'custom_cmd3_name', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True), keep_default=False)

        # Adding field 'Job.custom_cmd3_cmd'
        db.add_column('jobmng_job', 'custom_cmd3_cmd', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True), keep_default=False)

        # Adding field 'Job.custom_cmd3_path'
        db.add_column('jobmng_job', 'custom_cmd3_path', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Job.topo_url_create_build'
        db.add_column('jobmng_job', 'topo_url_create_build', self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True), keep_default=False)

        # Deleting field 'Job.custom_cmd1_name'
        db.delete_column('jobmng_job', 'custom_cmd1_name')

        # Deleting field 'Job.custom_cmd1_cmd'
        db.delete_column('jobmng_job', 'custom_cmd1_cmd')

        # Deleting field 'Job.custom_cmd1_path'
        db.delete_column('jobmng_job', 'custom_cmd1_path')

        # Deleting field 'Job.custom_cmd2_name'
        db.delete_column('jobmng_job', 'custom_cmd2_name')

        # Deleting field 'Job.custom_cmd2_cmd'
        db.delete_column('jobmng_job', 'custom_cmd2_cmd')

        # Deleting field 'Job.custom_cmd2_path'
        db.delete_column('jobmng_job', 'custom_cmd2_path')

        # Deleting field 'Job.custom_cmd3_name'
        db.delete_column('jobmng_job', 'custom_cmd3_name')

        # Deleting field 'Job.custom_cmd3_cmd'
        db.delete_column('jobmng_job', 'custom_cmd3_cmd')

        # Deleting field 'Job.custom_cmd3_path'
        db.delete_column('jobmng_job', 'custom_cmd3_path')


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
            'custom_cmd1_cmd': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'custom_cmd1_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'custom_cmd1_path': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'custom_cmd2_cmd': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'custom_cmd2_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'custom_cmd2_path': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'custom_cmd3_cmd': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'custom_cmd3_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'custom_cmd3_path': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'fail_email': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'finish_cmd': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
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
            'vcs_pass': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'vcs_user': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'wait_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'work_copy': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['jobmng']
