from rest_framework import pagination


class ChiaTrangPaginator(pagination.PageNumberPagination):
    page_size = 6