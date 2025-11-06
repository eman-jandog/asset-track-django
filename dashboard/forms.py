from django import  forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from .models import Asset, Order, Staff


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

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['asset','order_quantity']