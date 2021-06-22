from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import TextInput, NumberInput
from .models import User, Document, Transcript, Translation

class RegisterationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegisterationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document','language',)
        labels = {
            'language': 'Video language'
        }


class TranscriptForm(forms.ModelForm):
    class Meta:
        model = Transcript
        fields = ('font','text_x','text_y','text_color','background_color','background_opacity','text_size',)
        widgets = {
            'text_color': TextInput(attrs={'type': 'color'}),
            'background_color': TextInput(attrs={'type': 'color'}),
            'background_opacity': NumberInput(attrs={'min': '0', 'max': '1', 'step': '0.1'})
        }
        labels = {
            'text_x': 'Text X ("left", "center", "right" or a number)',
            'text_y': 'Text Y ("top", "center", "bottom" or a number)'
        }

class TranslationForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ('language',)
        labels = {
            'language': 'Target language'
        }