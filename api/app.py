from bottle import Bottle, response
from pydantic import ValidationError

app = Bottle()

def exception_middleware(route):
    def route_wrapper(*args, **kwargs):
        response.content_type = 'application/json'
        try:
            output = route(*args, **kwargs)
        except (ValidationError, ValueError) as e:
            response.status = 400
            return {'error': str(e)}
        return output
    return route_wrapper
