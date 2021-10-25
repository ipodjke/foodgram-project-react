from utils.views import ListRetriveViewSet

from .models import Tag
from .serializers import TagSerializer


class TagsViewSet(ListRetriveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
