import dearpygui.dearpygui as dpg

# # Function to create a black theme for the entire application
# def create_black_theme():
#     with dpg.theme(tag="black_theme"):
#         with dpg.theme_component(dpg.mvAll):
#             # dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (110, 0, 0), category=dpg.mvThemeCat_Core)  # Black window background
#             dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (110, 0, 0), category=dpg.mvThemeCat_Core)  # Dark title background
#             dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (60, 60, 60), category=dpg.mvThemeCat_Core)  # Darker when active
#             # dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (30, 30, 30), category=dpg.mvThemeCat_Core)  # Dark menu bar background
#             dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (100, 20, 20), category=dpg.mvThemeCat_Core)  # Frame background (buttons, etc.)
#             # dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 50, 50), category=dpg.mvThemeCat_Core)  # Button background
#             # dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (70, 70, 70), category=dpg.mvThemeCat_Core)  # Button hover
#             # dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (90, 90, 90), category=dpg.mvThemeCat_Core)  # Button active

#             # Text and border color settings
#             dpg.add_theme_color(dpg.mvThemeCol_Border, (255, 255, 255), category=dpg.mvThemeCat_Core)  # White border
#             dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)  # White text

# # Function to create a menu bar
# def create_menu_bar():
#     with dpg.menu_bar():
#         with dpg.menu(label="File"):
#             dpg.add_menu_item(label="New")
#             dpg.add_menu_item(label="Open")
#             dpg.add_menu_item(label="Save")
#             dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())
#         with dpg.menu(label="Edit"):
#             dpg.add_menu_item(label="Undo")
#             dpg.add_menu_item(label="Redo")
#             dpg.add_menu_item(label="Cut")
#             dpg.add_menu_item(label="Copy")
#             dpg.add_menu_item(label="Paste")
#         with dpg.menu(label="View"):
#             dpg.add_menu_item(label="Fullscreen")
#             dpg.add_menu_item(label="Zoom In")
#             dpg.add_menu_item(label="Zoom Out")

# # Function to create the main window
# def create_main_window():
#     with dpg.window(label="Main Window", width=800, height=600, tag="main_window"):
#         create_menu_bar()  # Place the menu bar inside the window
#         # Add some widgets inside the window (for demonstration)
#         dpg.add_text("Hello, welcome to the black-themed app!")
#         dpg.add_button(label="Click Me")
#         dpg.add_slider_float(label="Slider", default_value=0.5)

# # Setup DearPyGui context
# dpg.create_context()

# # Create the black theme
# create_black_theme()

# # Create the main window with a menu bar
# create_main_window()

# # Bind the black theme to the main window
# dpg.bind_theme("black_theme")

# # Setup viewport
# dpg.create_viewport(title='Black Themed App with Menu Bar', width=800, height=600)
# dpg.set_viewport_clear_color((100, 0, 0))  # Set viewport background to black

# # Setup DearPyGui rendering and show the app
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()



class App:
    def __init__(self):    
        self.create_context()
        
    ### ---------- CREATE GUI COMPONENTS - MENUS & WINDOWS ---------- ###

    def create_context(self):
        dpg.create_context()
        self.create_themes()
        self.create_menus()
        dpg.configure_app(docking=True, docking_space=False)


    def create_themes(self):
       
       
        with dpg.theme(tag="black_theme"):
            with dpg.theme_component(dpg.mvAll):  # Apply to all Dear PyGui components
                #dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0), category=dpg.mvThemeCat_Core)  # Black window background
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (0, 0, 0), category=dpg.mvThemeCat_Core)  # Dark title background
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (60, 60, 60), category=dpg.mvThemeCat_Core)  # Darker when active
                # dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (20, 20, 20), category=dpg.mvThemeCat_Core)  # Frame background (buttons, etc.)
                # dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (0, 0, 0), category=dpg.mvThemeCat_Core)  # Black background for popup windows
                # dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (20, 20, 20), category=dpg.mvThemeCat_Core)  # Menu bar background
                # dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255), category=dpg.mvThemeCat_Core)  # White text

    def create_menus(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="save workspace")
            with dpg.menu(label="Visual_Backtest"):
                dpg.add_radio_button(("None", "strat_1", "strat_2"), tag='backtest', horizontal=False)
    
    def run(self):
        #dpg.bind_theme("black_theme")
        dpg.create_viewport(title='TradeLab_Charts', width=600, height=200)
        dpg.bind_theme("black_theme")
        # dpg.set_viewport_clear_color((0, 0, 0))
        dpg.setup_dearpygui()
        dpg.show_viewport()       
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()

        dpg.start_dearpygui()
        dpg.destroy_context()

app = App()
app.run()