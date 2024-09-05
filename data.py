import flet as ft
import time
import threading
import json
import os
from audio import AudioProcessor
from image import ImageProcessor
from location import LocationApp
from server import start_server

class DataPage(ft.UserControl):
    def __init__(self, go_back):
        super().__init__()
        self.go_back = go_back
        self.location = ft.TextField(label="Location", read_only=True)
        self.image = ft.Image(src=None, width=300, height=300, fit=ft.ImageFit.CONTAIN)
        self.video = ft.TextField(label="Video", read_only=True)
        self.audio = ft.TextField(label="Audio", read_only=True)
        self.status = ft.Text("Waiting for data...")
        self.received_images = []
        self.current_image_index = 0

        # Initialize processors
        self.audio_processor = AudioProcessor()
        self.image_processor = ImageProcessor()
        self.location_app = LocationApp()

        # Load previous data
        self.load_previous_data()

        # Start the server in a separate thread
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        # Start periodic updates
        self.update_thread = threading.Thread(target=self.periodic_update)
        self.update_thread.daemon = True
        self.update_thread.start()

    def build(self):
        data_title = ft.Text("Data", size=20, weight="bold")
        back_button = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.go_back)
        next_button = ft.ElevatedButton("Next Image", on_click=self.next_image)
        prev_button = ft.ElevatedButton("Previous Image", on_click=self.prev_image)
        
        return ft.Column([
            ft.Row([back_button, data_title], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.location,
            self.image,
            ft.Row([prev_button, next_button]),
            self.video,
            self.audio,
            self.status
        ])

    def run_server(self):
        start_server(self.handle_incoming_data)

    def handle_incoming_data(self, data_type, data):
        if data_type == "image":
            self.image_processor.process_image(data)
            self.received_images.append(data)
            self.update_image()
        elif data_type == "audio":
            self.audio_processor.process_audio(data)
            self.audio.value = f"New audio received: {len(data)} bytes"
        elif data_type == "video":
            # Assuming video processing is similar to image
            self.video.value = f"New video received: {len(data)} bytes"
        self.save_data()
        self.update()

    def periodic_update(self):
        while True:
            self.fetch_location()
            self.update()
            time.sleep(60)  # Update every minute

    def fetch_location(self):
        try:
            latitude, longitude = self.location_app.get_location()
            self.location.value = f"Lat: {latitude}, Long: {longitude}"
        except Exception as e:
            self.location.value = f"Error fetching location: {str(e)}"

    def update_image(self):
        if self.received_images:
            self.image.src = self.received_images[self.current_image_index]
            self.status.value = f"Displaying image {self.current_image_index + 1} of {len(self.received_images)}"
        else:
            self.status.value = "No images received yet"

    def next_image(self, e):
        if self.received_images:
            self.current_image_index = (self.current_image_index + 1) % len(self.received_images)
            self.update_image()

    def prev_image(self, e):
        if self.received_images:
            self.current_image_index = (self.current_image_index - 1) % len(self.received_images)
            self.update_image()

    def load_previous_data(self):
        if os.path.exists("data_storage.json"):
            with open("data_storage.json", "r") as f:
                data = json.load(f)
                self.received_images = data.get("images", [])
                self.audio.value = data.get("audio", "")
                self.video.value = data.get("video", "")
                self.location.value = data.get("location", "")

    def save_data(self):
        data = {
            "images": self.received_images,
            "audio": self.audio.value,
            "video": self.video.value,
            "location": self.location.value
        }
        with open("data_storage.json", "w") as f:
            json.dump(data, f)

def main(page: ft.Page):
    def go_back(e):
        print("Going back")

    page.add(DataPage(go_back))

ft.app(target=main)