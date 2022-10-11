import deform
from deform.form import Button
from chameleon.zpt.template import PageTemplateFile
from horseman.mapping import RootNode
from horseman.exceptions import HTTPError
from knappe.decorators import context, html, json, composed
from knappe_deform import trigger
from knappe.request import RoutingRequest as Request
from knappe.response import Response
from knappe.routing import Router
from knappe.pipeline import Pipeline
from knappe.meta import HTTPMethodEndpointMeta
from knappe_deform import FormPage
from .ui import themeUI
from .forms import LoginSchema
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
class Login(FormPage):

    schema = LoginSchema

    @trigger('cancel', title="Cancel")
    def cancel(self, request):
        return Response.redirect('/')

    @trigger('process', title="Process")
    def process_credentials(self, request):
        try:
            form = self.get_form(request)
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
