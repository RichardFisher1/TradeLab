import dearpygui.dearpygui as dpg

class Window:
    def __init__(self, window_counter, timeframe, price_iterator, indicators):
        self.window_tag = f'window_{window_counter}'
        self.timeframe = timeframe
        self.price_iterator = price_iterator
        self.view_mode = 'Daily'
        self.plot_tag = f'plot_{window_counter}'
        self.x_axis_tag =  f'x-axis_{window_counter}'
        self.y_axis_tag = f'y-axis_{window_counter}'
        self.menu_indicators_tag = f'menu_indicators_{window_counter}'
        self.candle_series_tag = f'candle_series_{window_counter}'
        self.indicators = indicators

        with dpg.window(label=timeframe, width=400, height=400, tag=self.window_tag):
            with dpg.menu_bar():
                with dpg.menu(label="Indicators", tag=self.menu_indicators_tag):
                    self.update_indicator_menu()
                with dpg.menu(label="Veiw"):
                    dpg.add_radio_button(("Free", "Daily", "Custom"), default_value=self.view_mode, callback=self._update_view_mode)
        dpg.add_plot(height=-1, width=-1, parent=self.window_tag, tag=self.plot_tag)
        dpg.add_plot_legend(parent=self.plot_tag) 
        dpg.add_plot_axis(dpg.mvXAxis, time=False, no_tick_marks=False, parent=self.plot_tag,no_tick_labels=False, tag=self.x_axis_tag)
        dpg.add_plot_axis(dpg.mvYAxis, label="USD",parent=self.plot_tag, tag=self.y_axis_tag)
        dpg.add_candle_series(self.price_iterator.simulation_data[self.timeframe].index.tolist(),
                            self.price_iterator.simulation_data[self.timeframe]["Open"].tolist(),
                            self.price_iterator.simulation_data[self.timeframe]["Close"].tolist(),
                            self.price_iterator.simulation_data[self.timeframe]["Low"].tolist(),
                            self.price_iterator.simulation_data[self.timeframe]["High"].tolist(),
                            time_unit=dpg.mvTimeUnit_S,
                            parent=self.y_axis_tag,
                            tag = self.candle_series_tag)
        
        self.update_axis_limits()


    def update_axis_limits(self):
        if self.view_mode == 'Free':
            dpg.set_axis_limits_auto(self.x_axis_tag)
            dpg.set_axis_limits_auto(self.y_axis_tag)
        elif self.view_mode == 'Daily':
            xmin, xmax, ymin, ymax = self._calaculate_daily_axis_limits()
            dpg.set_axis_limits(self.x_axis_tag, xmin, xmax)
            dpg.set_axis_limits(self.y_axis_tag, ymin, ymax)


    def update_candle_series(self):        
        dpg.configure_item(
            self.candle_series_tag,
            dates=self.price_iterator.simulation_data[self.timeframe].index.tolist(),
            opens=self.price_iterator.simulation_data[self.timeframe]["Open"].tolist(),
            highs=self.price_iterator.simulation_data[self.timeframe]["High"].tolist(),
            lows=self.price_iterator.simulation_data[self.timeframe]["Low"].tolist(),
            closes=self.price_iterator.simulation_data[self.timeframe]["Close"].tolist(),
        )


    def update_checked_indicators(self, sender, app_data, user_data):
        print(sender, app_data, )


    def update_indicator_menu(self):

        print(self.indicators)
        # Clear existing items in the indicators menu
        children = dpg.get_item_children(self.menu_indicators_tag)
        if children:
            for child in children[1]:
                dpg.delete_item(child)

        # Add new checkboxes for each key in self.indicators
        for indicator in self.indicators:
            dpg.add_checkbox(label=indicator, callback=self.update_checked_indicators, 
                            user_data=[indicator, self.window_tag], parent=self.menu_indicators_tag)


    def _update_view_mode(self, _, app_data):
        self.view_mode = app_data


    def _calaculate_daily_axis_limits(self):
        n_bars_in_day = self.price_iterator.n_bars_in_day[self.timeframe]
        open_of_day_index = self.price_iterator.current_indices[self.timeframe] // (n_bars_in_day) * n_bars_in_day
        open_of_day = self.price_iterator.simulation_data[self.timeframe].iloc[open_of_day_index, 1]
        xmin = open_of_day_index - 0.5
        xmax = open_of_day_index - 0.5 + n_bars_in_day
        ymax = max(open_of_day + 200, max(self.price_iterator.simulation_data[self.timeframe].iloc[open_of_day_index:open_of_day_index+n_bars_in_day, 2])) + 5
        ymin = min(open_of_day - 200, min(self.price_iterator.simulation_data[self.timeframe].iloc[open_of_day_index:open_of_day_index+n_bars_in_day, 3])) - 5
        return xmin, xmax, ymin, ymax
    

    