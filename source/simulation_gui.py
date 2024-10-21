import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json


def setup_theme() -> None:
    # theme settings
    style = ttk.Style()
    style.theme_create("yummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [1, 0, 1, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": '#9a9a9a'},
            "map": {"background": [("selected", '#b3b3b3')],
                    "expand": [("selected", [1, 0, 1, 0])]}}})

    style.theme_use("yummy")


def setup_notebook(screen: tk.Tk) -> ttk.Notebook:
    # Create a Notebook widget (tabs container)
    notebook = ttk.Notebook(screen, height=400)
    notebook.pack(fill='both', expand=True)

    return notebook


def setup_tabs(notebook: ttk.Notebook) -> list[tk.Frame]:
    # Create frames for each tab
    tab1 = tk.Frame(notebook, bg='#b3b3b3', borderwidth=20)
    tab2 = tk.Frame(notebook, bg='#b3b3b3', borderwidth=20)
    tab3 = tk.Frame(notebook, bg='#b3b3b3', borderwidth=20)

    # Add frames to the notebook as tabs
    notebook.add(tab1, text="   Simulation Settings   ")
    notebook.add(tab2, text="    Developer Options    ")
    notebook.add(tab3, text="        Extra Tab        ")

    return [tab1, tab2, tab3]


def setup_tab1(screen: tk.Frame) -> list[tk.StringVar]:
    # simulation settings tab
    var_pop_count = tk.StringVar()
    label_pop_count = tk.Label(screen, text='Population Count:', bg='#b3b3b3')
    label_pop_count.grid(row=0, column=0, sticky='w', pady=5)
    entry_pop_count = tk.Entry(screen, width=10, bg='#b3b3b3', relief='solid', textvariable=var_pop_count)
    entry_pop_count.grid(row=0, column=1)

    var_infection_radius = tk.StringVar()
    label_infection_radius = tk.Label(screen, text='Infection Radius:', bg='#b3b3b3')
    label_infection_radius.grid(row=1, column=0, sticky='w', pady=5)
    entry_infection_radius = tk.Entry(screen, width=10, bg='#b3b3b3', relief='solid', textvariable=var_infection_radius)
    entry_infection_radius.grid(row=1, column=1)

    var_healthy_start_percentage = tk.StringVar()
    label_healthy_start_percentage = tk.Label(screen, text='Health Start Percentage:', bg='#b3b3b3')
    label_healthy_start_percentage.grid(row=2, column=0, sticky='w', pady=5)
    entry_healthy_start_percentage = tk.Entry(screen, width=10, bg='#b3b3b3', relief='solid',
                                              textvariable=var_healthy_start_percentage)
    entry_healthy_start_percentage.grid(row=2, column=1)

    var_sick_start_percentage = tk.StringVar()
    label_sick_start_percentage = tk.Label(screen, text='Sick Start Percentage:', bg='#b3b3b3')
    label_sick_start_percentage.grid(row=3, column=0, sticky='w', pady=5)
    entry_sick_start_percentage = tk.Entry(screen, width=10, bg='#b3b3b3', relief='solid',
                                           textvariable=var_sick_start_percentage)
    entry_sick_start_percentage.grid(row=3, column=1)

    var_infection_chance = tk.StringVar()
    label_infection_chance = tk.Label(screen, text='Infection Chance:', bg='#b3b3b3')
    label_infection_chance.grid(row=4, column=0, sticky='w', pady=5)
    entry_infection_chance = tk.Entry(screen, width=10, bg='#b3b3b3', relief='solid', textvariable=var_infection_chance)
    entry_infection_chance.grid(row=4, column=1)

    var_immune_chance = tk.StringVar()
    label_immune_chance = tk.Label(screen, text='Immune Chance:', bg='#b3b3b3')
    label_immune_chance.grid(row=5, column=0, sticky='w', pady=5)
    entry_immune_chance = tk.Entry(screen, width=10, bg='#b3b3b3', relief='solid', textvariable=var_immune_chance)
    entry_immune_chance.grid(row=5, column=1)

    var_group_count = tk.StringVar()
    label_group_count = tk.Label(screen, text='Group Count:', bg='#b3b3b3')
    label_group_count.grid(row=8, column=0, sticky='w', pady=5)
    entry_group_count = tk.Entry(screen, width=10, bg='#b3b3b3', relief='solid', textvariable=var_group_count)
    entry_group_count.grid(row=8, column=1)

    return [var_pop_count, var_infection_radius, var_sick_start_percentage, var_healthy_start_percentage,
            var_infection_chance, var_immune_chance, var_group_count]


def setup_tab2(screen: tk.Frame) -> list[tk.StringVar]:
    # developer settings tab
    var_person_display_size = tk.StringVar()
    label_person_display_size = tk.Label(screen, text='Person Display Size:', bg='#b3b3b3')
    label_person_display_size.grid(row=0, column=0, sticky='w', pady=5)
    entry_person_display_size = tk.Entry(screen, width=10, bg='#b3b3b3', relief='solid',
                                         textvariable=var_person_display_size)
    entry_person_display_size.grid(row=0, column=1)

    var_show_quads = tk.StringVar()
    label_show_quads = tk.Label(screen, text='Show Quads:', bg='#b3b3b3')
    label_show_quads.grid(row=1, column=0, sticky='w', pady=5)
    entry_show_quads = tk.Entry(screen, width=10, bg='#b3b3b3', relief='solid', textvariable=var_show_quads)
    entry_show_quads.grid(row=1, column=1)

    return [var_person_display_size, var_show_quads]


def setup_tab3(screen: tk.Frame) -> list[tk.StringVar]:
    return []


def setup_start_area(screen: tk.Tk) -> tk.Frame:
    start_area = tk.Frame(screen)
    start_area.pack(fill='both', expand=True)
    start_area.configure(bg='#9a9a9a')

    return start_area


def setup_start_area_buttons(screen: tk.Frame, widgets: list[tk.StringVar]) -> None:
    # create save button
    save_button = tk.Button(screen, text='Save', background='#9a9a9a', height=1, width=1,
                            command=lambda: create_save_window(widgets))
    save_button.pack(side='left', expand=True, fill='both')

    # create load button
    load_button = tk.Button(screen, text='Load', background='#9a9a9a', height=1, width=1,
                            command=lambda: create_load_window(widgets))
    load_button.pack(side='left', expand=True, fill='both')

    # create start button
    start_button = tk.Button(screen, text='Start Simulation', background='#06ba00', height=1, width=1,
                             command=lambda: start_simulation(widgets))
    start_button.pack(side='left', expand=True, fill='both')


def create_save_window(widgets: list[tk.StringVar]) -> None:
    save_window = tk.Toplevel(root)
    save_window.title('Save')
    save_window.geometry('160x120')
    save_window.configure(bg='#b3b3b3', borderwidth=20)
    save_window.focus()

    label_save_as = tk.Label(save_window, text='Save as:', bg='#b3b3b3', pady=5)
    label_save_as.grid(row=0, column=0, sticky='W', pady=5)

    user_input = tk.StringVar()
    entry_save_as = tk.Entry(save_window, width=10, bg='#b3b3b3', relief='solid', textvariable=user_input)
    entry_save_as.grid(row=0, column=1)
    entry_save_as.focus()

    btn_save = tk.Button(save_window, text='Save', bg='#b3b3b3', width=10, pady=5,
                         command=lambda: save_settings(user_input.get().lower(), widgets, save_window))
    btn_save.grid(row=1, column=0, columnspan=2)


def create_load_window(widgets: list[tk.StringVar]) -> None:
    load_window = tk.Toplevel(root)
    load_window.title('Save')
    load_window.geometry('160x120')
    load_window.configure(bg='#b3b3b3', borderwidth=20)
    load_window.focus()

    with open("saved_settings.json", mode="r", encoding="utf-8") as read_file:
        settings = json.load(read_file)
        settings_list = list(settings.keys())

    # datatype of menu text
    clicked = tk.StringVar()

    # initial menu text
    clicked.set("default")

    # Create Dropdown menu
    drop = tk.OptionMenu(load_window, clicked, *settings_list)
    drop.configure(bg='#b3b3b3', relief='solid', pady=5, highlightbackground='#b3b3b3')
    drop.pack()

    # label_load = tk.Label(load_window, text='Load:', bg='#b3b3b3', pady=5)
    # label_load.grid(row=0, column=0, sticky='W')
    #
    # user_input = tk.StringVar()
    # entry_load = tk.Entry(load_window, width=10, bg='#b3b3b3', relief='solid', textvariable=user_input)
    # entry_load.grid(row=0, column=1)
    # entry_load.focus()

    btn_load = tk.Button(load_window, text='Load', bg='#b3b3b3', width=10, pady=5,
                         command=lambda: load_settings(clicked.get().lower(), widgets, load_window))
    btn_load.pack(pady=5)


def start_simulation(widgets: list[tk.StringVar]) -> None:
    pass


def get_settings(widgets: list[tk.StringVar]) -> dict:
    var_pop_count, var_infection_radius, var_sick_start_percentage, var_healthy_start_percentage, \
        var_infection_chance, var_immune_chance, var_group_count, var_person_display_size, var_show_quads = widgets

    population_count = var_pop_count.get()
    infection_radius = var_infection_radius.get()
    sick_start_percentage = var_sick_start_percentage.get()
    healthy_start_percentage = var_healthy_start_percentage.get()
    infection_chance = var_infection_chance.get()
    immune_chance = var_immune_chance.get()
    group_count = var_group_count.get()
    person_display_size = var_person_display_size.get()
    show_quads = var_show_quads.get()

    return {
        "population_count": population_count,
        "infection_radius": infection_radius,
        "healthy_start_percentage": healthy_start_percentage,
        "sick_start_percentage": sick_start_percentage,
        "infection_chance": infection_chance,
        "immune_chance": immune_chance,
        "person_display_size": person_display_size,
        "show_quads": show_quads,
        "group_count": group_count
    }


def check_settings(widgets: list[tk.StringVar]) -> bool:
    var_pop_count, var_infection_radius, var_sick_start_percentage, var_healthy_start_percentage, \
        var_infection_chance, var_immune_chance, var_group_count, var_person_display_size, var_show_quads = widgets

    # ensure all inputs match correct data type
    try:
        population_count = int(var_pop_count.get())
        infection_radius = int(var_infection_radius.get())
        sick_start_percentage = float(var_sick_start_percentage.get())
        healthy_start_percentage = float(var_healthy_start_percentage.get())
        infection_chance = float(var_infection_chance.get())
        immune_chance = float(var_immune_chance.get())
        group_count = int(var_group_count.get())
        person_display_size = int(var_person_display_size.get())
        show_quads = var_show_quads.get().lower()

    except ValueError:
        tk.messagebox.showwarning(title='Wrong Value', message='Unknown or incorrect value was given')
        return False

    # ensure all values fall within an acceptable range
    if population_count < 0:
        tk.messagebox.showwarning(title='Wrong Value', message='Population Count cannot be negative')
        return False

    if infection_radius < 0:
        tk.messagebox.showwarning(title='Wrong Value', message='Infection Radius cannot be negative')
        return False

    if not (0 < sick_start_percentage < 1):
        tk.messagebox.showwarning(title='Wrong Value', message='Sick Start Percentage must be between 0 and 1')
        return False

    if not (0 < healthy_start_percentage < 1):
        tk.messagebox.showwarning(title='Wrong Value', message='Health Start Percentage must be between 0 and 1')
        return False

    if not (0 < infection_chance < 1):
        tk.messagebox.showwarning(title='Wrong Value', message='Infection Chance must be between 0 and 1')
        return False

    if not (0 < immune_chance < 1):
        tk.messagebox.showwarning(title='Wrong Value', message='Immune Chance must be between 0 and 1')
        return False

    if group_count < 0 or group_count > 4:
        tk.messagebox.showwarning(title='Wrong Value', message='Group Count must be between 1 and 4 inclusive')
        return False

    if person_display_size < 0:
        tk.messagebox.showwarning(title='Wrong Value', message='Person Display Size cannot be negative')
        return False

    # ensure start percentages add up to one
    if sick_start_percentage + healthy_start_percentage != 1:
        tk.messagebox.showwarning(title='Wrong Value',
                                  message='Sick Start Percentage and Healthy Start Percentage must add up to 100%')
        return False

    # ensure show quads is a bool
    if show_quads not in ['true', 't', 'false', 'f']:
        tk.messagebox.showwarning(title='Wrong Value', message='Show Quads must be either "True" or "False"')
        return False

    return True


def load_settings(settings_name: str, widgets: list[tk.StringVar], window: tk.Toplevel = None) -> None:
    with open("saved_settings.json", mode="r", encoding="utf-8") as read_file:
        settings = json.load(read_file)
        settings = settings[settings_name]

    var_pop_count, var_infection_radius, var_sick_start_percentage, var_healthy_start_percentage, var_infection_chance, var_immune_chance, var_group_count, var_person_display_size, var_show_quads = widgets

    var_pop_count.set(str(settings['population_count']))
    var_infection_radius.set(str(settings['infection_radius']))
    var_sick_start_percentage.set(str(settings['sick_start_percentage']))
    var_healthy_start_percentage.set(str(settings['healthy_start_percentage']))
    var_infection_chance.set(str(settings['infection_chance']))
    var_immune_chance.set(str(settings['immune_chance']))
    var_group_count.set(str(settings['group_count']))
    var_person_display_size.set(str(settings['person_display_size']))
    var_show_quads.set(str(settings['show_quads']))

    if window is not None:
        tk.messagebox.showinfo(title='Saved', message=f'Successfully loaded "{settings_name}" settings')
        window.destroy()


def save_settings(settings_name: str, widgets: list[tk.StringVar], this_window) -> None:
    # get all existing saves
    with open("saved_settings.json", mode="r", encoding="utf-8") as read_file:
        settings = json.load(read_file)
        settings_list = list(settings.keys())

        # double check before overwriting existing save
        if settings_name in settings_list and settings_name != 'default':
            if not tk.messagebox.askyesno(title='Overwrite Save?',
                                          message=f'Are you sure you want to overwrite "{settings_name}" save file?'):
                this_window.destroy()

    # stops user from overwriting the default settings
    if settings_name == 'default':
        tk.messagebox.showerror(title='Error!', message='Cannot overwrite default settings')
    else:
        # save settings
        if check_settings(widgets):
            settings[settings_name] = get_settings(widgets)
            with open("saved_settings.json", mode="w", encoding="utf-8") as write_file:
                json.dump(settings, write_file)
            tk.messagebox.showinfo(title='Saved', message=f'Current settings successfully saved as "{settings_name}"')
        else:
            tk.messagebox.showwarning(title='Error', message=f'Failed to save settings')

    this_window.destroy()


if __name__ == '__main__':
    # create the main application window
    root = tk.Tk()
    root.title("Pandemic Simulation Settings")
    root.geometry("400x500")

    # setup gui
    setup_theme()
    main_notebook = setup_notebook(root)
    main_tab1, main_tab2, main_tab3 = setup_tabs(main_notebook)
    tab1_widgets = setup_tab1(main_tab1)
    tab2_widgets = setup_tab2(main_tab2)
    tab3_widgets = setup_tab3(main_tab3)

    main_widgets = tab1_widgets + tab2_widgets + tab3_widgets

    main_start_area = setup_start_area(root)
    setup_start_area_buttons(main_start_area, main_widgets)

    load_settings('default', main_widgets)

    # Run the application
    root.mainloop()
