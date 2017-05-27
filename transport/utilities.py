from .models import Category


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
