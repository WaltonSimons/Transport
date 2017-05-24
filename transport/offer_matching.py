from .models import SiteUser, Offer, OfferMatch
from .maps import distance_between_locations


def calculate_match_value(offer, user):
    # values is a list of tuples - (value, weight)
    values = []
    distance = distance_between_locations(offer.start_location, user.location)
    p_distance = (1.0/(1.0+distance/100.0))
    values.append((p_distance, 1))

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
