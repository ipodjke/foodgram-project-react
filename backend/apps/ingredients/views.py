from utils.filters import DoubleSearchBackend
from utils.views import ListRetriveViewSet

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientsViewSet(ListRetriveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DoubleSearchBackend]
    search_fields = ['^name', '$name']
