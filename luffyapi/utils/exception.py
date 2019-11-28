from rest_framework.views import exception_handler as exc_handler
from rest_framework.response import Response
from utils.logging import logger


# 自定义异常
def exception_handler(exc, context):
    """自定义异常"""
    response = exc_handler(exc, context)

    logger.error('%s - %s - %s' % (context['view'], context['request'].method, exc))

    if response is None:
        return Response({'detail': '%s' % exc}, status=500, exception=True)

    return response
