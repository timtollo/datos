from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm
from django.forms import inlineformset_factory, BaseInlineFormSet

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'username', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'unit_price']
        
        
class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        
class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['customer', 'expiry_date', 'quotation_number']
        widgets = {
            'quotation_number': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class CustomQuotationItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not form.cleaned_data.get('item') and not form.cleaned_data.get('quantity'):
                continue
            if not form.cleaned_data.get('item'):
                raise forms.ValidationError("Item must be selected.")
            if not form.cleaned_data.get('quantity'):
                raise forms.ValidationError("Quantity must be provided.")

QuotationItemFormSet = inlineformset_factory(
    Quotation,
    QuotationItem,
    formset=CustomQuotationItemFormSet,
    fields=['item', 'quantity'],
    extra=1,
    can_delete=True
)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['quotation','due_date', 'amount_paid']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the queryset for the quotation field
        self.fields['quotation'].queryset = Quotation.objects.all()  # This ensures you fetch all quotations
        
        
# Supplier Form
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'contact_name', 'phone', 'email', 'address']

# Expense Form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['supplier', 'name', 'description', 'category_type', 'payment_method', 'amount', 'date']
        
        
class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = ['name', 'description','workstream']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'progress', 'due_date', 'kpi','risk_level']

