import dearpygui.dearpygui as dpg

class IndicatorManager:
    def update_checked_indicators(self, sender, app_data, user_data):
        print(f"Checkbox clicked: {user_data[0]}, State: {app_data}")

class TestApp:
    def __init__(self):
        dpg.create_context()
        self.menu_indicators_tag = "menu_indicators"
        self.indicators = ["SMA", "EMA", "MACD"]
        self.indicators_manager = IndicatorManager()

        with dpg.window(label="Test Window"):
            with dpg.menu_bar():
                with dpg.menu(label="Indicators", tag=self.menu_indicators_tag):
                    self.update_indicator_menu()
                
                dpg.add_button(label="Refresh Indicators", callback=self.update_indicator_menu)


    def update_indicator_menu(self):
        # Clear existing items in the indicators menu
        children = dpg.get_item_children(self.menu_indicators_tag)
        if children and children[1]:
            for child in children[1]:
                dpg.delete_item(child)

        # Add new checkboxes for each key in self.indicators
        for indicator in self.indicators:
            dpg.add_checkbox(label=indicator, 
                             callback=self.indicators_manager.update_checked_indicators, 
                             user_data=[indicator], 
                             parent=self.menu_indicators_tag)
            
    def run(self):
        dpg.create_viewport(title='Test App', width=600, height=300)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            self.update_indicator_menu()
            dpg.render_dearpygui_frame()
        dpg.start_dearpygui()
        dpg.destroy_context()



app = TestApp()
app.run()