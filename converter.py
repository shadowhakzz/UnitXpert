"""
Unit Converter Application
A comprehensive tool for converting between different units of measurement
including length, weight, and temperature.

Author: [Your Name]
License: MIT
"""

import tkinter as tk
from tkinter import ttk, font
import math

# Initial window setup
root = tk.Tk()
root.title("Unit Converter")
root.geometry("800x600")
root.minsize(400, 300)

# Default font settings
default_font = ('Tahoma', 12)
root.option_add('*Font', default_font)

# Padding constants for UI elements
PADDING = {
    'small': 5,
    'medium': 10,
    'large': 20
}

# Animation duration in milliseconds
ANIMATION_DURATION = 150

# Theme settings
LIGHT_THEME = {
    'bg': '#ffffff',
    'fg': '#2c3e50',
    'button_bg': '#3498db',
    'button_fg': '#ffffff',
    'button_hover': '#2980b9',
    'entry_bg': '#f8f9fa',
    'entry_fg': '#2c3e50',
    'combobox_bg': '#f8f9fa',
    'combobox_fg': '#2c3e50',
    'title_fg': '#2c3e50',
    'frame_bg': '#f8f9fa',
    'highlight_bg': '#e3f2fd'
}

DARK_THEME = {
    'bg': '#1a1b1e',
    'fg': '#e4e6eb',
    'button_bg': '#2d88ff',
    'button_fg': '#ffffff',
    'button_hover': '#1877f2',
    'entry_bg': '#242526',
    'entry_fg': '#e4e6eb',
    'combobox_bg': '#242526',
    'combobox_fg': '#e4e6eb',
    'title_fg': '#2d88ff',
    'frame_bg': '#242526',
    'highlight_bg': '#3a3b3c'
}

current_theme = LIGHT_THEME

# Helper functions for responsive UI


def get_scaled_font(size):
    """Returns a scaled font based on the given size"""
    return ('Tahoma', max(8, int(size * 12 / 12)))


def create_responsive_frame(parent):
    """Creates a responsive frame with proper padding"""
    frame = tk.Frame(parent, bg=current_theme['frame_bg'])
    frame.pack(expand=True, fill='both', padx=PADDING['medium'],
               pady=PADDING['medium'])
    return frame


def create_responsive_label(parent, text, size=12, is_title=False):
    """Creates a responsive label with proper styling"""
    return tk.Label(parent, text=text, font=get_scaled_font(size),
                    bg=current_theme['bg'],
                    fg=current_theme['title_fg'] if is_title else current_theme['fg'])


def create_responsive_entry(parent):
    """Creates a responsive entry field with proper styling"""
    entry = tk.Entry(parent, font=get_scaled_font(12))
    entry.configure(relief='flat',
                    bg=current_theme['entry_bg'],
                    fg=current_theme['entry_fg'],
                    insertbackground=current_theme['entry_fg'],
                    highlightthickness=1,
                    highlightbackground=current_theme['button_bg'],
                    highlightcolor=current_theme['button_hover'])
    return entry


def animate_button_click(button):
    """Animates button click with color change"""
    original_bg = button.cget('bg')
    button.configure(bg=current_theme['button_hover'])
    root.after(ANIMATION_DURATION, lambda: button.configure(bg=original_bg))


def create_responsive_button(parent, text, command):
    """Creates a responsive button with hover effects and click animation"""
    def wrapped_command():
        animate_button_click(button)
        command()

    button = tk.Button(parent, text=text, command=wrapped_command,
                       font=get_scaled_font(11),
                       bg=current_theme['button_bg'],
                       fg=current_theme['button_fg'],
                       relief='flat',
                       borderwidth=0,
                       padx=PADDING['medium'],
                       pady=PADDING['small'],
                       cursor='hand2')

    def on_enter(e):
        button.configure(bg=current_theme['button_hover'])
        button.configure(relief='solid')

    def on_leave(e):
        button.configure(bg=current_theme['button_bg'])
        button.configure(relief='flat')

    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)
    return button


def create_back_button(parent):
    """Creates a back button that returns to main menu"""
    back_button = create_responsive_button(
        parent, "Back to Main Menu", show_main_menu)
    back_button.pack(
        side='bottom', pady=PADDING['medium'], fill='x', padx=PADDING['large'])
    return back_button

# Theme management functions


def toggle_theme():
    """Toggles between light and dark themes"""
    global current_theme
    current_theme = DARK_THEME if current_theme == LIGHT_THEME else LIGHT_THEME
    update_theme()


def update_theme():
    """Updates all widgets with current theme settings"""
    root.configure(bg=current_theme['bg'])
    for widget in root.winfo_children():
        update_widget_theme(widget)


def update_widget_theme(widget):
    """Updates individual widget theme settings"""
    try:
        if isinstance(widget, tk.Frame):
            widget.configure(bg=current_theme['frame_bg'])
        elif isinstance(widget, tk.Label):
            if widget.cget('font')[1] >= 20:  # For titles
                widget.configure(
                    bg=current_theme['bg'], fg=current_theme['title_fg'])
            else:
                widget.configure(
                    bg=current_theme['bg'], fg=current_theme['fg'])
        elif isinstance(widget, tk.Button):
            widget.configure(bg=current_theme['button_bg'],
                             fg=current_theme['button_fg'],
                             activebackground=current_theme['button_hover'],
                             activeforeground=current_theme['button_fg'])
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=current_theme['entry_bg'],
                             fg=current_theme['entry_fg'],
                             insertbackground=current_theme['entry_fg'],
                             highlightbackground=current_theme['button_bg'],
                             highlightcolor=current_theme['button_hover'])
        elif isinstance(widget, ttk.Combobox):
            style = ttk.Style()
            style.configure('TCombobox',
                            background=current_theme['combobox_bg'],
                            foreground=current_theme['combobox_fg'],
                            fieldbackground=current_theme['combobox_bg'],
                            selectbackground=current_theme['button_bg'],
                            selectforeground=current_theme['button_fg'])
            widget.configure(style='TCombobox')

        for child in widget.winfo_children():
            update_widget_theme(child)
    except:
        pass


def clear_window():
    """Clears all widgets from the window"""
    for widget in root.winfo_children():
        widget.destroy()

# Base conversion functions


def decimal_to_base(n, base):
    """Converts a decimal number to specified base"""
    if n == 0:
        return "0"
    digits = "0123456789ABCDEF"
    result = ""
    negative = False
    if n < 0:
        negative = True
        n = -n
    while n > 0:
        result = digits[n % base] + result
        n = n // base
    return "-" + result if negative else result


def base_to_decimal(n, base):
    """Converts a number from specified base to decimal"""
    if not n:
        return 0
    digits = "0123456789ABCDEF"
    negative = False
    if n[0] == '-':
        negative = True
        n = n[1:]
    result = 0
    for digit in n:
        result = result * base + digits.index(digit.upper())
    return -result if negative else result

# Main conversion functions


def base_converter():
    """Base conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Base Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_card = tk.Frame(main_frame, bg=current_theme['frame_bg'],
                          relief='solid', borderwidth=1)
    input_card.pack(fill='x', padx=PADDING['large'],
                    pady=PADDING['medium'])

    input_frame = create_responsive_frame(input_card)
    input_frame.pack(expand=True, fill='both',
                     padx=PADDING['medium'],
                     pady=PADDING['medium'])

    # Input fields
    value_label = create_responsive_label(input_frame, "Number:", size=12)
    value_label.pack(pady=(0, PADDING['small']))
    value_entry = create_responsive_entry(input_frame)
    value_entry.pack(fill='x', padx=PADDING['large'],
                     pady=(0, PADDING['medium']))

    bases_frame = tk.Frame(input_frame, bg=current_theme['frame_bg'])
    bases_frame.pack(fill='x', padx=PADDING['medium'])

    # From base
    from_frame = tk.Frame(bases_frame, bg=current_theme['frame_bg'])
    from_frame.pack(side='left', fill='x', expand=True,
                    padx=(0, PADDING['small']))

    from_base_label = create_responsive_label(
        from_frame, "From Base:", size=12)
    from_base_label.pack(pady=(0, PADDING['small']))
    from_base_combo = ttk.Combobox(from_frame, values=["2", "8", "10", "16"])
    from_base_combo.pack(fill='x')

    # To base
    to_frame = tk.Frame(bases_frame, bg=current_theme['frame_bg'])
    to_frame.pack(side='right', fill='x', expand=True,
                  padx=(PADDING['small'], 0))

    to_base_label = create_responsive_label(to_frame, "To Base:", size=12)
    to_base_label.pack(pady=(0, PADDING['small']))
    to_base_combo = ttk.Combobox(to_frame, values=["2", "8", "10", "16"])
    to_base_combo.pack(fill='x')

    # Result card
    result_card = tk.Frame(main_frame, bg=current_theme['frame_bg'],
                           relief='solid', borderwidth=1)
    result_card.pack(fill='x', padx=PADDING['large'],
                     pady=PADDING['medium'])

    result_frame = create_responsive_frame(result_card)
    result_frame.pack(expand=True, fill='both',
                      padx=PADDING['medium'],
                      pady=PADDING['medium'])

    result_label = create_responsive_label(result_frame, "Result:", size=12)
    result_label.pack(pady=(0, PADDING['small']))
    result_entry = create_responsive_entry(result_frame)
    result_entry.pack(fill='x', padx=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Operation buttons
    buttons_frame = tk.Frame(main_frame, bg=current_theme['bg'])
    buttons_frame.pack(fill='x', padx=PADDING['large'])

    def convert():
        """Converts number between bases"""
        try:
            value = value_entry.get()
            from_base = int(from_base_combo.get())
            to_base = int(to_base_combo.get())

            # Convert to decimal
            decimal = base_to_decimal(value, from_base)
            # Convert to target base
            result = decimal_to_base(decimal, to_base)

            result_entry.delete(0, tk.END)
            result_entry.insert(0, result)

            # Visual effect for result
            result_card.configure(relief='solid', borderwidth=2)
            root.after(ANIMATION_DURATION,
                       lambda: result_card.configure(relief='solid', borderwidth=1))

        except ValueError:
            result_entry.delete(0, tk.END)
            result_entry.insert(0, "Error: Please enter valid values")

            # Visual effect for error
            result_card.configure(bg='#ffebee')  # Light red
            root.after(ANIMATION_DURATION,
                       lambda: result_card.configure(bg=current_theme['frame_bg']))

    convert_btn = create_responsive_button(buttons_frame, "Convert", convert)
    convert_btn.pack(side='left', fill='x', expand=True,
                     padx=(0, PADDING['small']))


def show_main_menu():
    """Shows the main menu of the application"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'], pady=PADDING['large'])

    # Title
    title_label = create_responsive_label(
        main_frame, "Unit Converter", size=28, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Categories frame
    categories_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    categories_frame.pack(expand=True, fill='both', padx=PADDING['medium'])

    # Configure grid
    categories_frame.grid_columnconfigure(0, weight=1)
    categories_frame.grid_columnconfigure(1, weight=1)
    categories_frame.grid_columnconfigure(2, weight=1)

    # Create category sections
    categories = {
        "Basic Units": [
            ("Length", length_converter),
            ("Weight", weight_converter),
            ("Temperature", temperature_converter),
            ("Time", time_converter),
            ("Volume", volume_converter)
        ],
        "Advanced Units": [
            ("Speed", speed_converter),
            ("Area", area_converter),
            ("Energy", energy_converter),
            ("Pressure", pressure_converter),
            ("Digital Storage", digital_storage_converter)
        ],
        "Scientific Units": [
            ("Angle", angle_converter),
            ("Frequency", frequency_converter),
            ("Force", force_converter),
            ("Power", power_converter),
            ("Density", density_converter)
        ],
        "Electrical Units": [
            ("Electric Current", electric_current_converter),
            ("Electric Resistance", electric_resistance_converter),
            ("Magnetic Flux", magnetic_flux_converter)
        ],
        "Other Units": [
            ("Viscosity", viscosity_converter),
            ("Luminance", luminance_converter)
        ]
    }

    # Create category frames
    for col, (category_name, buttons) in enumerate(categories.items()):
        category_frame = tk.Frame(
            categories_frame, bg=current_theme['frame_bg'])
        category_frame.grid(
            row=0, column=col, padx=PADDING['medium'], pady=PADDING['medium'], sticky='nsew')

        # Category title
        category_label = create_responsive_label(
            category_frame, category_name, size=16, is_title=True)
        category_label.pack(pady=PADDING['small'])

        # Category separator
        separator = ttk.Separator(category_frame, orient='horizontal')
        separator.pack(fill='x', pady=PADDING['small'])

        # Buttons in category
        for text, command in buttons:
            button = create_responsive_button(category_frame, text, command)
            button.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Theme toggle button at bottom
    theme_button = create_responsive_button(
        main_frame, "Toggle Theme", toggle_theme)
    theme_button.pack(side='bottom', fill='x',
                      padx=PADDING['large'], pady=PADDING['medium'])

# Time conversion functions


def time_converter():
    """Time conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Time Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = (
        'Second', 'Minute', 'Hour', 'Day', 'Week', 'Month', 'Year')
    source_combo.set('Second')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = (
        'Second', 'Minute', 'Hour', 'Day', 'Week', 'Month', 'Year')
    target_combo.set('Minute')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to seconds first
            time_to_seconds = {
                'Second': 1,
                'Minute': 60,
                'Hour': 3600,
                'Day': 86400,
                'Week': 604800,
                'Month': 2592000,  # Assuming 30 days
                'Year': 31536000   # Assuming 365 days
            }

            # Convert to seconds
            seconds = value * time_to_seconds[source]
            # Convert to target unit
            result = seconds / time_to_seconds[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])

# Volume conversion functions


def volume_converter():
    """Volume conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Volume Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = (
        'Milliliter', 'Liter', 'Cubic Centimeter', 'Cubic Meter', 'Gallon', 'Pint', 'Quart')
    source_combo.set('Milliliter')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = (
        'Milliliter', 'Liter', 'Cubic Centimeter', 'Cubic Meter', 'Gallon', 'Pint', 'Quart')
    target_combo.set('Liter')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to milliliters first
            volume_to_ml = {
                'Milliliter': 1,
                'Liter': 1000,
                'Cubic Centimeter': 1,
                'Cubic Meter': 1000000,
                'Gallon': 3785.41,
                'Pint': 473.176,
                'Quart': 946.353
            }

            # Convert to milliliters
            ml = value * volume_to_ml[source]
            # Convert to target unit
            result = ml / volume_to_ml[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])

# Speed conversion functions


def speed_converter():
    """Speed conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Speed Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = (
        'Meters per Second', 'Kilometers per Hour', 'Miles per Hour', 'Knots')
    source_combo.set('Kilometers per Hour')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = (
        'Meters per Second', 'Kilometers per Hour', 'Miles per Hour', 'Knots')
    target_combo.set('Miles per Hour')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to meters per second first
            speed_to_mps = {
                'Meters per Second': 1,
                'Kilometers per Hour': 0.277778,
                'Miles per Hour': 0.44704,
                'Knots': 0.514444
            }

            # Convert to meters per second
            mps = value * speed_to_mps[source]
            # Convert to target unit
            result = mps / speed_to_mps[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])

# Area conversion functions


def area_converter():
    """Area conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Area Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('Square Meter', 'Square Centimeter',
                              'Square Kilometer', 'Hectare', 'Square Foot', 'Square Yard', 'Acre')
    source_combo.set('Square Meter')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('Square Meter', 'Square Centimeter',
                              'Square Kilometer', 'Hectare', 'Square Foot', 'Square Yard', 'Acre')
    target_combo.set('Square Kilometer')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to square meters first
            area_to_sqm = {
                'Square Meter': 1,
                'Square Centimeter': 0.0001,
                'Square Kilometer': 1000000,
                'Hectare': 10000,
                'Square Foot': 0.092903,
                'Square Yard': 0.836127,
                'Acre': 4046.86
            }

            # Convert to square meters
            sqm = value * area_to_sqm[source]
            # Convert to target unit
            result = sqm / area_to_sqm[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])

# Energy conversion functions


def energy_converter():
    """Energy conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Energy Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('Joule', 'Kilojoule', 'Calorie',
                              'Kilocalorie', 'Kilowatt Hour', 'Horsepower Hour')
    source_combo.set('Joule')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('Joule', 'Kilojoule', 'Calorie',
                              'Kilocalorie', 'Kilowatt Hour', 'Horsepower Hour')
    target_combo.set('Kilocalorie')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to joules first
            energy_to_joules = {
                'Joule': 1,
                'Kilojoule': 1000,
                'Calorie': 4.184,
                'Kilocalorie': 4184,
                'Kilowatt Hour': 3600000,
                'Horsepower Hour': 2684520
            }

            # Convert to joules
            joules = value * energy_to_joules[source]
            # Convert to target unit
            result = joules / energy_to_joules[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])

# Pressure conversion functions


def pressure_converter():
    """Pressure conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Pressure Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('Pascal', 'Kilopascal',
                              'Bar', 'Atmosphere', 'PSI')
    source_combo.set('Pascal')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('Pascal', 'Kilopascal',
                              'Bar', 'Atmosphere', 'PSI')
    target_combo.set('Bar')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to pascals first
            pressure_to_pa = {
                'Pascal': 1,
                'Kilopascal': 1000,
                'Bar': 100000,
                'Atmosphere': 101325,
                'PSI': 6894.76
            }

            # Convert to pascals
            pa = value * pressure_to_pa[source]
            # Convert to target unit
            result = pa / pressure_to_pa[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])

# Digital Storage conversion functions


def digital_storage_converter():
    """Digital Storage conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Digital Storage Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = (
        'Bit', 'Byte', 'Kilobyte', 'Megabyte', 'Gigabyte', 'Terabyte')
    source_combo.set('Megabyte')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = (
        'Bit', 'Byte', 'Kilobyte', 'Megabyte', 'Gigabyte', 'Terabyte')
    target_combo.set('Gigabyte')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to bits first
            storage_to_bits = {
                'Bit': 1,
                'Byte': 8,
                'Kilobyte': 8 * 1024,
                'Megabyte': 8 * 1024 * 1024,
                'Gigabyte': 8 * 1024 * 1024 * 1024,
                'Terabyte': 8 * 1024 * 1024 * 1024 * 1024
            }

            # Convert to bits
            bits = value * storage_to_bits[source]
            # Convert to target unit
            result = bits / storage_to_bits[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def length_converter():
    """Length conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Length Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = (
        'Meter', 'Centimeter', 'Millimeter', 'Kilometer', 'Inch', 'Foot', 'Yard', 'Mile')
    source_combo.set('Meter')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = (
        'Meter', 'Centimeter', 'Millimeter', 'Kilometer', 'Inch', 'Foot', 'Yard', 'Mile')
    target_combo.set('Centimeter')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to meters first
            length_to_meters = {
                'Meter': 1,
                'Centimeter': 0.01,
                'Millimeter': 0.001,
                'Kilometer': 1000,
                'Inch': 0.0254,
                'Foot': 0.3048,
                'Yard': 0.9144,
                'Mile': 1609.344
            }

            # Convert to meters
            meters = value * length_to_meters[source]
            # Convert to target unit
            result = meters / length_to_meters[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def weight_converter():
    """Weight conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Weight Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = (
        'Kilogram', 'Gram', 'Milligram', 'Pound', 'Ounce', 'Ton')
    source_combo.set('Kilogram')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = (
        'Kilogram', 'Gram', 'Milligram', 'Pound', 'Ounce', 'Ton')
    target_combo.set('Gram')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to kilograms first
            weight_to_kg = {
                'Kilogram': 1,
                'Gram': 0.001,
                'Milligram': 0.000001,
                'Pound': 0.453592,
                'Ounce': 0.0283495,
                'Ton': 1000
            }

            # Convert to kilograms
            kg = value * weight_to_kg[source]
            # Convert to target unit
            result = kg / weight_to_kg[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def temperature_converter():
    """Temperature conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Temperature Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('Celsius', 'Fahrenheit', 'Kelvin')
    source_combo.set('Celsius')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('Celsius', 'Fahrenheit', 'Kelvin')
    target_combo.set('Fahrenheit')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to Celsius first
            if source == 'Fahrenheit':
                celsius = (value - 32) * 5/9
            elif source == 'Kelvin':
                celsius = value - 273.15
            else:  # Celsius
                celsius = value

            # Convert from Celsius to target unit
            if target == 'Fahrenheit':
                result = (celsius * 9/5) + 32
            elif target == 'Kelvin':
                result = celsius + 273.15
            else:  # Celsius
                result = celsius

            result_label.configure(
                text=f"Result: {result:.2f} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def angle_converter():
    """Angle conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Angle Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = (
        'Degree', 'Radian', 'Grad', 'Arcminute', 'Arcsecond')
    source_combo.set('Degree')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = (
        'Degree', 'Radian', 'Grad', 'Arcminute', 'Arcsecond')
    target_combo.set('Radian')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to degrees first
            angle_to_degrees = {
                'Degree': 1,
                'Radian': 57.2958,
                'Grad': 0.9,
                'Arcminute': 1/60,
                'Arcsecond': 1/3600
            }

            # Convert to degrees
            degrees = value * angle_to_degrees[source]
            # Convert to target unit
            result = degrees / angle_to_degrees[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def frequency_converter():
    """Frequency conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Frequency Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('Hertz', 'Kilohertz',
                              'Megahertz', 'Gigahertz', 'RPM')
    source_combo.set('Hertz')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('Hertz', 'Kilohertz',
                              'Megahertz', 'Gigahertz', 'RPM')
    target_combo.set('Kilohertz')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to hertz first
            freq_to_hertz = {
                'Hertz': 1,
                'Kilohertz': 1000,
                'Megahertz': 1000000,
                'Gigahertz': 1000000000,
                'RPM': 1/60
            }

            # Convert to hertz
            hertz = value * freq_to_hertz[source]
            # Convert to target unit
            result = hertz / freq_to_hertz[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def force_converter():
    """Force conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Force Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = (
        'Newton', 'Kilogram-force', 'Pound-force', 'Dyne')
    source_combo.set('Newton')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = (
        'Newton', 'Kilogram-force', 'Pound-force', 'Dyne')
    target_combo.set('Kilogram-force')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to newtons first
            force_to_newton = {
                'Newton': 1,
                'Kilogram-force': 9.80665,
                'Pound-force': 4.44822,
                'Dyne': 0.00001
            }

            # Convert to newtons
            newton = value * force_to_newton[source]
            # Convert to target unit
            result = newton / force_to_newton[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def power_converter():
    """Power conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Power Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = (
        'Watt', 'Kilowatt', 'Horsepower', 'Kilocalorie per hour')
    source_combo.set('Watt')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = (
        'Watt', 'Kilowatt', 'Horsepower', 'Kilocalorie per hour')
    target_combo.set('Kilowatt')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to watts first
            power_to_watt = {
                'Watt': 1,
                'Kilowatt': 1000,
                'Horsepower': 745.7,
                'Kilocalorie per hour': 1.163
            }

            # Convert to watts
            watt = value * power_to_watt[source]
            # Convert to target unit
            result = watt / power_to_watt[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def density_converter():
    """Density conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Density Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('kg/m³', 'g/cm³', 'lb/ft³')
    source_combo.set('kg/m³')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('kg/m³', 'g/cm³', 'lb/ft³')
    target_combo.set('g/cm³')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to kg/m³ first
            density_to_kgm3 = {
                'kg/m³': 1,
                'g/cm³': 1000,
                'lb/ft³': 16.0185
            }

            # Convert to kg/m³
            kgm3 = value * density_to_kgm3[source]
            # Convert to target unit
            result = kgm3 / density_to_kgm3[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def viscosity_converter():
    """Viscosity conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Viscosity Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('Pa·s', 'Poise', 'Centipoise')
    source_combo.set('Pa·s')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('Pa·s', 'Poise', 'Centipoise')
    target_combo.set('Poise')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to Pa·s first
            viscosity_to_pas = {
                'Pa·s': 1,
                'Poise': 0.1,
                'Centipoise': 0.001
            }

            # Convert to Pa·s
            pas = value * viscosity_to_pas[source]
            # Convert to target unit
            result = pas / viscosity_to_pas[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def magnetic_flux_converter():
    """Magnetic Flux conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Magnetic Flux Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('Weber', 'Maxwell', 'Magnetic Lines')
    source_combo.set('Weber')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('Weber', 'Maxwell', 'Magnetic Lines')
    target_combo.set('Maxwell')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to webers first
            flux_to_weber = {
                'Weber': 1,
                'Maxwell': 0.00000001,
                'Magnetic Lines': 0.00000001
            }

            # Convert to webers
            weber = value * flux_to_weber[source]
            # Convert to target unit
            result = weber / flux_to_weber[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def luminance_converter():
    """Luminance conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Luminance Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('cd/m²', 'Foot-lambert', 'Stilb')
    source_combo.set('cd/m²')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('cd/m²', 'Foot-lambert', 'Stilb')
    target_combo.set('Foot-lambert')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to cd/m² first
            luminance_to_cdm2 = {
                'cd/m²': 1,
                'Foot-lambert': 3.426259,
                'Stilb': 10000
            }

            # Convert to cd/m²
            cdm2 = value * luminance_to_cdm2[source]
            # Convert to target unit
            result = cdm2 / luminance_to_cdm2[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def electric_current_converter():
    """Electric Current conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Electric Current Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('Ampere', 'Milliampere', 'Microampere')
    source_combo.set('Ampere')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('Ampere', 'Milliampere', 'Microampere')
    target_combo.set('Milliampere')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to amperes first
            current_to_ampere = {
                'Ampere': 1,
                'Milliampere': 0.001,
                'Microampere': 0.000001
            }

            # Convert to amperes
            ampere = value * current_to_ampere[source]
            # Convert to target unit
            result = ampere / current_to_ampere[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


def electric_resistance_converter():
    """Electric Resistance conversion interface"""
    clear_window()
    main_frame = create_responsive_frame(root)
    main_frame.pack(expand=True, fill='both',
                    padx=PADDING['large'],
                    pady=PADDING['large'])

    title_label = create_responsive_label(
        main_frame, "Electric Resistance Converter", size=24, is_title=True)
    title_label.pack(pady=PADDING['large'])

    # Add separator
    separator = ttk.Separator(main_frame, orient='horizontal')
    separator.pack(fill='x', pady=PADDING['medium'])

    # Add back button
    create_back_button(main_frame)

    # Input card
    input_frame = tk.Frame(main_frame, bg=current_theme['frame_bg'])
    input_frame.pack(fill='x', padx=PADDING['medium'], pady=PADDING['medium'])

    # Source unit
    source_label = create_responsive_label(input_frame, "From:")
    source_label.pack(anchor='w', padx=PADDING['small'])

    source_value = tk.StringVar()
    source_entry = create_responsive_entry(input_frame)
    source_entry.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    source_unit = tk.StringVar()
    source_combo = ttk.Combobox(input_frame, textvariable=source_unit)
    source_combo['values'] = ('Ohm', 'Kiloohm', 'Megaohm')
    source_combo.set('Ohm')
    source_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Target unit
    target_label = create_responsive_label(input_frame, "To:")
    target_label.pack(anchor='w', padx=PADDING['small'])

    target_unit = tk.StringVar()
    target_combo = ttk.Combobox(input_frame, textvariable=target_unit)
    target_combo['values'] = ('Ohm', 'Kiloohm', 'Megaohm')
    target_combo.set('Kiloohm')
    target_combo.pack(fill='x', padx=PADDING['small'], pady=PADDING['small'])

    # Result
    result_var = tk.StringVar()
    result_label = create_responsive_label(
        input_frame, "", size=14)
    result_label.pack(pady=PADDING['medium'])

    def convert():
        try:
            value = float(source_entry.get())
            source = source_unit.get()
            target = target_unit.get()

            # Convert everything to ohms first
            resistance_to_ohm = {
                'Ohm': 1,
                'Kiloohm': 1000,
                'Megaohm': 1000000
            }

            # Convert to ohms
            ohm = value * resistance_to_ohm[source]
            # Convert to target unit
            result = ohm / resistance_to_ohm[target]

            result_label.configure(
                text=f"Result: {result:.4g} {target}")
        except ValueError:
            result_label.configure(text="Please enter a valid number")
        except Exception as e:
            result_label.configure(text=f"Error: {str(e)}")

    # Convert button
    convert_btn = create_responsive_button(input_frame, "Convert", convert)
    convert_btn.pack(fill='x', padx=PADDING['small'], pady=PADDING['medium'])


# Start the application
if __name__ == "__main__":
    show_main_menu()
    root.mainloop()
