from .models import SiteUser, Offer, OfferMatch
from .maps import distance_between_locations


def calculate_match_value(offer, user):
    distance = distance_between_locations(offer.start_location, user.location)
    p_distance = (1.0/(1.0+distance/100.0))
    return p_distance


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
