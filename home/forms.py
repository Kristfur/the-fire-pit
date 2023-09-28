from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    """
    Add first and last name to signup form
    """
    first_name = forms.CharField(max_length=30, label='First Name',
                                 widget=forms.TextInput(
                                    attrs={'placeholder': ('First Name')}))
    last_name = forms.CharField(max_length=30, label='Last Name',
                                widget=forms.TextInput(
                                    attrs={'placeholder': ('Last Name')}))

    def save(self, request):
        """
        Save user model, save first and last name to model
        """
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
