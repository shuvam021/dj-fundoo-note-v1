from rest_framework.response import Response


def ApiResponse(data=None, status=None, msg=""):
    message_switcher = {
        200: "Data fetch successful",
        201: "Create or Update successful",
        204: "Delete successful",
        404: "User doesn't exist"
    }
    status_list = list(message_switcher.keys())
    mod_data = {
        'status': status,
        'message': message_switcher.get(status) if status in status_list else msg,
        'data': data
    }
    return Response(data=mod_data, status=status)
