from django.urls import path

from .views import (
    EmployeeStatistic,
    ClientStatistic,
    EmployeesStatistic,
)

urlpatterns = [
    path('statistics/employee/<int:pk>/', EmployeeStatistic.as_view(), name="employee_statistic"),
    path('statistics/client/<int:pk>/', ClientStatistic.as_view(), name="client_statistic"),
    path('employee/statistics/', EmployeesStatistic.as_view(), name="employees_statistic"),
]
