# import dearpygui.dearpygui as dpg
# from math import sin

# dpg.create_context()

# sindatax = []
# sindatay = []
# for i in range(0, 100):
#     sindatax.append(i / 100)
#     sindatay.append(0.5 + 0.5 * sin(50 * i / 100))
# sindatay2 = []
# for i in range(0, 100):
#     sindatay2.append(2 + 0.5 * sin(50 * i / 100))

# with dpg.window(label="Tutorial", width=500, height=400):
#     with dpg.theme(tag="plot_theme"):
#         with dpg.theme_component(dpg.mvScatterSeries):
#             dpg.add_theme_color(dpg.mvPlotCol_Line, (217, 95, 2), category=dpg.mvThemeCat_Plots)
#             dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, dpg.mvPlotMarker_Up, category=dpg.mvThemeCat_Plots)
#             dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 4, category=dpg.mvThemeCat_Plots)

#     # create plot
#     with dpg.plot(tag="plot", label="Line Series", height=-1, width=-1):

#         # optionally create legend
#         dpg.add_plot_legend()

#         # REQUIRED: create x and y axes
#         dpg.add_plot_axis(dpg.mvXAxis, label="x")
#         dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="yaxis")

#         # series belong to a y axis
#         dpg.add_stem_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)", parent="yaxis", tag="series_data")
#         dpg.add_scatter_series(sindatax, sindatay2, label="2 + 0.5 * sin(x)", parent="yaxis", tag="series_data2")

#         # apply theme to series
#         dpg.bind_item_theme("series_data", "plot_theme")
#         dpg.bind_item_theme("series_data2", "plot_theme")

# dpg.create_viewport(title='Custom Title', width=800, height=600)
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()


import pandas as pd

# Create a simple DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Info': [None, None, None]  # Placeholder for dictionaries
})

# Define a dictionary
person_info = {'age': 25, 'city': 'New York'}

# Use 'at' to set the dictionary as an element in the DataFrame
df.at[1, 'Info'] = person_info

# Print the updated DataFrame
print(df)