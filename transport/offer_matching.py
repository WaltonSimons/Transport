from .models import SiteUser, Offer, OfferMatch
from .maps import distance_between_locations
from django.utils import timezone

def calculate_match_value(offer, user):
    # values is a list of tuples - (value, weight)
    prefs = user.preferences

    values = []
    distance = distance_between_locations(offer.start_location, user.location)
    p_distance = (1.0 / (1.0 + distance / 100.0))
    values.append((p_distance, prefs.distance_to_start))

    if user.has_vehicle():
        p_cargo_weight = get_highest_for_vehicles(user.vehicles.all(), offer, calculate_cargo_weight_match)
        values.append((p_cargo_weight, prefs.cargo_weight))

        p_cargo_dimensions = get_highest_for_vehicles(user.vehicles.all(), offer,
                                                      calculate_cargo_dimensions_match)
        values.append((p_cargo_dimensions, prefs.cargo_dimension))

    p_longest_pickup = calculate_longest_pickup(offer.earliest_pickup, offer.latest_pickup)
    values.append((p_longest_pickup, prefs.longest_pickup))

    p_longest_delivery = calculate_longest_pickup(offer.earliest_delivery, offer.latest_delivery)
    values.append((p_longest_delivery, prefs.longest_delivery))

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


def get_highest_for_vehicles(vehicle_list, offer, function):
    return max([function(vehicle, offer) for vehicle in vehicle_list])


def calculate_cargo_weight_match(vehicle, offer):
    user_max_capacity = vehicle.max_capacity
    offer_cargo_weight = offer.weight
    if user_max_capacity < offer_cargo_weight:
        return 0
    return 1.0 / ((1.0 + user_max_capacity - offer_cargo_weight) % 100.0)


def calculate_cargo_dimensions_match(vehicle, offer):
    offer_cargo_length = offer.length
    offer_cargo_width = offer.width
    offer_cargo_height = offer.width
    if vehicle.length < offer_cargo_length or vehicle.width < offer_cargo_width or vehicle.height < offer_cargo_height:
        return 0
    p_length = 1.0 / ((1.0 + vehicle.length - offer_cargo_length) % 100.0)
    p_width = 1.0 / ((1.0 + vehicle.width - offer_cargo_width) % 100.0)
    p_height = 1.0 / ((1.0 + vehicle.height - offer_cargo_height) % 100.0)
    return (p_length + p_width + p_height) / 3.0


def calculate_longest_pickup(earliest_pickup, latest_pickup):
    if latest_pickup < timezone.now():
        return 0
    if earliest_pickup < timezone.now():
        return ((latest_pickup - timezone.now()).days %101) / 100
    else:
        delay = ((earliest_pickup - timezone.now()).days %101) / 10
        interval = ((latest_pickup - earliest_pickup).days %101)
        if interval <= delay:
            return 0
        else:
            return (interval - delay) / 100


def calculate_longest_delivery(earliest_delivery, latest_delivery):
    if latest_delivery < timezone.now():
        return 0
    if earliest_delivery < timezone.now():
        return ((latest_delivery - timezone.now()).days %101) / 100
    else:
        delay = ((earliest_delivery- timezone.now()).days %101) / 10
        interval = ((latest_delivery - earliest_delivery).days %101)
        if interval <= delay:
            return 0
        else:
            return (interval - delay) / 100
