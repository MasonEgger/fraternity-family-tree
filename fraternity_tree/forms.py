from django import forms
from .models import Brother

class FamilyTreeForm(forms.Form):
    name = forms.ChoiceField()
    generations = forms.IntegerField(help_text="How many generations above this brother would you like to include?", min_value=0, max_value=20)

    def __init__(self, *args, **kwargs):
        _brother_list = kwargs.pop('data_list', [])
        super(FamilyTreeForm, self).__init__(*args, **kwargs)

        self.fields['name'] = forms.ChoiceField(choices=_brother_list)

class PledgeClassForm(forms.Form):
    pledge_class = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        _pledge_class_list = kwargs.pop('data_list', [])
        super(PledgeClassForm, self).__init__(*args, **kwargs)

        self.fields['pledge_class'] = forms.ChoiceField(choices=_pledge_class_list)


