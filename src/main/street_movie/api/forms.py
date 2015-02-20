# coding: utf-8

import logging

from django import forms

logger = logging.getLogger(__name__)


class CreateMovieForm(forms.Form):
    latLng = forms.CharField(
        label=u'緯度経度',
        widget=forms.HiddenInput(attrs={'class': 'form-control'}),
    )

    start_lon = forms.DecimalField(
        label=u'経度（スタート）',
        max_digits=9,
        decimal_places=6,
        widget=forms.HiddenInput()
    )

    start_lat = forms.DecimalField(
        label=u'緯度（スタート）',
        max_digits=9,
        decimal_places=6,
        widget=forms.HiddenInput()
    )

    end_lon = forms.DecimalField(
        label=u'経度（エンド）',
        max_digits=9,
        decimal_places=6,
        widget=forms.HiddenInput()
    )

    end_lat = forms.DecimalField(
        label=u'緯度（エンド）',
        max_digits=9,
        decimal_places=6,
        widget=forms.HiddenInput()
    )