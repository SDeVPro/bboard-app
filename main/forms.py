from django import forms
from django.forms import fields, models
from .models import AdvUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .apps import user_registreted

class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Elektron manzil')

    class Meta:
        model = AdvUser
        fields = {'username','email','first_name','last_name','send_messages'}

class RegistrerUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,label='Elektron manzil')
    password1 = forms.CharField(label='Parol',widget=forms.PasswordInput,help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Parol(qaytatdan)',widget=forms.PasswordInput,help_text='Parolni yuqorida kiritgan parolingizdek kiriting')
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password_validation)
        return password1
    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1!=password2:
            errors = {'password2':ValidationError('Kiritilgan parollar mos tushmadi',code='password_mismatch')}
            raise ValidationError(errors)

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registreted.send(RegistrerUserForm, instance=user)
        return user 
    class Meta:
        model = AdvUser
        fields = {'username','email','password1','password2','first_name','last_name','send_messages'}