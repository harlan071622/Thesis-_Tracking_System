import customtkinter as ctk

ctk.set_appearance_mode("system")   
ctk.set_default_color_theme("dark-blue")  

FONT_TITLE_PARAMS = {"size":22, "weight":"bold"}
FONT_HEADER_PARAMS = {"size":18, "weight":"bold"}
FONT_NORMAL_PARAMS = {"size":14, "weight":"normal"}
FONT_SMALL_PARAMS = {"size":12, "weight":"normal"}

def get_font(params):
    """
    Create a CTkFont instance using given parameters.
    """
    return ctk.CTkFont(family=params.get("family"), size=params.get("size"), weight=params.get("weight"))

COLOR_BG         = "#ffffff"
COLOR_FRAME_BG   = "#ffffff"
COLOR_PRIMARY    = "#3498db"
COLOR_SECONDARY  = "#4CAF50"
COLOR_ACCENT     = "#FF5722"
COLOR_TEXT       = "#333333"


def style_button(button: ctk.CTkButton, primary: bool = True):
    """
    Apply consistent styling to CTkButtons.
    :param button: CTkButton instance
    :param primary: if True uses primary color, else secondary
    """
    fg = COLOR_PRIMARY if primary else COLOR_SECONDARY
    button.configure(
        fg_color=fg,
        hover_color=COLOR_ACCENT,
        text_color="white",
        font=get_font(FONT_NORMAL_PARAMS)
    )


def style_frame(frame: ctk.CTkFrame):
    frame.configure(fg_color=COLOR_FRAME_BG)


def style_label(label: ctk.CTkLabel, header: bool = False):
    
    params = FONT_HEADER_PARAMS if header else FONT_NORMAL_PARAMS
    label.configure(font=get_font(params), text_color=COLOR_TEXT)
