import colander
import deform
from knappe.annotations import annotation
from typing import NamedTuple


class Button(NamedTuple):
    name: str
    title: str
    value: str
    css_class: str = None
    icon: str = None


class trigger(annotation):
    name = "__trigger__"

    def __init__(self, value,
                 title: str = None, icon: str = None, css_class = None):
        self.key = value
        self.annotation = Button(
            name='trigger',
            title=title,
            value=value,
            css_class=css_class,
            icon=icon
        )

    @classmethod
    def buttons_actions(cls, form):
        buttons = []
        actions = {}
        for button, action in cls.find(form):
            buttons.append(
                deform.form.Button(**button._asdict())
            )
            key = (button.name, button.value)
            if key in actions:
                raise KeyError(f'Button defined twice: {button}')
            actions[key] = action

        return buttons, actions


class LoginForm(colander.Schema):

    username = colander.SchemaNode(
        colander.String(),
        title="Login")

    password = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.PasswordWidget(),
        title="Password",
        description="Your password")
