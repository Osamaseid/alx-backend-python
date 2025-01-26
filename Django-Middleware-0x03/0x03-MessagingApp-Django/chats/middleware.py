import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.utils import timezone

logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s',
    filemode='a',
)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = self._get_user(request)
        
        message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - User: {user} - Path: {request.path}"
        
        logger.info(message)
        
        response = self.get_response(request)
        return response

    def _get_user(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            return request.user.email
        return "Anonymous"
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lower_bound_time = time(9, 0, 0) 
        upper_bound_time = time(18, 0, 0)
        now = timezone.now()
        time_now = now.time()
        if time_now < lower_bound_time or time_now > upper_bound_time:
            return HttpResponseForbidden("Site not accessible")
        response = self.get_response(request)
        return response
    
class OffensiveLanguageMiddleware:
    message_count = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            ip = request.META['REMOTE_ADDR']
            current_time = time.time()
            self.message_count[ip] = [t for t in self.message_count[ip] if current_time - t < 60]

            if len(self.message_count[ip]) >= 5:
                return HttpResponseForbidden("403 Forbidden: Too many messages sent.")
            self.message_count[ip].append(current_time)

        response = self.get_response(request)
        return response
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            if request.user.role != 'admin':
                return HttpResponseForbidden(f"{request.user.get('role')} role not allowed.")
            else:
                response = self.get_response(request)
                return response
        return HttpResponseForbidden('Authentication needed')