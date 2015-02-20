# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Movie.lat'
        db.add_column(u'street_movie', 'lat',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=9, decimal_places=6),
                      keep_default=False)

        # Adding field 'Movie.lon'
        db.add_column(u'street_movie', 'lon',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=9, decimal_places=6),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Movie.lat'
        db.delete_column(u'street_movie', 'lat')

        # Deleting field 'Movie.lon'
        db.delete_column(u'street_movie', 'lon')


    models = {
        u'api.movie': {
            'Meta': {'object_name': 'Movie', 'db_table': "u'street_movie'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '9', 'decimal_places': '6'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '9', 'decimal_places': '6'}),
            'movie': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['api']