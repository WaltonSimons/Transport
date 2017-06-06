from .models import Category, CargoType


def get_categories():
    categories = Category.objects.all()
    parent_categories = [cat for cat in categories if cat.parentCategory is None]
    res = []
    for parent in parent_categories:
        children = []
        for cat in categories:
            if cat.parentCategory == parent:
                children.append(cat)
        res.append((parent.name, map(lambda c: (c.pk, c.name), children)))
    return res


def get_cargo_types():
    cargo_types = CargoType.objects.all()
    return [(c.pk, c.name) for c in cargo_types]
