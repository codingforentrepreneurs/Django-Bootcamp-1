from django import forms

from .models import Product
# class ProductForm(forms.Form):
#     title = forms.CharField()


class ProductModelForm(forms.ModelForm):
    # title = forms.CharField()
    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'image',
            'media',
        ]
        exclude = [
            'price'
        ]
    
    def clean_content(self):
        data = self.cleaned_data.get('content')
        if len(data) < 4:
            raise forms.ValidationError("This is not long enough")
        return data