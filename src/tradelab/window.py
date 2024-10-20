import dearpygui.dearpygui as dpg

class Window:
    def __init__(self, window_counter, timeframe, price_iterator, indicator_manager):
        self.window_tag = f'window_{window_counter}'
        self.timeframe = timeframe
        self.price_iterator = price_iterator
        self.view_mode = 'Daily'
        self.plot_tag = f'plot_{window_counter}'
        self.x_axis_tag =  f'x-axis_{window_counter}'
        self.y_axis_tag = f'y-axis_{window_counter}'
        self.menu_indicators_tag = f'menu_indicators_{window_counter}'
        self.candle_series_tag = f'candle_series_{window_counter}'
        self.current_time_vline_tag = f"vline_tag_{window_counter}"
        self.indicator_manager = indicator_manager
        self.indicators = self.indicator_manager.available_indicator
        self.checked_indicators = {}

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
        
        dpg.add_vline_series([self.price_iterator.current_indices[self.timeframe]], parent=self.x_axis_tag, tag=self.current_time_vline_tag)

        self.update_axis_limits()

    def update_axis_limits(self):
        if self.view_mode == 'Free':
            dpg.set_axis_limits_auto(self.x_axis_tag)
            dpg.set_axis_limits_auto(self.y_axis_tag)
        elif self.view_mode == 'Daily':
            xmin, xmax, ymin, ymax = self._calaculate_daily_axis_limits()
            dpg.set_axis_limits(self.x_axis_tag, xmin, xmax)
            dpg.set_axis_limits(self.y_axis_tag, ymin, ymax)

    def update_candle_serie_plots(self):        
        dpg.configure_item(
            self.candle_series_tag,
            dates=self.price_iterator.simulation_data[self.timeframe].index.tolist(),
            opens=self.price_iterator.simulation_data[self.timeframe]["Open"].tolist(),
            highs=self.price_iterator.simulation_data[self.timeframe]["High"].tolist(),
            lows=self.price_iterator.simulation_data[self.timeframe]["Low"].tolist(),
            closes=self.price_iterator.simulation_data[self.timeframe]["Close"].tolist(),
        )

    def update_current_time_vline(self):        
        dpg.set_value(self.current_time_vline_tag, [[self.price_iterator.current_indices[self.timeframe]]])


    def update_indicator_menu(self):
        # Clear existing items in the indicators menu
        children = dpg.get_item_children(self.menu_indicators_tag)
        if children:
            for child in children[1]:
                dpg.delete_item(child)
       
        for indicator_name in self.indicators:
            is_checked = True if indicator_name in self.checked_indicators else False
            dpg.add_checkbox(
                label=indicator_name, 
                callback=self.activate_indicator, 
                user_data=indicator_name, 
                default_value=is_checked, 
                parent=self.menu_indicators_tag
            )

            if is_checked == True:
                self.indicator_manager.create_indicator(indicator_name, self.timeframe)


    def activate_indicator(self, sender, app_data, indicator_name):
        if app_data == True:
            window_counter = int(self.window_tag.split('_')[-1])
            self.indicator_manager.create_indicator(indicator_name, self.timeframe)
            indicator_data = self.indicator_manager.active_indicators[indicator_name, self.timeframe]['indicator'].data            
            tags = []
            for index, column_name in enumerate(indicator_data.columns[1:]):
                tag = f'{indicator_name}_{window_counter}_{index}'
                tags.append(tag)
                dpg.add_line_series(list(indicator_data.index), list(indicator_data[column_name]), tag=tag, parent=self.y_axis_tag)
            
            self.checked_indicators[indicator_name] = tags
        else:
            for tag in self.checked_indicators[indicator_name]:
                dpg.delete_item(tag)
            del self.checked_indicators[indicator_name]
            self.indicator_manager.delete_indicator(indicator_name, self.timeframe)

    def update_indicator_plots(self):

        for indicator_name, tags in list(self.checked_indicators.items()):
            indicator_data = self.indicator_manager.active_indicators[indicator_name, self.timeframe]['indicator'].data
            for tag, column_name in zip(tags, indicator_data.columns[1:]):
                dpg.configure_item(tag, x=list(indicator_data.index), y=list(indicator_data[column_name]))


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
    

    