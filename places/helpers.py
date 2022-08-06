from django.core.paginator import (
    Paginator,
    InvalidPage
)


def paginate(paginate_by, objects, request) -> dict:
    is_paginated = False

    if objects.count() > paginate_by:

        page = request.GET.get('page', 1)
        paginator = Paginator(objects, paginate_by)
        page_obj = paginator.get_page(page)

        try:
            objects = paginator.page(page)
        except InvalidPage:
            objects = paginator.page(1)

        is_paginated = True


        return {'is_paginated': is_paginated, 'page_obj': page_obj, 'places': objects}

    return {'is_paginated': is_paginated, 'places': objects}
