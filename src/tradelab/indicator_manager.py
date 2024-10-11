import os
from utils.helper_functions import get_class_names_from_file
import importlib.util
import dearpygui.dearpygui as dpg


class IndicatorManager:
    def __init__(self, file_path, windows, price_iterator):
        self.file_path = file_path
        self.windows = windows
        self.price_iterator = price_iterator
        self.last_modified_time = None
        self.indicators = {}
        self.update_stored_indicators()

    def get_file_modification_time(self, file_path):
        """Get the last modified time of the specified file."""
        return os.path.getmtime(file_path)
    
    def update_stored_indicators(self):

        current_modified_time = self.get_file_modification_time(self.file_path)
        if current_modified_time != self.last_modified_time:
            self.last_modified_time = current_modified_time
            file_path = "workspace/my_indicators.py"
            class_names = get_class_names_from_file(file_path)
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            keys_to_remove = [key for key in self.indicators if key not in class_names]
            for key in keys_to_remove:
                del self.indicators[key]

            for class_name in class_names:
                if class_name not in self.indicators:
                    cls = getattr(module, class_name)  #
                    instance = cls(self.price_iterator)  
                    self.indicators[class_name] = instance

            ordered_indicators = {name: self.indicators[name] for name in class_names if name in self.indicators}
            self.indicators.clear()
            self.indicators.update(ordered_indicators)

            for window in self.windows.values():
                window.update_indicator_menu()


            
            # remove linseries or drawing of removed indicators  
            # recheck previous turn on indicators

    def update_checked_indicators(self, sender, app_data, user_data):
        print(sender, app_data)
        ...