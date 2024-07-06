from django.urls import path
from .views import OrganisationListView, OrganisationDetailView, OrganisationCreateView

urlpatterns = [
    path('api/organisations/', OrganisationListView.as_view(), name='organisation-list'),
    path('api/organisations/<int:org_id>/', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('api/organisations/', OrganisationCreateView.as_view(), name='organisation-create'),
]
