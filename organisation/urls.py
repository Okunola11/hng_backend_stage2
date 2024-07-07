from django.urls import path
from .views import OrganisationDetailView, OrganisationListCreateView, AddUserToOrganisationView

urlpatterns = [
    path('api/organisations', OrganisationListCreateView.as_view(), name='organisation-list-create'),
    path('api/organisations/<str:orgId>', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('api/organisations/<str:orgId>/users', AddUserToOrganisationView.as_view(), name='add-to-organisation'),
]
