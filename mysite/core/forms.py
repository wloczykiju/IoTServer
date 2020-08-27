from django import forms
from .models import Connection


class ConnectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConnectionForm, self).__init__(*args, **kwargs)
        self.fields['ip'].label = "IP address of your server"
        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
       
    class Meta:
        model = Connection
        fields = ('ip', 'username', 'password')
 

    def clean(self):
        cleaned_data = super(ConnectionForm, self).clean()
        ip = cleaned_data.get('ip')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not ip and not username and not password:
            raise forms.ValidationError('You have to fill in all fields!')

