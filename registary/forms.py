from django import forms
from .models import Citizen
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    
    # Profile fields
    national_id = forms.CharField(max_length=10, required=True)
    phone_number = forms.CharField(max_length=15, required=True, initial="+989")
    father_name = forms.CharField(max_length=100, required=True)
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        from .models import UserProfile
        if UserProfile.objects.filter(national_id=national_id).exists():
            raise forms.ValidationError("This National ID is already registered.")
        return national_id

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Create or get Citizen object
            citizen, created = Citizen.objects.get_or_create(
                national_id=self.cleaned_data.get('national_id'),
                defaults={
                    'first_name': self.cleaned_data.get('first_name'),
                    'last_name': self.cleaned_data.get('last_name'),
                    'phone_number': self.cleaned_data.get('phone_number'),
                    'father_name': self.cleaned_data.get('father_name'),
                    'birth_date': self.cleaned_data.get('birth_date'),
                    'address': self.cleaned_data.get('address'),
                }
            )
            # If citizen already existed but not connected to this user, update its info (optional)
            if not created:
                citizen.first_name = self.cleaned_data.get('first_name')
                citizen.last_name = self.cleaned_data.get('last_name')
                citizen.phone_number = self.cleaned_data.get('phone_number')
                citizen.father_name = self.cleaned_data.get('father_name')
                citizen.birth_date = self.cleaned_data.get('birth_date')
                citizen.address = self.cleaned_data.get('address')
                citizen.save()

            # Connect Citizen to UserProfile
            profile = user.profile
            profile.citizen = citizen
            profile.save()
        return user


    