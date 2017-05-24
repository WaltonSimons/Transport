from .models import SiteUser, Offer, OfferMatch
from .maps import distance_between_locations


def calculate_match_value(offer, user):
    # values is a list of tuples - (value, weight)
    values = []
    distance = distance_between_locations(offer.start_location, user.location)
    p_distance = (1.0 / (1.0 + distance / 100.0))
    values.append((p_distance, 1))

    p_cargo_weight = calculate_cargo_weight_match(offer.weight, user.vehicles.all()[0].max_capacity)
    values.append((p_cargo_weight, 0.5))

    p_cargo_dimensions = calculate_cargo_dimensions_match(user.vehicles.all()[0], offer.length, offer.width, offer.height)
    values.append((p_cargo_dimensions, 0.7))

    res = sum([x * y for x, y in values]) / sum([y for x, y in values])
    return res


def create_match(offer, user):
    query = OfferMatch.objects.filter(user=user, offer=offer)
    if not query:
        match = OfferMatch()
        match.offer = offer
        match.user = user
        match.value = calculate_match_value(offer, user)
        match.save()
        return match
    return query[0]


def calculate_cargo_weight_match(offer_cargo_weight, user_max_capacity):
    if user_max_capacity < offer_cargo_weight:
        return 0
    return 1.0 / ((1.0 + user_max_capacity - offer_cargo_weight) % 100.0)


def calculate_cargo_dimensions_match(user_vehicle, offer_cargo_length, offer_cargo_width, offer_cargo_height):
    if user_vehicle.length < offer_cargo_length or user_vehicle.width < offer_cargo_width or user_vehicle.height < offer_cargo_height:
        return 0
    p_length = 1.0 / ((1.0 + user_vehicle.length - offer_cargo_length) % 100.0)
    p_width = 1.0 / ((1.0 + user_vehicle.width - offer_cargo_width) % 100.0)
    p_height = 1.0 / ((1.0 + user_vehicle.height - offer_cargo_height) % 100.0)
    return (p_length + p_width + p_height) / 3.0
