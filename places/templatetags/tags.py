from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='has_reservation')
def has_reservation(user, place_id):
    for reservation in user.reservations.all():
        if reservation.place_id == place_id:
            return True
    return False
