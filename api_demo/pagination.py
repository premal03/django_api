from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'limit'
    max_page_size = 5


class CustomLimitPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 3


class CursorLimitPagination(CursorPagination):
    page_size = 3
    ordering = 'rollno'
