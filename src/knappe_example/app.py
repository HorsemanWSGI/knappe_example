from horseman.mapping import RootNode
from knappe.pipeline import Pipeline
from knappe.request import RoutingRequest as Request
from knappe.routing import Router
from .ui import themeUI


class Application(RootNode):

    def __init__(self, middlewares=(), config=None):
        self.config = config
        self.router = Router()
        self.pipeline: Pipeline[Request, Response] = Pipeline(middlewares)

    def resolve(self, path_info, environ):
        endpoint = self.router.match_method(
            path_info, environ['REQUEST_METHOD'])
        request = Request(environ, app=self, endpoint=endpoint)
        request.context['ui'] = themeUI
        return self.pipeline(endpoint.handler)(request)
