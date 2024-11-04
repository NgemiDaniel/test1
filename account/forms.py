from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser, UserProfile


# In forms.py
class SellerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'style': 'border: 1px solid #ccc; padding: 10px; width: 80%; margin-bottom: 20px; margin-top: 20px;',
                'placeholder': 'Enter your username'
            }),
            'password1': forms.PasswordInput(attrs={
                'style': 'border: 1px solid #ccc; padding: 10px; width: 80%; margin-bottom: 20px; margin-top: 20px;',
                'placeholder': 'Enter your password'
            }),
            'password2': forms.PasswordInput(attrs={
                'style': 'border: 1px solid #ccc; padding: 10px; width: 80%; margin-bottom: 20px; margin-top: 20px;',
                'placeholder': 'Confirm your password'
            }),
            'email': forms.EmailInput(attrs={
                'style': 'border: 1px solid #ccc; padding: 10px; width: 80%; margin-bottom: 20px; margin-top: 20px;',
                'placeholder': 'Enter your email address'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'seller'
        if commit:
            user.save()
        return user


class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'password1': forms.PasswordInput(attrs={'class': 'input-field'}),
            'password2': forms.PasswordInput(attrs={'class': 'input-field'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'client'  # Automatically assign role to 'client'
        if commit:
            user.save()
        return user


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role']

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in ['manager', 'sales']:
            raise forms.ValidationError("Only Manager and Sales roles can be created with this form.")
        return role

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'style': 'border: 1px solid #ccc; margin-left: 20px; background-color: lightcyan; padding: 20px; width: 70%; border-radius: 5px; margin-bottom: 10px;'
            }),
            'bio': forms.Textarea(attrs={
                'style': 'width: 80%; height: 150px; padding: 10px; background-color: lightcyan; margin-left: 20px; margin-bottom:20px; border: 1px solid #ccc; border-radius: 5px; resize: none; '
            }),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']  # Fields to update
        widgets = {
            'username': forms.TextInput(attrs={'style': 'border: 1px solid #ccc; border-radius: 5px; margin-bottom:20px; padding: 10px; width: 90%;'}),
            'email': forms.EmailInput(attrs={'style': 'border: 1px solid #ccc; margin-bottom:20px; margin-top:20px; border-radius: 5px; padding: 10px; width: 80%;'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check for existing usernames, excluding the current user
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


# Custom Password Change Form
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return new_password2