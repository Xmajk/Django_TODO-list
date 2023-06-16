from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Uživatelské jméno'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Heslo'}))

    def clean(self):
        cleaned_data = super().clean()
        username=cleaned_data.get("username")
        password = cleaned_data.get("password")
        return cleaned_data