from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    """Custom pagination for messages - 20 messages per page"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        _= self.page.paginator.count
        return super().get_paginated_response(data)
