import deform
from deform.form import Button
from chameleon.zpt.template import PageTemplateFile
from horseman.mapping import RootNode
from horseman.exceptions import HTTPError
from knappe.decorators import context, html, json, composed, trigger
from knappe.request import RoutingRequest as Request
from knappe.response import Response
from knappe.routing import Router
from knappe.pipeline import Pipeline
from knappe.meta import HTTPMethodEndpointMeta
from .ui import themeUI
from .forms import LoginForm, trigger
from functools import cached_property


router = Router()


class Application(RootNode):

    def __init__(self, router=router, middlewares=(), config=None):
        self.config = config
        self.router = router
        self.pipeline: Pipeline[Request, Response] = Pipeline(middlewares)

    def resolve(self, path_info, environ):
        endpoint = self.router.match_method(
            path_info, environ['REQUEST_METHOD'])
        request = Request(environ, app=self, endpoint=endpoint)
        request.context['ui'] = themeUI
        return self.pipeline(endpoint.handler)(request)


def get_document(request):
    if request.params['docid'] == '1':
        return {
            'id': 1,
            'name': 'test',
            'data': 'some data'
        }
    raise LookupError('Could not find the document.')


@router.register('/doc/{docid}')
class DocumentView(metaclass=HTTPMethodEndpointMeta):

    @json
    @context(get_document)
    def GET(self, request: Request, document: dict) -> dict:
        return document


@router.register('/')
@html('index')
def index(request):
    return {}


@router.register('/login')
class Login(metaclass=HTTPMethodEndpointMeta):

    def __init__(self):
        print('I compute the actions and buttons')
        triggers = trigger.in_order(self)
        self.actions = {('trigger', t.value): m for t, m in triggers}
        self.buttons = tuple((
            deform.form.Button(
                name='trigger',
                title=t.title,
                value=t.value,
                css_class=t.css_class,
                icon=t.icon,
            ) for t, m in triggers
        ))

    def get_form(self, request):
        schema = LoginForm().bind(request=request)
        return deform.form.Form(schema, buttons=self.buttons)

    @html('form')
    def GET(self, request):
        form = self.get_form(request)
        return {
            "error": None,
            "rendered_form": form.render()
        }

    @trigger('cancel', title="Cancel")
    def cancel(self, request, form):
        return Response.redirect('/')

    @trigger('process', title="Process")
    @html('form')
    def process_credentials(self, request, form):
        try:
            appstruct = form.validate(request.data.form)
            auth = request.context['authentication']
            user = auth.from_credentials(request, appstruct)
            if user is not None:
                auth.remember(request, user)
                return Response.redirect("/")

            return {
                "error": "Login failed.",
                "rendered_form": form.render()
            }
        except deform.exception.ValidationFailure as e:
            return {
                "error": None,
                "rendered_form": e.render()
            }

    def POST(self, request):
        form = self.get_form(request)
        found = tuple(set(self.actions) & set(request.data.form))
        if len(found) != 1:
            raise HTTPError(
                400, body='Could not resolve an action for the form.')
        action = self.actions[found[0]]
        return action(request, form)
