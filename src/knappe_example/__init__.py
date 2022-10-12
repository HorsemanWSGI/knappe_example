from knappe.plugins import Plugin
from .views import views
from .forms import forms


Example = Plugin('my example', blueprints={
    'router': views | forms
})
