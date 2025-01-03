from tkinter import *
from tkinter import messagebox, Label
import json
from tkinter.ttk import Label
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MainPanel:
    def __init__(self, window, next, previous):
        self.main_frame = Frame(window)
        self.main_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.pokemon_bg = PhotoImage(file="pokedex_bg.png")
        self.pokemon_img = PhotoImage(file="assets/1.png")

        self.canvas = Canvas(self.main_frame, width=270, height=480, bg="#DC0A2D")
        self.canvas.create_image(135, 240, image=self.pokemon_bg)
        self.canvas.pack()
        self.canvas_image = self.canvas.create_image(135, 200, image=self.pokemon_img)
        self.pokemon_name = self.canvas.create_text(135, 300, text="Bulbasaur #001", font=("Courier", 17, "bold"))

        self.next_btn = Button(self.canvas, text="Next", command=next)
        self.next_btn.config(width=10)
        self.next_btn.place(x=170, y=400)

        self.prev_btn = Button(self.canvas, text="Previous", command=previous)
        self.prev_btn.config(width=10)
        self.prev_btn.place(x=40, y=400)

    def update_main_panel(self, new_pokemon, pokemon_images):
        pokemon_number = str(new_pokemon['pokedex_number'])
        if pokemon_number not in pokemon_images:
            pokemon_images[pokemon_number] = PhotoImage(file=f"assets/{pokemon_number}.png")

        self.canvas.itemconfig(self.canvas_image, image=pokemon_images[pokemon_number])
        self.canvas.itemconfig(self.pokemon_name, text=f"{new_pokemon['name']} #{pokemon_number.zfill(3)}")


class SearchPanel:
    def __init__(self, window, search):
        self.search_frame = Frame(window, background="#DC0A2D")
        self.search_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")
        self.search_frame.config(padx=100, pady=10)

        self.user_input = Entry(self.search_frame)
        self.user_input.grid(row=0, column=0)
        self.user_input.config(width=50)

        self.search_btn = Button(self.search_frame, text="Search", command=search)
        self.search_btn.grid(row=0, column=2)


class InfoPanel:
    def __init__(self, window, pokemon_data, type_colors):
        self.info_frame = LabelFrame(window, width=250, height=200)
        self.info_frame.grid(row=1, column=1, sticky="nsew")
        self.info_frame.grid_propagate(False)  # Prevent frame from resizing
        self.info_frame.config(padx=75, pady=30)

        self.type_label = Label(self.info_frame, text="Type", font=("Courier", 10, "bold"))
        self.type_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        self.type1_label = Label(self.info_frame, text=pokemon_data["type1"], font=("Courier", 10, "bold"),
                                 background=type_colors["grass"], foreground="white")
        self.type1_label.grid(row=1, column=0, padx=(0, 5))
        self.type2_label = Label(self.info_frame, text=pokemon_data["type2"], font=("Courier", 10, "bold"),
                                 background=type_colors["poison"], foreground="white")
        self.type2_label.grid(row=1, column=1)

        self.height_title = Label(self.info_frame, text="Height", font=("Courier", 10, "bold"))
        self.height_title.grid(row=2, column=0, columnspan=2, pady=(15, 0))
        self.height_value = Label(self.info_frame, text="0.7 m", font=("Courier", 15, "bold"))
        self.height_value.grid(row=3, column=0, columnspan=2)

        self.weight_title = Label(self.info_frame, text="Weight", font=("Courier", 10, "bold"))
        self.weight_title.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        self.weight_value = Label(self.info_frame, text="6.9 kg", font=("Courier", 15, "bold"))
        self.weight_value.grid(row=5, column=0, columnspan=2)

    def update_info(self, new_pokemon, type_colors):
        self.type1_label.config(text=new_pokemon['type1'], background=type_colors[new_pokemon['type1'].lower()])
        try:
            self.type2_label.config(text=new_pokemon['type2'], background=type_colors[new_pokemon['type2'].lower()])
        except KeyError:
            self.type2_label.pack_forget()

        # Update measurements
        self.height_value.config(text=f"{new_pokemon['height_m']} m")
        self.weight_value.config(text=f"{new_pokemon['weight_kg']} kg")


class AbilityPanel:
    def __init__(self, window, pokemon_data):
        self.ability_frame = LabelFrame(window, width=250, height=200)
        self.ability_frame.grid(row=1, column=2, sticky="nsew")
        self.ability_frame.grid_propagate(False)
        self.ability_frame.config(pady=30, padx=75)

        self.species_title = Label(self.ability_frame, text="Species", font=("Courier", 10, "bold"))
        self.species_title.pack(pady=(0, 5))
        self.species_value = Label(self.ability_frame, text=pokemon_data["classfication"].split(" ")[0],
                                   font=("Courier", 15, "bold"))
        self.species_value.pack(pady=(0, 15))

        self.abilities_title = Label(self.ability_frame, text="Abilities", font=("Courier", 10, "bold"))
        self.abilities_title.pack(pady=(0, 5))
        self.abilities_list = pokemon_data["abilities"].strip('[]').replace("'", "").split(", ")

        for i, ability in enumerate(self.abilities_list):
            self.ability_label = Label(self.ability_frame, text=ability, font=("Courier", 15, "bold"))
            pady = (0, 10) if i < len(self.abilities_list) - 1 else 0
            self.ability_label.pack(pady=pady)

    def update_ability_panel(self, new_pokemon):
        self.species_value.config(text=new_pokemon["classfication"].split(" ")[0])

        # Update abilities
        # First, clear existing ability labels
        for widget in self.ability_frame.winfo_children():
            if widget not in (self.species_title, self.species_value, self.abilities_title):
                widget.destroy()

        # Add new ability labels
        self.abilities_list = new_pokemon["abilities"].strip('[]').replace("'", "").split(", ")[:2]
        for i, ability in enumerate(self.abilities_list):
            self.ability_label = Label(self.ability_frame, text=ability, font=("Courier", 15, "bold"))
            pady = (0, 10) if i < len(self.abilities_list) - 1 else 0
            self.ability_label.pack(pady=pady)


class DefensePanel:
    def __init__(self, window, pokemon_data, type_colors):
        self.defense_frame = LabelFrame(window, width=250, height=150)
        self.defense_frame.grid(row=2, column=2, sticky="nsew")
        self.defense_frame.grid_propagate(False)

        self.weak_frame = Frame(self.defense_frame)
        self.weak_frame.pack(pady=(0, 15))
        Label(self.weak_frame, text="Weaknesses", font=("Courier", 10, "bold")).pack(pady=(0, 5))

        self.type_defenses = [key for key in pokemon_data.keys() if "against" in key]
        self.weak_types_frame = Frame(self.weak_frame)
        self.weak_types_frame.pack()

        self.weak_overflow_frame = None
        self.resist_overflow_frame = None

        self.resist_frame = Frame(self.defense_frame)
        self.resist_frame.pack()
        Label(self.resist_frame, text="Resistances", font=("Courier", 10, "bold")).pack()

        self.resist_types_frame = Frame(self.resist_frame)
        self.resist_types_frame.pack()

        self.update_defense_pane(pokemon_data, type_colors)

    def update_defense_pane(self, new_pokemon, type_colors):
        for widget in self.weak_types_frame.winfo_children():
            widget.destroy()
        for widget in self.resist_types_frame.winfo_children():
            widget.destroy()

        if self.weak_overflow_frame:
            self.weak_overflow_frame.destroy()
            self.weak_overflow_frame = None
        if self.resist_overflow_frame:
            self.resist_overflow_frame.destroy()
            self.resist_overflow_frame = None

        weak_types = [defense for defense in self.type_defenses if float(new_pokemon[defense]) > 1]
        resist_types = [defense for defense in self.type_defenses if float(new_pokemon[defense]) < 1]

        for i, defense in enumerate(weak_types):
            type_name = defense.split("_")[1]
            frame = self.weak_types_frame if i < 3 else self.get_weak_overflow_frame()
            weak_type = Label(frame, text=type_name, font=("Courier", 10, "bold"), background=type_colors[type_name.lower()], foreground="white")
            weak_type.pack(side="left", padx=2)

        for i, defense in enumerate(resist_types):
            type_name = defense.split("_")[1]
            frame = self.resist_types_frame if i < 3 else self.get_resist_overflow_frame()
            res_type = Label(frame, text=type_name, font=("Courier", 10, "bold"),
                             background=type_colors[type_name.lower()], foreground="white")
            res_type.pack(side="left", padx=2)

    def get_weak_overflow_frame(self):
        if not self.weak_overflow_frame:
            self.weak_overflow_frame = Frame(self.weak_frame)
            self.weak_overflow_frame.pack(pady=(5, 0))
        return self.weak_overflow_frame

    def get_resist_overflow_frame(self):
        if not self.resist_overflow_frame:
            self.resist_overflow_frame = Frame(self.resist_frame)
            self.resist_overflow_frame.pack(pady=(5, 0))
        return self.resist_overflow_frame


class StatsPanel:
    def __init__(self, window, pokemon_data):
        self.fig = Figure(figsize=(3, 2), facecolor='none')
        self.stats_names_list = ['HP', 'ATK', 'DEF', 'SPA', 'SPD', 'SPE']
        self.stats_list = list(map(int, [pokemon_data["hp"], pokemon_data["attack"], pokemon_data["defense"],
                                         pokemon_data["sp_attack"], pokemon_data["sp_defense"], pokemon_data["speed"]]))
        self.plot1 = self.fig.add_subplot(111)
        self.bars = self.plot1.barh(self.stats_names_list, self.stats_list,
                                    color=['#FF5959', '#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3'])

        self.plot1.set_frame_on(False)
        self.plot1.tick_params(left=False, bottom=False)
        self.plot1.get_xaxis().set_visible(False)
        self.plot1.set_xlim(0, max(self.stats_list) + 10)

        for spine in self.plot1.spines.values():
            spine.set_visible(False)

        for bar in self.bars:
            width = bar.get_width()
            self.plot1.text(width, bar.get_y() + bar.get_height() / 2, f'{int(width)}', va='center', fontsize=8,
                            fontweight='bold')

        self.fig.tight_layout()
        self.stats_frame = LabelFrame(window, width=250, height=200)
        self.stats_frame.grid(row=2, column=1, sticky="nsew")
        self.stats_frame.grid_propagate(False)
        self.stats_canvas = FigureCanvasTkAgg(self.fig, master=self.stats_frame)
        self.stats_canvas.draw()
        self.stats_canvas.get_tk_widget().pack()

    def update_stats_panel(self, new_pokemon):
        self.stats_list = list(map(int, [new_pokemon["hp"], new_pokemon["attack"], new_pokemon["defense"],
                                         new_pokemon["sp_attack"], new_pokemon["sp_defense"], new_pokemon["speed"]]))

        self.plot1.clear()
        bars_updated = self.plot1.barh(self.stats_names_list, self.stats_list,
                                       color=['#FF5959', '#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3'])
        self.plot1.set_frame_on(False)
        self.plot1.tick_params(left=False, bottom=False)
        self.plot1.get_xaxis().set_visible(False)
        self.plot1.set_xlim(0, max(self.stats_list) + 10)

        for spine_ in self.plot1.spines.values():
            spine_.set_visible(False)

        # Add value labels to the bars
        for bar in bars_updated:
            width = bar.get_width()
            self.plot1.text(width, bar.get_y() + bar.get_height() / 2, f'{int(width)}', va='center', fontsize=8,
                            fontweight='bold')

        # fig.tight_layout()
        self.stats_canvas.draw()


class DataManager:
    def __init__(self):
        self.type_colors = {
            'normal': '#A8A878', 'fire': '#F08030', 'water': '#6890F0',
            'electric': '#F8D030', 'grass': '#78C850', 'ice': '#98D8D8',
            'fight': '#C03028', 'poison': '#A040A0', 'ground': '#E0C068',
            'flying': '#A890F0', 'psychic': '#F85888', 'bug': '#A8B820',
            'rock': '#B8A038', 'ghost': '#705898', 'dragon': '#7038F8',
            'dark': '#705848', 'steel': '#B8B8D0', 'fairy': '#EE99AC'
        }
        self.default_pokemon = self.load_data()["Bulbasaur"]
        self.pokemon_list = list(self.load_data().keys())
        self.pokemon_images = {}
        self.current_pokemon_idx = 1

    def load_data(self):
        with open("pokemon.json") as json_file:
            data = json.load(json_file)
            return data

    def load_new_data(self, new_pokemon):
        try:
            with open("pokemon.json") as json_file:
                data = json.load(json_file)
                pokemon_list = list(data.keys())
                self.current_pokemon_idx = pokemon_list.index(new_pokemon)
                return data[new_pokemon]

        except KeyError as e:
            messagebox.showwarning("Error", f"{e} doesn't exist! Check your input again")


class Pokedex(Tk):
    def __init__(self):
        super().__init__()
        self.config(background="#DC0A2D", height=500, width=500)
        self.maxsize(height=500, width=825)

        self.data_manager = DataManager()

        self.search_panel = SearchPanel(self, self.search)
        self.main_panel = MainPanel(self, self.next, self.previous)
        self.info_panel = InfoPanel(self, self.data_manager.default_pokemon, self.data_manager.type_colors)
        self.ability_panel = AbilityPanel(self, self.data_manager.default_pokemon)
        self.defense_panel = DefensePanel(self, self.data_manager.default_pokemon, self.data_manager.type_colors)
        self.stats_panel = StatsPanel(self, self.data_manager.default_pokemon)

    def render_pokedex(self, new_pokemon_data):
        self.info_panel.update_info(new_pokemon_data, self.data_manager.type_colors)
        self.ability_panel.update_ability_panel(new_pokemon_data)
        self.defense_panel.update_defense_pane(new_pokemon_data, self.data_manager.type_colors)
        self.stats_panel.update_stats_panel(new_pokemon_data)
        self.main_panel.update_main_panel(new_pokemon_data, self.data_manager.pokemon_images)
        print(self.data_manager.current_pokemon_idx)

    def search(self):
        user_search = self.search_panel.user_input.get().title()
        new_pokemon_data = self.data_manager.load_new_data(user_search)
        self.render_pokedex(new_pokemon_data)

    def next(self):
        if self.data_manager.current_pokemon_idx < len(self.data_manager.pokemon_list) - 1:
            self.data_manager.current_pokemon_idx += 1
            new_pokemon_data = self.data_manager.load_new_data(
                self.data_manager.pokemon_list[self.data_manager.current_pokemon_idx]
            )
            self.render_pokedex(new_pokemon_data)
        else:
            messagebox.showinfo("Info", "You've reached the last Pokémon!")

    def previous(self):
        if self.data_manager.current_pokemon_idx > 0:
            self.data_manager.current_pokemon_idx -= 1
            new_pokemon_data = self.data_manager.load_new_data(
                self.data_manager.pokemon_list[self.data_manager.current_pokemon_idx]
            )
            self.render_pokedex(new_pokemon_data)
        else:
            messagebox.showinfo("Info", "You're at the first Pokémon!")


pokedex = Pokedex()
pokedex.mainloop()


