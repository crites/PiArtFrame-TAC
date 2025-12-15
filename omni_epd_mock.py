"""Mock omni_epd for Windows development
This allows you to develop and test the Mandelbrot generation
without needing the actual e-ink hardware.
"""

class EPD:
    """Mock EPD (e-Paper Display) class"""
    
    def __init__(self, device_name=None):
        self.device_name = device_name or "mock_display"
        self.width = 800
        self.height = 480
        print(f"[MOCK] Initialized e-ink display: {self.device_name}")
        
    def prepare(self):
        """Mock prepare - called before displaying"""
        print("[MOCK] EPD prepared")
        
    def display(self, image):
        """Mock display - saves image to file instead of showing on e-ink"""
        print(f"[MOCK] Displaying image {image.size} on {self.device_name}")
        # Save preview for testing
        preview_path = "preview.png"
        image.save(preview_path)
        print(f"[MOCK] Saved preview to {preview_path}")
        
    def close(self):
        """Mock close - cleanup"""
        print("[MOCK] EPD closed")


class displayfactory:
    """Mock displayfactory class"""
    
    @staticmethod
    def load_display_driver(device_name):
        """Load a mock display driver"""
        print(f"[MOCK] Loading display driver: {device_name}")
        return EPD(device_name)