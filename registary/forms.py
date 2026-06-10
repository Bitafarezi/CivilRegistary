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


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    
    # Profile fields
    national_id = forms.CharField(max_length=10, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    father_name = forms.CharField(max_length=100, required=True)
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile') and self.instance.profile.citizen:
            citizen = self.instance.profile.citizen
            
            self.fields['national_id'].initial = citizen.national_id
            self.fields['phone_number'].initial = citizen.phone_number
            self.fields['father_name'].initial = citizen.father_name
            self.fields['birth_date'].initial = citizen.birth_date
            self.fields['address'].initial = citizen.address
            
            for field in ['first_name', 'last_name','national_id', 'father_name', 'birth_date']:
                self.fields[field].disabled = True

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = user.profile
            citizen = profile.citizen
            if citizen:
                # Some other fields not updated here because they are disabled in the form
                citizen.phone_number = self.cleaned_data.get('phone_number')
                citizen.address = self.cleaned_data.get('address')
                citizen.save()
        return user
    