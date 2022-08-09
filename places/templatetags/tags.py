from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, user_type):
    return user.user_type == user_type


@register.filter(name='has_reservation')
def has_reservation(user, place_id):
    if user.is_authenticated:
        for reservation in user.reservations.all():
            if reservation.place_id == place_id:
                return True
    return False
