import dearpygui.dearpygui as dpg
from tradelab.price_iterator import PriceIterator
from tradelab.indicator_manager import IndicatorManager
from utils.helper_functions import get_class_names_from_file
from tradelab.window import Window



class ChartsApp:
    def __init__(self, data):
        self.file_path = "workspace/my_indicators.py"
        self.window_counter = 0
        self.windows = {}
        
        self.price_iterator = PriceIterator(data)
        self.indicator_manager = IndicatorManager(self.file_path, self.price_iterator)
        
        self.backtest_switch = False
        self.start_switch = False

        self.create_context()
      
    ### ---------- CREATE GUI COMPONENTS - MENUS & WINDOWS ---------- ###

    def create_context(self):
        dpg.create_context()
        self.create_menus()
        self.create_controls_window()
        dpg.configure_app(docking=True, docking_space=True, init_file="dpg.ini", load_init_file=True)
        
    def create_menus(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="save workspace", callback=self.save_workspace)
            with dpg.menu(label="New_Chart"):
                for timeframe in self.price_iterator.data.keys():
                    dpg.add_menu_item(label=timeframe, callback=self.create_chart_window, user_data=timeframe)
            with dpg.menu(label="Backtest"):
                dpg.add_radio_button(("None", "strat_1", "strat_2"), tag='backtest', callback=self._backtest_switch, horizontal=False)

    def create_controls_window(self):
        with dpg.window(label="Controls", no_close=True, collapsed=True):
            dpg.add_text("This window has no close button.")
            dpg.add_radio_button(list(self.price_iterator.data.keys()), default_value=None, callback=self.change_increment)
            dpg.add_button(label="Next_iteration", callback=self.next_iteration)
            dpg.add_button(label="Start", callback=self.start)
            dpg.add_button(label="Stop", callback=self.stop)
            dpg.add_button(label="Next_day", callback=self.next_day)

    def create_chart_window(self, sender, app_data, timeframe):
        window_tag = f'window_{self.window_counter}'
        self.windows[window_tag] = Window(self.window_counter, timeframe, self.price_iterator, self.indicator_manager)
        self.window_counter +=1
    
    def _backtest_switch(self, sender, app_data):
        if app_data == 'None':
            self.backtest_switch = False
        else:
            self.backtest_switch = True
  
    def save_workspace(self):
        dpg.save_init_file("dpg.ini")
    
    ### ---------- CONTROLLER & MENU BUTTONS ---------- ###

    def next_iteration(self):
        self.price_iterator.next()
        self.indicator_manager.update_active_indicators()

        for window in self.windows.values():
                window.update_candle_serie_plots()
                window.update_indicator_plots()
                
    def change_increment(self, sender, timeframe):
        previous_time = self.price_iterator.current_time
        self.price_iterator.change_increment(timeframe)
        new_time = self.price_iterator.current_time
        if previous_time != new_time:
            #update candelsticks 
            ...

    def start(self):
        self.start_switch = True
    
    def stop(self):
        self.start_switch = False

    def next_day(self):
        self.price_iterator.next_day()
        for window in self.windows.values():
                window.update_candle_series()

    ### -------- MAIN FLOW ------------------ ###
               
    def run(self):
        dpg.create_viewport(title='TradeLab_Charts', width=600, height=200)
        dpg.setup_dearpygui()
        dpg.show_viewport()       
        while dpg.is_dearpygui_running():
            
            if self.indicator_manager.update_available_indicators():
                 for window in self.windows.values():
                    window.update_indicator_menu()  # right now this updates also active indicators and checked_indicators
                    window.update_indicator_plots()
            

            # update indicators
            # update plot indicators 



            
            if self.start_switch is True:
                self.next_iteration()

            for window in self.windows.values():
                window.update_axis_limits()
            
            


            dpg.render_dearpygui_frame()

            

        dpg.start_dearpygui()
        dpg.destroy_context()

