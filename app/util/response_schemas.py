# from app.db import schemas
#
# {
#     400: {"model": schemas.Message, "description": "Bad Request"}
# }

base_responses = {
    400: {"description": "Bad Request"},
    401: {"description": "Unauthorized"},
    404: {"description": "Not Found"},
    422: {"description": "Validation Error"},
    500: {"description": "Internal Server Error"}
}

general_responses = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"message": "success"}
            }
        },
    }
}

all_users_responses = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"total_pages": 0,
                            "total_items": 0,
                            "page_data": {"page_num": 0,
                                          "items_count": 0,
                                          "items":
                                              [{
                                                  "id": 0,
                                                  "first_name": "string",
                                                  "email": "string",
                                                  "is_admin": "string",
                                                  "created_by_userid": "string",
                                                  "created_timestamp": "string"}]}}
            }
        },
    }
}

all_keys_responses = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"total_pages": 0,
                            "total_items": 0,
                            "page_data": {"page_num": 0,
                                          "items_count": 0,
                                          "items":
                                              [{
                                                  "created_by_userid": 0,
                                                  "key_id": "string",
                                                  "user_id": "string",
                                                  "created_timestamp": "string"}]}}
            }
        },
    }
}


all_filter_comparison_responses = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"total_pages": 0,
                            "total_items": 0,
                            "page_data": {"page_num": 0,
                                          "items_count": 0,
                                          "items":
                                              [{
                                                  "id": "string",
                                                  "text_sample_id_1": "string",
                                                  "text_sample_id_2": "string",
                                                  "item_1_is_better": "bool",
                                                  "user_id": "string",
                                                  "created_timestamp": "string"}]}}
            }
        },
    }
}

create_filter_comparison = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"text_sample_1": "string",
                            "text_sample_2": "string",
                            "comparison_id": "string"}
            }
        },
    }
}


get_token_response = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"access_token": "string",
                            "token_type": "string"}
            }
        },
    }
}

login_response = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {"access_token": "string",
                            "token_type": "string",
                            "session_id": "string",
                            "user": {
                                "id": 0, "first_name": "string"
                                , "email": "string"
                                , "is_active": "string"
                                , "is_admin": "string"
                                , "created_by_userid": "string"
                                , "created_timestamp": "string"}}
            }
        },
    }
}

single_users_responses = {
    **base_responses,
    200: {
        "content": {
            "application/json": {
                "example": {
                    "id": 0, "first_name": "string"
                    , "email": "string"
                    , "is_active": "string"
                    , "is_admin": "string"
                    , "created_by_userid": "string"
                    , "created_timestamp": "string"}
            }
        },
    }
}