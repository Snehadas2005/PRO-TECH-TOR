import geocoder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class LocationApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        self.lat_label = Label(text="Latitude: Fetching...")
        self.long_label = Label(text="Longitude: Fetching...")
        self.button = Button(text="Fetch Location", on_press=self.get_location)
        
        self.layout.add_widget(self.lat_label)
        self.layout.add_widget(self.long_label)
        self.layout.add_widget(self.button)
        
        return self.layout

    def get_location(self, instance):
        g = geocoder.ip('me')
        location = g.latlng
        if location:
            self.lat_label.text = f"Latitude: {location[0]}"
            self.long_label.text = f"Longitude: {location[1]}"
            Lat_itude=location[0]
            Long_itude=location[1]
            print("Lattitude: ",Lat_itude)
            print("Longitude: ",Long_itude)
        else:
            self.lat_label.text = "Unable to fetch location"
            self.long_label.text = ""

if __name__ == "__main__":
    LocationApp().run()
