from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from .models import Organisation
from .serializers import OrganisationSerializer


class OrganisationListView(ListAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organisation.objects.filter(users=self.request.user)

class OrganisationDetailView(RetrieveAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(users=self.request.user)

class OrganisationCreateView(CreateAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]
