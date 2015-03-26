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

    start_name = forms.CharField(
        label=u'スタート地点',
        widget=forms.HiddenInput(attrs={'class': 'form-control'}),
    )

    end_name = forms.CharField(
        label=u'エンド地点',
        widget=forms.HiddenInput(attrs={'class': 'form-control'}),
    )

    center_lat = forms.DecimalField(
        label=u"緯度(中心)",
        max_digits=9,
        decimal_places=6,
        widget=forms.HiddenInput()
    )

    center_lon = forms.DecimalField(
        label=u"軽度(中心)",
        max_digits=9,
        decimal_places=6,
        widget=forms.HiddenInput()
    )