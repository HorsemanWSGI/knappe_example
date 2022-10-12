from knappe.blueprint import Blueprint
from knappe.decorators import context, html, json
from knappe.meta import HTTPMethodEndpointMeta
from knappe.routing import Router


views: Blueprint[Router] = Blueprint(Router)


def get_document(request):
    if request.params['docid'] == '1':
        return {
            'id': 1,
            'name': 'test',
            'data': 'some data'
        }
    raise LookupError('Could not find the document.')


@views.register('/doc/{docid}')
class DocumentView(metaclass=HTTPMethodEndpointMeta):

    @json
    @context(get_document)
    def GET(self, request, document: dict) -> dict:
        return document


@views.register('/')
@html('index')
def index(request):
    return {}
