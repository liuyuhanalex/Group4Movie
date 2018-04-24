from django import forms
from webapp.models import Users,Rates

class Search(forms.Form):
    CHOICES = (('movie','Movie'), ('people','People'),('user','User'))
    search_genre = forms.ChoiceField(label='',widget=forms.Select(attrs={'class':'search_genre'}),
    choices=CHOICES)
    search_content = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'search_content'}))

class Register(forms.ModelForm):

    class Meta:
        model = Users
        fields =['name','username','password']
        widgets = {
            'name':forms.TextInput(attrs={'class':'register_name'}),
            'username':forms.TextInput(attrs={'class':'register_username'}),
            'password':forms.PasswordInput(attrs={'class':'register_password'})
        }

class Login(forms.Form):
    login_username = forms.CharField(label="User Name",widget=forms.TextInput(attrs={'class':'login_username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'login_password'}))

# class Rating(forms.ModelForm):
#     class Meta:
#         model = Rates
#         fields = ['rating']
#         widgets = {
#             'rating':forms.NumberInput(attrs={'class':'rating'}),
#         }

class Rating(forms.Form):
    rating = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'rating'}))
