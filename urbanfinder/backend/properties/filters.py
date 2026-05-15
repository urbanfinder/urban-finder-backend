"""
django-filter filter sets for property search and listing.
"""

from django_filters import rest_framework as filters

from .models import Property


class PropertyFilter(filters.FilterSet):
    """
    Advanced filtering for property listings.
    Supports range queries on price, bedroom/bathroom counts,
    and exact/partial matching on text fields.
    """

    # Price range
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    # Spec ranges
    min_bedrooms = filters.NumberFilter(field_name="bedrooms", lookup_expr="gte")
    max_bedrooms = filters.NumberFilter(field_name="bedrooms", lookup_expr="lte")
    min_bathrooms = filters.NumberFilter(field_name="bathrooms", lookup_expr="gte")
    min_area = filters.NumberFilter(field_name="area_sq_ft", lookup_expr="gte")
    max_area = filters.NumberFilter(field_name="area_sq_ft", lookup_expr="lte")

    # Text filters
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    state = filters.CharFilter(field_name="state", lookup_expr="icontains")

    # Choice filters
    property_type = filters.ChoiceFilter(choices=Property.PropertyType.choices)
    furnishing = filters.ChoiceFilter(choices=Property.FurnishingStatus.choices)
    status = filters.ChoiceFilter(choices=Property.ListingStatus.choices)

    # Boolean filters
    is_verified = filters.BooleanFilter()
    negotiable = filters.BooleanFilter()

    class Meta:
        model = Property
        fields = [
            "min_price",
            "max_price",
            "min_bedrooms",
            "max_bedrooms",
            "min_bathrooms",
            "min_area",
            "max_area",
            "city",
            "state",
            "property_type",
            "furnishing",
            "status",
            "is_verified",
            "negotiable",
        ]
