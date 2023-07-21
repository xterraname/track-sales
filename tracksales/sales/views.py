from django.db.models import Sum, F, Count, Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import *
from .serializers import (
    MonthYearSerializer,
    EmployeeStatisticSerializer,
    ClientStatisticSerializer,
    EmployeesStatisticSerializer,
)

month_param = OpenApiParameter(
    'month', required=False,
    type=OpenApiTypes.NUMBER,
    location=OpenApiParameter.QUERY
)

year_param = OpenApiParameter(
    'year', required=False,
    type=OpenApiTypes.NUMBER,
    location=OpenApiParameter.QUERY
)


@extend_schema(parameters=[month_param, year_param])
class EmployeeStatistic(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeStatisticSerializer

    def retrieve(self, request, *args, **kwargs):
        orders = get_orders_by_date(
            self.request, query={'employee': self.get_object()})

        self.queryset = self.queryset.annotate(
            total_clients=Count('orders__client', distinct=True,
                                filter=Q(orders__in=orders)),
            total_products=Sum('orders__products__quantity',
                               filter=Q(orders__in=orders)),
            total_amount=Sum(F('orders__products__quantity') *
                             F('orders__products__product__price'),
                             filter=Q(orders__in=orders))
        )

        return super().retrieve(request, *args, **kwargs)


@extend_schema(parameters=[month_param, year_param])
class ClientStatistic(RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientStatisticSerializer

    def retrieve(self, request, *args, **kwargs):
        orders = get_orders_by_date(
            self.request, query={'client': self.get_object()})

        self.queryset = self.queryset.annotate(
            total_products=Sum('orders__products__quantity',
                               filter=Q(orders__in=orders)),
            total_amount=Sum(F('orders__products__quantity') *
                             F('orders__products__product__price'),
                             filter=Q(orders__in=orders))
        )

        return super().retrieve(request, *args, **kwargs)
    

@extend_schema(parameters=[month_param, year_param])
class EmployeesStatistic(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeesStatisticSerializer

    def get_queryset(self):
        queryset = self.queryset

        orders = get_orders_by_date(self.request)

        queryset = queryset.annotate(
            total_clients=Count(
                'orders__client',
                distinct=True,
                filter=Q(orders__in=orders)),
            total_products=Sum(
                'orders__products__quantity',
                filter=Q(orders__in=orders)),
            total_amount=Sum(
                F('orders__products__quantity') *
                F('orders__products__product__price'),
                filter=Q(orders__in=orders)
            )
        )

        return queryset


def get_orders_by_date(request, query={}):
    date_serializer = MonthYearSerializer(data=request.GET)

    if not date_serializer.is_valid():
        return Response(date_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    month = date_serializer.validated_data.get('month', None)
    year = date_serializer.validated_data['year']

    query['date__year'] = year
    if month:
        query['date__month'] = month

    return Order.objects.filter(**query)
