__author__ = 'osito_wang'
__date__ = '2018/6/19 10:24'
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={"invalid": "You have entered wrong verify code"})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "You have entered wrong verify code"})



class ModifyPwdForm(forms.Form):
    new_password = forms.CharField(required=True, min_length=6)
    confirm_password = forms.CharField(required=True, min_length=6)

