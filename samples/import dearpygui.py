import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from utils.data_import import import_data
import threading


market_config = {
        'date_range': ('2024-05-09', '2024-05-09'),
        'time_range': ('14:00:00', '17:00:00'),
        'market': 'wallstreet',
        'timeframes': ['1min']
    }

    # Load market data
date_bounds = market_config['date_range']
time_bounds = market_config['time_range']
market = market_config['market']
timeframes = market_config['timeframes']
data = import_data(date_bounds, time_bounds, market, timeframes)

df = data['1min']

dates = df['DateTime'].to_list()
dates = df.index.to_list()
min_dates = min(dates)
max_dates = max(dates)
opens = df['Open'].to_list()
highs = df['High'].to_list()
lows = df['Low'].to_list()
closes = df['Close'].to_list()


dpg.create_context()

class charts():
    ...

with dpg.window(label="Tutorial", width=400, height=400):
    dpg.add_plot(label="Bar Series", height=-1, width=-1, tag='tttt')
    dpg.add_plot_axis(dpg.mvXAxis, time=False, no_tick_marks=False, parent='tttt',no_tick_labels=False, tag='x-axis_1')
    dpg.add_plot_axis(dpg.mvYAxis, label="USD",parent='tttt', tag='y-axis_2')






# dpg.add_candle_series(
#                 dates,
#                 opens,
#                 closes,
#                 lows,
#                 highs,
#                 parent='y-axis_2'
#             )
# dpg.add_line_series([0, 1, 2, 3], [3, 2, 5, 8], label="Series", parent='y-axis_2', tag = 'hello')


# Function to update the line series
def update_line_series(tag):
    # New data for the line series
    new_x_data = [0, 1, 2, 3, 4, 5]
    new_y_data = [10, 30, 40, 20, 50, 10]
    
    # Update the line series with new data
    dpg.configure_item(tag, x=new_x_data, y=new_y_data, label="Updated Series")



       
dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    
    update_line_series('guh')

dpg.start_dearpygui()
dpg.destroy_context()



# import dearpygui.dearpygui as dpg

# dpg.create_context()

# # Callback function to print "Hi" when the plot is resized
# def on_resize(sender, app_data):
#     print("Hi, the plot has been resized!")

# # Create a window with a plot
# with dpg.window(label="Main Window", width=500, height=400):
#     with dpg.plot(label="Example Plot", height=-1, width=-1, tag="my_plot"):
#         dpg.add_plot_axis(dpg.mvXAxis, label="x")
#         with dpg.plot_axis(dpg.mvYAxis, label="y"):
#             dpg.add_line_series([0, 1, 2, 3], [3, 2, 5, 8], label="Series")

# # Add a handler registry and attach the resize handler to the plot
# with dpg.handler_registry():
#     dpg.add_item_resize_handler(callback=on_resize, parent="my_plot")

# dpg.create_viewport(title='Resizable Plot Example', width=600, height=400)
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()


# import dearpygui.dearpygui as dpg

# dpg.create_context()

# def change_text(sender, app_data):
#     dpg.set_value("text item", f"Mouse Button ID: {app_data}")

# def visible_call(sender, app_data):
#     print("I'm visible")

# with dpg.window(width=500, height=300, tag="234"):
#     with dpg.plot(label="Example Plot", height=-1, width=-1, tag="my_plot"):
#         dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="4")
#         with dpg.plot_axis(dpg.mvYAxis, label="y", tag="3"):
#             dpg.add_line_series([0, 1, 2, 3], [3, 2, 5, 8], label="Series")


# dpg.create_viewport(title='Custom Title', width=800, height=600)
# dpg.setup_dearpygui()
# dpg.show_viewport()

# while dpg.is_dearpygui_running():
#     dpg.render_dearpygui_frame()
# # dpg.start_dearpygui()

# dpg.set_frame_callback(1, visible_call)


# dpg.destroy_context()


        # dpg.set_axis_ticks(dpg.last_item(), (("S1", 1), ("S2", 2), ("S3", 3)))





















# import dearpygui.dearpygui as dpg


# old_axis_limits = None

# dpg.create_context()

# def change_text(sender, app_data):
#     dpg.set_value("text item", f"Mouse Button ID: {app_data}")

# def visible_call(old_axis_limits, new_axis_limit):
#     if new_axis_limit != old_axis_limits:
#         old_axis_limits = new_axis_limit
#         print(new_axis_limit)
#     return new_axis_limit

# # Create a window with a plot
# with dpg.window(width=500, height=300):
#     with dpg.plot(label="Example Plot", height=-1, width=-1, tag="my_plot"):
#         dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
#         with dpg.plot_axis(dpg.mvYAxis, label="y", tag="y_axis"):
#             dpg.add_line_series([0, 1, 2, 3], [3, 2, 5, 8], label="Series")

#         dpg.draw_line((0, 4), (10, 4), color=(255, 0, 0, 255), thickness=0, parent='my_plot')


# # Setup viewport and show the window
# dpg.create_viewport(title='Custom Title', width=800, height=600)
# dpg.setup_dearpygui()
# dpg.show_viewport()

# # Main rendering loop
# while dpg.is_dearpygui_running():
#     old_axis_limits = visible_call(old_axis_limits, dpg.get_axis_limits('x_axis'))
#     dpg.render_dearpygui_frame()

# # Cleanup
# dpg.destroy_context()
