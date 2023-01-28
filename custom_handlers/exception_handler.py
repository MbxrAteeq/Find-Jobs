from rest_framework.views import exception_handler
import logging
logger = logging.getLogger(__name__)


def core_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        response = _convert_to_custom_error_format(response)
        return response
    else:
        return None


def _convert_to_custom_error_format(response):
    if isinstance(response.data, list):
        data = dict()
        data['message'] = "\n".join(response.data)
        data['code'] = response.status_code
        response.data = data
        return response
    detail = response.data.get('detail')
    if detail:
        del response.data['detail']
    elif response.data.get('error'):
        error = response.data.get('error')
        if isinstance(error, (list, tuple)):
            detail = "\n".join(error)
        elif isinstance(error, str):
            detail = error
        else:
            detail = ""
        del response.data['error']
    response.data['message'] = detail
    response.data['status'] = response.status_code
    return response
