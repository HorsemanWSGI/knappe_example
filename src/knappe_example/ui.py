import typing as t
import pathlib
from chameleon.zpt.template import PageTemplateFile
from chameleon.zpt.loader import TemplateLoader
from knappe.decorators import html
from knappe.ui import SlotExpr, slot, UI, Layout
from knappe.request import RoutingRequest as Request


PageTemplateFile.expression_types['slot'] = SlotExpr

TEMPLATES = TemplateLoader(
    str(pathlib.Path(__file__).parent / "templates"),
    default_extension=".pt"
)


@slot.register
@html('header')
def header(request: Request, view: t.Any, context: t.Any, name: t.Literal['header']):
    return {'title': 'This is a header'}


themeUI = UI(
    templates=TEMPLATES,
    layout=Layout(TEMPLATES['master']),
)
