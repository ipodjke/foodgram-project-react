from rest_framework import mixins, viewsets


class ListRetriveViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    pass
