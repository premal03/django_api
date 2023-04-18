from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'limit'
    max_page_size = 5
