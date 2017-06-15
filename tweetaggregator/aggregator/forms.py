from django import forms

from multiselectfield import MultiSelectFormField

from .models import Twitter, Category


class TwitterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TwitterForm, self).__init__(*args, **kwargs)
        self.fields['categories'] = MultiSelectFormField(choices=[
            (category.name, category.name) for category in Category.objects.all()
        ])
    
    class Meta:
        model = Twitter
        fields = '__all__'
