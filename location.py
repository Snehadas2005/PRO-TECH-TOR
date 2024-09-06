import geocoder

def get_current_location():
    g = geocoder.ip('me')  # Fetches the location using the IP address
    return g.latlng

# Call the function
location = get_current_location()

if location:
    print(f"Current location: Latitude: {location[0]}, Longitude: {location[1]}")
else:
    print("Unable to fetch the location.")
