from django import  forms
from django.forms import ModelForm, inlineformset_factory, HiddenInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from .models import Asset, Order, Staff, OrderItem


class AssetForm(ModelForm):
    class Meta:
        model = Asset
        fields = ['name','track_id','category', 'brand', 'sn', 'price', 'employee', 'date_purchase', 'date_warranty', 'status', 'location', 'supplier', 'description']
        labels = {
            'name': 'Asset Name',
            'track_id': 'Asset ID',
            'employee': 'Assigned Employee',
            'sn': 'Serial Number'
        },
        widgets = {
            'date_purchase': forms.DateInput(attrs={'type': 'date'}),
            'date_warranty': forms.DateInput(attrs={'type': 'date'}),
        }   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Field(
                        'name',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        placeholder='e.g., MacBook Pro 16',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                Div(
                    Field(
                        'track_id',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        placeholder='Auto-generated if empty',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Div(
                    Field(
                        'category',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                Div(
                    Field(
                        'brand',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        placeholder='e.g., Apple, Dell, HP',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Div(
                    Field(
                        'employee',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                Div(
                    Field(
                        'sn',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        placeholder="Serial number",
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Div(
                    Field(
                        'price',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        placeholder="0.00",
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                Div(
                    Field(
                        'date_purchase',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        placeholder='e.g., MacBook Pro 16',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Div(
                    Field(
                        'location',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        placeholder="e.g., IT Department, Floor 2",
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                Div(
                    Field(
                        'status',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Div(
                    Field(
                        'date_warranty',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                Div(
                    Field(
                        'supplier',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        placeholder='Supplier name',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Field(
                    'description',
                    label_class='block text-sm font-medium text-gray-700 mb-2',
                    placeholder="Additional details about the asset...",
                    css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                )
            )
        )
        self.fields['employee'].querset = Staff.objects.all().order_by('first_name')

class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'department', 'position', 'address', 'location', 'phone_number', 'start_date', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Field(
                        "first_name",
                        label_class="block text-sm font-medium text-gray-700 mb-2",
                        css_class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all",
                        placeholder="Enter first name"
                    )
                ),
                Div(
                    Field(
                        "last_name",
                        label_class="block text-sm font-medium text-gray-700 mb-2",
                        css_class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all",
                        placeholder="Enter last name"
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Field(
                    "email",
                    label_class="block text-sm font-medium text-gray-700 mb-2",
                    css_class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all",
                    placeholder="employee@assettrack.com"
                )
            ),
            Div(
                Div(
                    Field(
                        "department",
                        label_class="block text-sm font-medium text-gray-700 mb-2",
                        css_class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    )
                ),
                Div(
                    Field(
                        "position",
                        label_class="block text-sm font-medium text-gray-700 mb-2",
                        css_class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all",
                        placeholder="e.g., HR Assistant"
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Div(
                    Field(
                        "phone_number",
                        label_class="block text-sm font-medium text-gray-700 mb-2",
                        css_class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all",
                        placeholder="+63 912-345-6789"
                    )
                ),
                Div(
                    Field(
                        "start_date",
                        label_class="block text-sm font-medium text-gray-700 mb-2",
                        css_class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Field(
                    "location",
                    label_class="block text-sm font-medium text-gray-700 mb-2",
                    css_class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all",
                    placeholder="e.g., Building A, Floor 3"
                )
            ),
            Div(
                Field(
                    "notes",
                    label_class="block text-sm font-medium text-gray-700 mb-2",
                    css_class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all",
                    placeholder="Additional notes about the employee..."
                )
            ),
        )

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['supplier', 'department', 'status', 'date_expected', 'instruction', 'track_id']
        labels = {
            'supplier': 'Supplier/Store',
            'department': 'Department/Requisitor'
        }
        widgets = {
            'date_expected': forms.DateInput(attrs={'type':'date'}),
            'instruction': forms.Textarea(attrs={'row': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('track_id', type='hidden'),
            Div(
                Div(
                    Field(
                        'supplier',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        placeholder='e.g., Walter',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                Div(
                    Field(
                        'department',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        placeholder='Select department',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Div(
                    Field(
                        'date_expected',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                Div(
                    Field(
                        'status',
                        label_class='block text-sm font-medium text-gray-700 mb-2',
                        css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                    )
                ),
                css_class="grid grid-cols-1 md:grid-cols-2 gap-6"
            ),
            Div(
                Field(
                    'instruction',
                    label_class='block text-sm font-medium text-gray-700 mb-2',
                    placeholder='Add reminders for the order',
                    css_class='w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all'
                ),
            )
        )

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity', 'price']
        widgets = {
            'item': forms.TextInput(attrs={'placeholder': 'eg. Macbook 16'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'value': 1}),
            'price': forms.NumberInput(attrs={'step':'0.01', 'min': 0, 'placeholder': '0.00' })
        }
        labels = {
            'item': 'Item Name'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('id', type='hidden'),
            Field('order', type='hidden'),
            Field('DELETE', type='hidden'),
            Div(
                Field(
                    'item',
                    css_class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all text-sm"
                ),
                css_class="md:col-span-2"
            ),
            Div(
                Field(
                    'quantity',
                    css_class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all text-sm"
                )
            ),
            Div(
                Field(
                    'price',
                    css_class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all text-sm"
                )
            )
        )

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True,
)

