from django import forms
from .models import History


class HistoryForm(forms.ModelForm) :
   class Meta :
       model = History
       fields=(
        #    "table_name",
           )
