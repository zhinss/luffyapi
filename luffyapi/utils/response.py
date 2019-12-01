from rest_framework.response import Response


# 自定义APIResponse返回类
class APIResponse(Response):
    """自定义APIResponse返回类"""
    def __init__(self, data_status=0, data_msg='ok', results=None,
                 http_status=None, headers=None, exception=False, **kwargs):
        data = {
            'status': data_status,
            'msg': data_msg,
        }
        if results is not None:
            data['results'] = results
        data.update(kwargs)

        super().__init__(data=data, status=http_status, headers=headers, exception=exception)