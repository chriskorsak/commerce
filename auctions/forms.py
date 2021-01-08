from django import forms

#list form classes here

# class CreateEntryForm(forms.Form):
#   title = forms.CharField(max_length=64, initial="Title", widget=forms.TextInput(attrs={'class':'form-control'}))
#   price = forms.DecimalField(max_digits=8, decimal_places=2, initial="Price")
#   description = forms.CharField(widget=forms.Textarea, max_length=256, initial="Description")
#   photo = forms.CharField(max_length=200, initial="Photo URL")
#   category = forms.CharField(max_length=32, initial="Category")