from functools import partial
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

base_swagger = partial(
    swagger_auto_schema,
    )

common_response = openapi.Response(
                description="Token response",
                examples={'application/json': {
                    "token": {'refresh': "your_refresh_token_here", 'access': "your_access_token_here"}
                }}
            )

RESPONSES_DICT_USER = {
    201: common_response,
    200: common_response,
    400: "Bad request",
}

RESPONSES_DICT_TODO ={
    200: "ok",
    201: "Created successfully",
    204: "No content",
    404: "Not found",
    400: "Bad request"
}

def get_user_request_body(include_name=False):
    properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Enter a valid email",
                    example="admin@gmail.com",
                    format=openapi.FORMAT_EMAIL
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Enter a password",
                    example="1234@abc"
                ),
            }
    if include_name:
        properties['name'] = openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Enter a name",
                    example="Elham"
                )
    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=properties,
            required=['email', 'password']
        )
    return request_body

def get_todo_request_body():
    request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Enter a tite",
                    example="This is a title"
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Enter description",
                    example="This is description"
                ),
            },
        )
    return request_body
    
def get_authentication_parameters():
    return[
        openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True
            )
    ]

def get_path_parameters():
    return[
        openapi.Parameter(
                'Id',
                openapi.IN_PATH,
                description="ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
    ]

def get_query_parameters():
    return[
        openapi.Parameter('title', openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING),
        openapi.Parameter('description', openapi.IN_QUERY, description="Filter by description", type=openapi.TYPE_STRING),
        openapi.Parameter('ordering', openapi.IN_QUERY, description="Sort by field", type=openapi.TYPE_STRING),
    ]

get_list_swagger = base_swagger(
            operation_description="""Get a list of all to-do items with filtering and sorting options.
                                     Only authenticated users can access this.
                                     Limited to 5 requests per minute.""",
            responses={200: RESPONSES_DICT_TODO[200]},
            manual_parameters=get_authentication_parameters() + get_query_parameters()
            )

post_register_swagger = base_swagger(
            operation_description="Register a user with email and password and name",
            request_body=get_user_request_body(include_name=True),
            responses={
                201: RESPONSES_DICT_USER[201],
                400: RESPONSES_DICT_USER[400]
                },
            )

post_login_swagger = base_swagger(
            operation_description="Login a user with email and password",
            request_body=get_user_request_body(include_name=False),
            responses={
                200: RESPONSES_DICT_USER[200],
                400: RESPONSES_DICT_USER[400]
                },
            )

post_todo_swagger = base_swagger(
            operation_description="Create a todo with title and description",
            request_body=get_todo_request_body(),
            manual_parameters=get_authentication_parameters(),
            responses={
                201: RESPONSES_DICT_TODO[201],
                400: RESPONSES_DICT_TODO[400]
                },
            )

put_todo_swagger = base_swagger(
            operation_description="Update an existing todo. only authenticated user who is owner can update this",
            request_body=get_todo_request_body(),
            manual_parameters=get_authentication_parameters(),
            responses={
                200: RESPONSES_DICT_TODO[200],
                400: RESPONSES_DICT_TODO[400],
                404: RESPONSES_DICT_TODO[404]
                },
            )

delete_todo_swagger = base_swagger(
            operation_description="Delete an existing todo. only authenticated user who is owner can delete this",
            manual_parameters=get_authentication_parameters() + get_path_parameters(),
            responses={
                204: RESPONSES_DICT_TODO[204],
                404: RESPONSES_DICT_TODO[404]
                },
            )
