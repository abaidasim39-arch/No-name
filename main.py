import warnings
# Version warning ko hide karne ke liye
warnings.filterwarnings("ignore", category=UserWarning, module="requests")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.clock import Clock, mainthread
import threading
import requests
import time

class NetworkCheckerApp(App):
    def build(self):
        # Main vertical layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Status Label
        self.status_label = Label(text="ASIM Network Service: Stopped", font_size='18sp')
        layout.add_widget(self.status_label) # FIX: add_widget use kiya
        
        # Buttons ka horizontal layout
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        
        # Start Button
        self.start_btn = Button(text="Start Checking", background_color=(0, 1, 0, 1))
        self.start_btn.bind(on_press=self.start_service)
        btn_layout.add_widget(self.start_btn) # FIX: add_widget use kiya
        
        # Stop Button
        self.stop_btn = Button(text="Stop Checking", background_color=(1, 0, 0, 1))
        self.stop_btn.bind(on_press=self.stop_service)
        btn_layout.add_widget(self.stop_btn) # FIX: add_widget use kiya
        
        layout.add_widget(btn_layout) # FIX: add_widget use kiya
        
        # Windows control flag
        self.is_running = False
        return layout

    def start_service(self, instance):
        if platform == 'android':
            self.status_label.text = "🔄 Service Starting in Background (Android)..."
            self.status_label.color = (0, 1, 1, 1)
            from android import AndroidService
            AndroidService('ASIM Network Checker', 'running').start('')
        else:
            if not self.is_running:
                self.is_running = True
                self.status_label.text = "🔄 Service Running in Background (Windows)..."
                self.status_label.color = (0, 1, 0, 1)
                threading.Thread(target=self.windows_background_worker, daemon=True).start()

    def stop_service(self, instance):
        self.status_label.text = "🛑 Service Stopped"
        self.status_label.color = (1, 0, 0, 1)
        
        if platform == 'android':
            from android import AndroidService
            AndroidService('ASIM Network Checker', 'running').stop()
        else:
            self.is_running = False

    def windows_background_worker(self):
        url = "https://speedtest.net"
        while self.is_running:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.update_ui(f"✅ Connected (Status: {response.status_code})", (0, 1, 0, 1))
                else:
                    self.update_ui(f"⚠️ Code {response.status_code}", (1, 1, 0, 1))
            except Exception as e:
                self.update_ui(f"❌ Disconnected\nError: {str(e)[:30]}", (1, 0, 0, 1))
            
            time.sleep(5)

    @mainthread
    def update_ui(self, text, color):
        if self.is_running:
            self.status_label.text = text
            self.status_label.color = color

if __name__ == "__main__":
    NetworkCheckerApp().run()
