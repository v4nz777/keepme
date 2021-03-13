from django import forms
from .models import User, Thing, TransactionLend, TransactionBorrow
from django.contrib.admin import widgets




class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ['thing_name', 'serial_no', 'image']

        labels = {
            'thing_name': '',
            'serial_no': '',
            'image': ''
        }

        widgets = {    
            'thing_name': forms.TextInput(attrs={
                'placeholder': 'Enter object name...',
                'class': 'form-input'
            }),
            'serial_no': forms.TextInput(attrs={
                'placeholder': 'Enter serial number...',
                'class': 'form-input'
            })
        }

class UpdateAvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']
        labels = {'avatar':''}
        widgets = {
            'avatar': forms.FileInput(attrs={
                'id': 'avatarInput'
            })
        }

class TransactionLendForm(forms.ModelForm):
    class Meta:
        model = TransactionLend
        fields = ['lender', 'thing', 'borrower', 'promised_return']
        exclude = ['lender', 'thing', 'borrower']
        widgets = {
            'promised_return': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            )
        }

class TransactionBorrowForm(forms.ModelForm):
    class Meta:
        model = TransactionBorrow
        fields = ['thing', 'borrower','owner', 'promised_return']
        exclude = ['thing', 'borrower', 'owner']
        widgets = {
            'promised_return': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            )
        }