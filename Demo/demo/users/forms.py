from django import forms
from users.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    re_password = forms.CharField(label="Re-type Password", widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['username', 'fullname', 'password', 're_password', 'phone', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")

        if password or re_password:
            if password != re_password:
                raise forms.ValidationError("Passwords do not match")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(widget=forms.PasswordInput)