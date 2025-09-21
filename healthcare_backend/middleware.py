from django.http import JsonResponse
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """Handle unhandled exceptions"""
        logger.error(f"Unhandled exception: {str(exception)}", exc_info=True)
        
        return JsonResponse({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred. Please try again later.',
            'status_code': 500
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
