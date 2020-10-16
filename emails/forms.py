from django import forms

from .models import InventoryWaitlist

class InventoryWaitlistForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product") or None
        super().__init__(*args, **kwargs)
        self.product = product

    class Meta:
        model = InventoryWaitlist
        fields = [
            'email',
        ]
    

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        # check product inventory
        email = cleaned_data.get("email")
        qs = InventoryWaitlist.objects.filter(product=self.product, email__iexact=email)
        if qs.count() > 5:
            erro_msg = "10-4 we have your waitlist entry for this product."
            # raise self.add_error("email", erro_msg)
            raise forms.ValidationError(erro_msg) # non_field_errors
        return cleaned_data