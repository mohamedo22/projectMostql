# imageditor/forms.py
from django import forms

class TextForm(forms.Form):
    text1 = forms.CharField(label='Text 1', max_length=100)
    text2 = forms.CharField(label='Text 2', max_length=100)
    text3 = forms.CharField(label='Text 3', max_length=100)
    text4 = forms.CharField(label='Text 4', max_length=100)
    text5 = forms.CharField(label='Text 5', max_length=100)
    text6 = forms.CharField(label='Text 6', max_length=100)
    text7 = forms.CharField(label='Text 7', max_length=100)
    text8 = forms.CharField(label='Text 8', max_length=100)
    text9 = forms.CharField(label='Text 9', max_length=100)
    text10 = forms.CharField(label='Text 10', max_length=100)
