# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Movie.lon'
        db.delete_column(u'street_movie', 'lon')

        # Deleting field 'Movie.lat'
        db.delete_column(u'street_movie', 'lat')

        # Adding field 'Movie.start_lat'
        db.add_column(u'street_movie', 'start_lat',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=9, decimal_places=6),
                      keep_default=False)

        # Adding field 'Movie.start_lon'
        db.add_column(u'street_movie', 'start_lon',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=9, decimal_places=6),
                      keep_default=False)

        # Adding field 'Movie.end_lat'
        db.add_column(u'street_movie', 'end_lat',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=9, decimal_places=6),
                      keep_default=False)

        # Adding field 'Movie.end_lon'
        db.add_column(u'street_movie', 'end_lon',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=9, decimal_places=6),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Movie.lon'
        db.add_column(u'street_movie', 'lon',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=9, decimal_places=6),
                      keep_default=False)

        # Adding field 'Movie.lat'
        db.add_column(u'street_movie', 'lat',
                      self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=9, decimal_places=6),
                      keep_default=False)

        # Deleting field 'Movie.start_lat'
        db.delete_column(u'street_movie', 'start_lat')

        # Deleting field 'Movie.start_lon'
        db.delete_column(u'street_movie', 'start_lon')

        # Deleting field 'Movie.end_lat'
        db.delete_column(u'street_movie', 'end_lat')

        # Deleting field 'Movie.end_lon'
        db.delete_column(u'street_movie', 'end_lon')


    models = {
        u'api.movie': {
            'Meta': {'object_name': 'Movie', 'db_table': "u'street_movie'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_lat': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '9', 'decimal_places': '6'}),
            'end_lon': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '9', 'decimal_places': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'start_lat': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '9', 'decimal_places': '6'}),
            'start_lon': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '9', 'decimal_places': '6'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['api']