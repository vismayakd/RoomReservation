from django import forms
from .models import RoomCategory, Room, SpecialRate




class RoomCategoryForm(forms.ModelForm):
    class Meta:
        model = RoomCategory
        fields = ['name', 'base_price']


class RoomForm(forms.ModelForm):
    class  Meta:
        model = Room
        fields = ['room_number','category','is_available','image']

class SpecialRateForm(forms.ModelForm):
    class Meta:
        model = SpecialRate
        fields = ['room_category','start_date','end_date','rate_multiplier']
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            }