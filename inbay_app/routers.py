import re
import threading 
request_cfg = threading.local()


class RouterMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.process_request(request)
    
    def process_request( self, request):
        role = None
        
        if request.POST:
            role = request.POST.get('role')
        db_name = 'default'
        if role:
            db_name = f'{role}_db'
        request_cfg.cfg = db_name
        
        return None

    def process_response( self, request, response ):
        if hasattr( request_cfg, 'cfg' ):
            del request_cfg.cfg
        return response


class DatabaseRouter (object):
    def _default_db( self ):
        print("request_cfg",request_cfg)
        if hasattr( request_cfg, 'cfg' ):
            return request_cfg.cfg
        else:
            return 'default'

    def db_for_read( self, model, **hints ):
        return self._default_db()

    def db_for_write( self, model, **hints ):
        return self._default_db()