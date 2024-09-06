from twilio.rest import Client
import geocoder


# Twilio credentials (replace with your account details)
account_sid = 'AC07c5448faad898741565138342d94bcd'
auth_token = '89f922612e37c6f2766807dbd0eb599d'
twilio_number = '+14342647392'

def get_current_location():
    g = geocoder.ip('me')  # Fetches the location using the IP address
    return g.latlng

# Call the function
# List of contacts to send the SOS message to
contacts = [
    '+917017970296',  # Replace with the actual phone numbers
]

location = get_current_location()
if location:
    print(f"Current location: Latitude: {location[0]}, Longitude: {location[1]}")
else:
    print("Unable to fetch the location.")
# SOS message to be sent
sos_message = f"Current location: Latitude: {location[0]}, Longitude: {location[1]}.SOS! I'm in danger. Please help me immediately."

# Function to send SOS message
def send_sos_message():
    client = Client(account_sid, auth_token)
    
    for contact in contacts:
        message = client.messages.create(
            body=sos_message,
            from_=twilio_number,
            to=contact
        )
        print(f"Sent SOS message to {contact}: SID {message.sid}")

if __name__ == "__main__":
    send_sos_message()
