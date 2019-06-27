from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        # import pdb; pdb.set_trace()
        request_data = args[0].request.data
        
        name = request_data.get("name", "")
        isbn = request_data.get("isbn", "")
        authors = request_data.get("authors")
        message = ''
        if len(request_data) == 0:
            message = "No parameters provided"
        
        return Response(
                data={
                    "message": message
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated


def response_builder(status_code, status_msg, data, msg=''):
    res = {}
    res['status_code'] = status_code
    res['status'] = status_msg
    
    if msg:
        res['message'] = msg
    if not data:
        res['data'] = []
        return res
    if isinstance(data, list):
        for d in data:
            # d['authors'] = d['authors'].split(',')
            res['data'] = data
    else:
        if 'authors' in data:
            # data['authors'] = data['authors'].split(',')
            res['data'] = [data]
        else:
            res['data'] = []
    return res


def request_to_dict(input_request):
    """
    used to convert querydict request data into pure dict object data
    """
    temp_dict = {}
    for key in input_request:
        temp_dict[key] = input_request[key]
    return temp_dict