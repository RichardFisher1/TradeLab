import os
from utils.helper_functions import get_class_names_from_file
import importlib.util
import dearpygui.dearpygui as dpg
from pprint import pprint
import importlib
import sys


class IndicatorManager:
    def __init__(self, file_path, price_iterator):
        self.file_path = file_path
        self.price_iterator = price_iterator
        self.last_modified_time = None
        self.available_indicator = {}
        self.active_indicators = {}
        self.update_available_indicators()

    def get_file_modification_time(self, file_path):
        """Get the last modified time of the specified file."""
        return os.path.getmtime(file_path)
    
    def update_available_indicators(self):

        current_modified_time = self.get_file_modification_time(self.file_path)
        if current_modified_time != self.last_modified_time:
            self.last_modified_time = current_modified_time
            file_path = "workspace/my_indicators.py"
            class_names = get_class_names_from_file(file_path)
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # keys_to_remove = [key for key in self.available_indicator if key not in class_names]
            # for key in keys_to_remove:
            #     del self.available_indicator[key]
            self.available_indicator.clear()
            for class_name in class_names:
                # if class_name not in self.available_indicator:
                cls = getattr(module, class_name)
                self.available_indicator[class_name] = cls
            
            ordered_indicators = {name: self.available_indicator[name] for name in class_names if name in self.available_indicator}
            self.available_indicator.clear()
            self.available_indicator.update(ordered_indicators)

            self.active_indicators.clear()

            return True
        
    def create_indicator(self, indicator_name, timeframe):
        key = (indicator_name, timeframe)
        if key not in self.active_indicators:
            cls = self.available_indicator[indicator_name](self.price_iterator, timeframe)            
            self.active_indicators[key] = {
                'indicator': cls,
                'count': 1  
            }
        else:
            self.active_indicators[key]['count'] += 1

    def delete_indicator(self, indicator_name, timeframe):
        key = (indicator_name, timeframe)
        if key in self.active_indicators:
            self.active_indicators[key]['count'] -= 1
            if self.active_indicators[key]['count'] == 0:
                del self.active_indicators[key]

    def update_active_indicators(self, change_increment=False):
        for value in self.active_indicators.values():
            value['indicator'].update(change_increment)



        
