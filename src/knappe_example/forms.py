import colander
import deform
from knappe.annotations import annotation
from typing import NamedTuple, Iterator


class Trigger(NamedTuple):
    title: str
    value: str
    css_class: str = None
    icon: str = None
    order: int = 0


class trigger(annotation):
    name = "__trigger__"

    def __init__(self,
                 value,
                 title: str = None,
                 icon: str = None,
                 css_class = None,
                 order: int = 10,

                 ):
        self.annotation = Trigger(
            title=title,
            value=value,
            css_class=css_class,
            icon=icon,
            order=order,
        )

    @classmethod
    def in_order(cls, component):
        return sorted(trigger.find(component), key=lambda x: x[0].order)


class LoginForm(colander.Schema):

    username = colander.SchemaNode(
        colander.String(),
        title="Login")

    password = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.PasswordWidget(),
        title="Password",
        description="Your password")
