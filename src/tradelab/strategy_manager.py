import os
from utils.helper_functions import get_class_names_from_file
import importlib

class StrategyManager:
    def __init__(self, price_iterator, broker):
        self.file_path = "workspace/my_strategies.py"
        self.broker = broker
        self.price_iterator = price_iterator
        self.last_modified_time = None
        self.available_strategies = {}
        self.active_strategy = {}
        self.update_available_strategies()

    def get_file_modification_time(self, file_path):
        """Get the last modified time of the specified file."""
        return os.path.getmtime(file_path)
    
    def update_available_strategies(self):
        
        current_modified_time = self.get_file_modification_time(self.file_path)
        if current_modified_time != self.last_modified_time:
            self.last_modified_time = current_modified_time
            class_names = get_class_names_from_file(self.file_path)
            module_name = os.path.splitext(os.path.basename(self.file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, self.file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            self.available_strategies.clear()
            for class_name in class_names:
                cls = getattr(module, class_name)
                self.available_strategies[class_name] = cls
            
            ordered_indicators = {name: self.available_strategies[name] for name in class_names if name in self.available_strategies}
            # self.available_strategies.clear()
            self.available_strategies.update(ordered_indicators)

            return True
    
    def activate_strategy(self, strategy_name):

        cls = self.available_strategies[strategy_name](self.price_iterator, self.broker)            
        self.active_strategy[strategy_name] = {
                'strategy': cls,    
            }
        