from functools import partial
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

base_swagger = partial(
    swagger_auto_schema,
    )

get_list_swagger = base_swagger(
            operation_description="Get a list of all todo items",
            responses={200: "نتایج با موفقیت نمایش داده شد."}
            )

post_register_swagger = base_swagger(
            operation_description="Register a user with email, password and username",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
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
                    'username': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Enter username",
                        example="admin"
                    ),
                },
                required=['email', 'password', 'username']
            ),
            responses={
                201: openapi.Response(
                    description="Token response",
                    examples={'application/json': {
                        "token": {'refresh': "your_refresh_token_here", 'access': "your_access_token_here"}
                    }}
                ),
                400: "Bad request"
                },
            )