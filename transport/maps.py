from .models import Location
import geocoder


def get_coordinates(name, postcode):
    return geocoder.google(name + ' ' + postcode).latlng


def distance_between_coordinates(coord1, coord2):
    return geocoder.distance(coord1, coord2)  # km


def get_location_model(name, postcode):
    query = Location.objects.filter(name=name, postcode=postcode)
    location = query[0] if len(query) != 0 else None
    if location is None:
        location = Location()
        location.name = name
        location.postcode = postcode
        coordinates = get_coordinates(name, postcode)
        location.latitude = coordinates[0]
        location.longitude = coordinates[1]
        location.save()
    return location


def distance_between_locations(location1, location2):
    coord1 = [location1.latitude, location1.longitude]
    coord2 = [location2.latitude, location2.longitude]
    return distance_between_coordinates(coord1, coord2)
