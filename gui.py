import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, Grid
from tkinter.colorchooser import askcolor
from CustomCardParam import Medal, write_card_param, read_card_param
from PlayerColorParam import write_color_param, read_color_param, Color
from DuelPlayerParam import read_dpp_Xfbin, read_prm_bas, PRM_bas
from CharaCode import read_chara_code, write_chara_code, Character


class StoreStuff:

    def __init__(self):
        self.colors = []
        self.custom_cards = []

Multicopy = StoreStuff()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #set defaults
        self.title("ASBR Tools")
        self.geometry("500x300")
        
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        Grid.grid_rowconfigure(self.frame, 0, weight=1)
        Grid.grid_rowconfigure(self.frame, 1, weight=1)
        '''Grid.grid_rowconfigure(self.frame, 2, weight=1)
        Grid.grid_rowconfigure(self.frame, 3, weight=1)
        Grid.grid_rowconfigure(self.frame, 4, weight=1)'''
        #Grid.grid_rowconfigure(self.frame, 5, weight=1)
        Grid.grid_columnconfigure(self.frame, 0, weight=1)
        Grid.grid_columnconfigure(self.frame, 1, weight=1)
        Grid.grid_columnconfigure(self.frame, 2, weight=1)
        '''Grid.grid_rowconfigure(self.frame, 0, weight=1)
        Grid.grid_columnconfigure(self.frame, 0, weight=1)'''


        # use grid to place widgets
        self.custom_card_button = tk.Button(self.frame, text="Custom Card Param Editor", command=self.open_custom_card)
        self.custom_card_button.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.player_color_button = tk.Button(self.frame, text="Player Color Param Editor", command=self.open_player_color)
        self.player_color_button.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.chara_viewer_button = tk.Button(self.frame, text="Character Viewer Param Editor", command=self.open_chara_viewer)
        self.chara_viewer_button.grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5)

        self.duel_player_button = tk.Button(self.frame, text="Duel Player Param Editor", command=self.open_duel_player)
        self.duel_player_button.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.chara_code_button = tk.Button(self.frame, text="Character Code Editor", command=self.open_chara_code)
        self.chara_code_button.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)

    
    def open_custom_card(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = CustomCardGUI(self.new_window)
    
    def open_player_color(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = PlayerColorGUI(self.new_window)
    
    def open_duel_player(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = DuelPlayerGUI(self.new_window)
    
    def open_chara_viewer(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = CharaViewerGUI(self.new_window)
    
    def open_chara_code(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = CharaCodeGUI(self.new_window)

class CustomCardGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Custom Card Param Editor")
        self.master.geometry("800x600")
        self.pack(fill=tk.BOTH, expand=True)

        self.medals = []
        self.copied_medal = None
        self.old_path = ""
        self.selected_medal = None

        #master frame
        Grid.columnconfigure(self, 0, weight=1, uniform="group1")
        Grid.columnconfigure(self, 1, weight=1, uniform="group1")
        Grid.rowconfigure(self, 0, weight=0, uniform="group2")
        Grid.rowconfigure(self, 1, weight=5, uniform="group2")

        #make multiple frames for each section
        self.frame_l_up = tk.Frame(self)
        self.frame_l_up.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame_l_down = tk.Frame(self)
        self.frame_l_down.grid(row=1, column=0, sticky=tk.NSEW)
        self.frame_r = tk.Frame(self)
        self.frame_r.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)

        

        #left upper buttons
        self.frame_l_up.grid_rowconfigure(0, weight=1)
        self.frame_l_up.grid_columnconfigure(0, weight=1)
        self.frame_l_up.grid_columnconfigure(1, weight=1)
        self.frame_l_up.grid_columnconfigure(2, weight=1)
        self.frame_l_up.grid_columnconfigure(3, weight=1)
        self.open_button = tk.Button(self.frame_l_up, text="Open", command=self.open_file)
        self.open_button.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.save_button = tk.Button(self.frame_l_up, text="Save", command=self.save_file)
        self.save_button.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)
        self.quick_save_button = tk.Button(self.frame_l_up, text="Quick Save", command=self.quick_save_file)
        self.quick_save_button.grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5)
        self.auto_save_bool = tk.BooleanVar()
        self.auto_save_button = tk.Checkbutton(self.frame_l_up, text="Auto Save", variable=self.auto_save_bool)
        self.auto_save_button.grid(row=0, column=3, sticky=tk.NSEW, padx=5, pady=5)

        #left lower frame
        Grid.columnconfigure(self.frame_l_down, 0, weight=1)
        Grid.columnconfigure(self.frame_l_down, 1, weight=1)
        Grid.columnconfigure(self.frame_l_down, 2, weight=1)
        Grid.columnconfigure(self.frame_l_down, 3, weight=1)
        Grid.columnconfigure(self.frame_l_down, 4, weight=0)
        Grid.rowconfigure(self.frame_l_down, 0, weight=1)
        Grid.rowconfigure(self.frame_l_down, 1, weight=0)
        self.listbox = tk.Listbox(self.frame_l_down)
        self.listbox.grid(row=0, column=0, sticky=tk.NSEW, columnspan=4)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_select)
        self.listbox.configure(exportselection=False, selectmode=tk.EXTENDED)

        self.scrollbar = tk.Scrollbar(self.frame_l_down, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=4, sticky=tk.NS)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_button = tk.Button(self.frame_l_down, text="Add", command=self.add_medal)
        self.add_button.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.remove_button = tk.Button(self.frame_l_down, text="Remove", command=self.remove_medal)
        self.remove_button.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)
        self.copy_medal_button = tk.Button(self.frame_l_down, text="Copy Medal", command=self.copy_multiple)
        self.copy_medal_button.grid(row=1, column=2, sticky=tk.NSEW, padx=5, pady=5)
        self.paste_medal_button = tk.Button(self.frame_l_down, text="Paste Medal", command=self.paste_multiple)#, state=tk.DISABLED)
        self.paste_medal_button.grid(row=1, column=3, sticky=tk.NSEW, padx=5, pady=5)
        

        #right frame
        Grid.columnconfigure(self.frame_r, 0, weight=1)
        Grid.columnconfigure(self.frame_r, 1, weight=1)
        Grid.columnconfigure(self.frame_r, 2, weight=1)
        Grid.columnconfigure(self.frame_r, 3, weight=1)
        Grid.rowconfigure(self.frame_r, 0, weight=1)
        Grid.rowconfigure(self.frame_r, 1, weight=1)
        Grid.rowconfigure(self.frame_r, 2, weight=1)
        Grid.rowconfigure(self.frame_r, 3, weight=1)
        Grid.rowconfigure(self.frame_r, 4, weight=1)
        Grid.rowconfigure(self.frame_r, 5, weight=1)
        Grid.rowconfigure(self.frame_r, 6, weight=1)
        Grid.rowconfigure(self.frame_r, 7, weight=1)
        Grid.rowconfigure(self.frame_r, 8, weight=1)
        Grid.rowconfigure(self.frame_r, 9, weight=1)
        Grid.rowconfigure(self.frame_r, 10, weight=1)
        Grid.rowconfigure(self.frame_r, 11, weight=1)
        Grid.rowconfigure(self.frame_r, 12, weight=1)
        Grid.rowconfigure(self.frame_r, 13, weight=1)
        Grid.rowconfigure(self.frame_r, 14, weight=1)
        Grid.rowconfigure(self.frame_r, 15, weight=1)
        Grid.rowconfigure(self.frame_r, 16, weight=1)
        self.card_id_label = tk.Label(self.frame_r, text="Card ID")
        self.card_id_label.grid(row=0, column=0, sticky=tk.NSEW, columnspan=4)
        self.card_id_input = tk.Entry(self.frame_r)
        self.card_id_input.grid(row=1, column=0, sticky=tk.NSEW, columnspan=4)

        self.part = tk.Label(self.frame_r, text="Part")
        self.part.grid(row=2, column=0, sticky=tk.NSEW)
        self.part_input = tk.Entry(self.frame_r)
        self.part_input.grid(row=3, column=0, sticky=tk.NSEW)

        self.interaction_label = tk.Label(self.frame_r, text="Interaction")
        self.interaction_label.grid(row=2, column=1, sticky=tk.NSEW)
        self.interaction_input = tk.Entry(self.frame_r)
        self.interaction_input.grid(row=3, column=1, sticky=tk.NSEW)

        self.medal_label = tk.Label(self.frame_r, text="Medal Type")
        self.medal_label.grid(row=2, column=2, sticky=tk.NSEW)
        self.medal_type = tk.Entry(self.frame_r)
        self.medal_type.grid(row=3, column=2, sticky=tk.NSEW)

        self.letter_label = tk.Label(self.frame_r, text="Letter")
        self.letter_label.grid(row=2, column=3, sticky=tk.NSEW)
        self.letter_input = tk.Entry(self.frame_r)
        self.letter_input.grid(row=3, column=3, sticky=tk.NSEW)

        self.sfx1_label = tk.Label(self.frame_r, text="SFX 1")
        self.sfx1_label.grid(row=4, column=0, sticky=tk.NSEW, columnspan=2)
        self.sfx1_input = tk.Entry(self.frame_r)
        self.sfx1_input.grid(row=5, column=0, sticky=tk.NSEW, columnspan=2)

        self.sfx2_label = tk.Label(self.frame_r, text="SFX 2")
        self.sfx2_label.grid(row=4, column=2, sticky=tk.NSEW, columnspan=2)
        self.sfx2_input = tk.Entry(self.frame_r)
        self.sfx2_input.grid(row=5, column=2, sticky=tk.NSEW, columnspan=2)

        self.sfx3_label = tk.Label(self.frame_r, text="SFX 3")
        self.sfx3_label.grid(row=6, column=0, sticky=tk.NSEW, columnspan=2)
        self.sfx3_input = tk.Entry(self.frame_r)
        self.sfx3_input.grid(row=7, column=0, sticky=tk.NSEW, columnspan=2)

        self.sfx4_label = tk.Label(self.frame_r, text="SFX 4")
        self.sfx4_label.grid(row=6, column=2, sticky=tk.NSEW, columnspan=2)
        self.sfx4_input = tk.Entry(self.frame_r)
        self.sfx4_input.grid(row=7, column=2, sticky=tk.NSEW, columnspan=2)

        #unk stuff
        self.unk1_label = tk.Label(self.frame_r, text="Unk 1")
        self.unk1_label.grid(row=8, column=0, sticky=tk.NSEW)
        self.unk1_input = tk.Entry(self.frame_r)
        self.unk1_input.grid(row=9, column=0, sticky=tk.NSEW)

        self.unk2_label = tk.Label(self.frame_r, text="Unk 2")
        self.unk2_label.grid(row=8, column=1, sticky=tk.NSEW)
        self.unk2_input = tk.Entry(self.frame_r)
        self.unk2_input.grid(row=9, column=1, sticky=tk.NSEW)

        self.unk3_label = tk.Label(self.frame_r, text="Unk 3")
        self.unk3_label.grid(row=8, column=2, sticky=tk.NSEW)
        self.unk3_input = tk.Entry(self.frame_r)
        self.unk3_input.grid(row=9, column=2, sticky=tk.NSEW)

        self.unk4_label = tk.Label(self.frame_r, text="Unk 4")
        self.unk4_label.grid(row=8, column=3, sticky=tk.NSEW)
        self.unk4_input = tk.Entry(self.frame_r)
        self.unk4_input.grid(row=9, column=3, sticky=tk.NSEW)

        self.unk5_label = tk.Label(self.frame_r, text="Unk 5")
        self.unk5_label.grid(row=10, column=0, sticky=tk.NSEW)
        self.unk5_input = tk.Entry(self.frame_r)
        self.unk5_input.grid(row=11, column=0, sticky=tk.NSEW)

        self.unk6_label = tk.Label(self.frame_r, text="Unk 6")
        self.unk6_label.grid(row=10, column=1, sticky=tk.NSEW)
        self.unk6_input = tk.Entry(self.frame_r)
        self.unk6_input.grid(row=11, column=1, sticky=tk.NSEW)

        self.patch_label = tk.Label(self.frame_r, text="Patch")
        self.patch_label.grid(row=10, column=2, sticky=tk.NSEW)
        self.patch_input = tk.Entry(self.frame_r)
        self.patch_input.grid(row=11, column=2, sticky=tk.NSEW)

        self.unk8_label = tk.Label(self.frame_r, text="Unk 8")
        self.unk8_label.grid(row=10, column=3, sticky=tk.NSEW)
        self.unk8_input = tk.Entry(self.frame_r)
        self.unk8_input.grid(row=11, column=3, sticky=tk.NSEW)

        self.char_id_label = tk.Label(self.frame_r, text="Character ID")
        self.char_id_label.grid(row=12, column=0, sticky=tk.NSEW)
        self.char_id_input = tk.Entry(self.frame_r)
        self.char_id_input.grid(row=13, column=0, sticky=tk.NSEW)

        self.dlc_id = tk.Label(self.frame_r, text="DLC ID")
        self.dlc_id.grid(row=12, column=1, sticky=tk.NSEW)
        self.dlc_id_input = tk.Entry(self.frame_r)
        self.dlc_id_input.grid(row=13, column=1, sticky=tk.NSEW)

        self.unlock_condition_label = tk.Label(self.frame_r, text="Unlock Condition")
        self.unlock_condition_label.grid(row=12, column=2, sticky=tk.NSEW)
        self.unlock_condition_input = tk.Entry(self.frame_r)
        self.unlock_condition_input.grid(row=13, column=2, sticky=tk.NSEW)

        self.cost_label = tk.Label(self.frame_r, text="Cost")
        self.cost_label.grid(row=12, column=3, sticky=tk.NSEW)
        self.cost_input = tk.Entry(self.frame_r)
        self.cost_input.grid(row=13, column=3, sticky=tk.NSEW)

        self.medal_name_label = tk.Label(self.frame_r, text="Medal Name")
        self.medal_name_label.grid(row=14, column=0, sticky=tk.NSEW)
        self.medal_name_input = tk.Entry(self.frame_r)
        self.medal_name_input.grid(row=15, column=0, sticky=tk.NSEW)

        self.card_detail_label = tk.Label(self.frame_r, text="Card Detail")
        self.card_detail_label.grid(row=14, column=1, sticky=tk.NSEW, columnspan=2)
        self.card_detail_input = tk.Entry(self.frame_r)
        self.card_detail_input.grid(row=15, column=1, sticky=tk.NSEW, columnspan=2)

        self.card_index_label = tk.Label(self.frame_r, text="Card Index")
        self.card_index_label.grid(row=14, column=3, sticky=tk.NSEW)
        self.card_index_input = tk.Entry(self.frame_r)
        self.card_index_input.grid(row=15, column=3, sticky=tk.NSEW)



        self.apply_medal = tk.Button(self.frame_r, text="Apply", command=self.apply_medal)
        self.apply_medal.grid(row=16, column=0, sticky=tk.NSEW, columnspan=4, pady=5)

        
    def open_file(self):
        file = filedialog.askopenfilename(
            filetypes=[("PlayerColorParam", "*.xfbin")]
        )
        if file:
            self.medals = read_card_param(file)
            self.old_path = file

            #clear the listbox
            self.listbox.delete(0, tk.END)

            for i in range(len(self.medals)):
                
                medal = self.medals[i]
                self.listbox.insert(tk.END, f"{medal.CharacterCode} {medal.CardID}")

            #select the first item in the listbox
            if len(self.medals) > 0:
                self.listbox.selection_set(0)
                self.listbox.activate(0)
                self.listbox.event_generate("<<ListboxSelect>>")

    def listbox_select(self, event):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            medal = self.medals[index]

            self.card_id_input.delete(0, tk.END)
            self.medal_type.delete(0, tk.END)
            self.interaction_input.delete(0, tk.END)
            self.letter_input.delete(0, tk.END)
            self.part_input.delete(0, tk.END)
            self.unk1_input.delete(0, tk.END)
            self.unk2_input.delete(0, tk.END)
            self.unk3_input.delete(0, tk.END)
            self.unk4_input.delete(0, tk.END)
            self.unk5_input.delete(0, tk.END)
            self.unk6_input.delete(0, tk.END)
            self.patch_input.delete(0, tk.END)
            self.unk8_input.delete(0, tk.END)
            self.sfx1_input.delete(0, tk.END)
            self.sfx2_input.delete(0, tk.END)
            self.sfx3_input.delete(0, tk.END)
            self.sfx4_input.delete(0, tk.END)
            self.char_id_input.delete(0, tk.END)
            self.dlc_id_input.delete(0, tk.END)
            self.unlock_condition_input.delete(0, tk.END)
            self.cost_input.delete(0, tk.END)
            self.medal_name_input.delete(0, tk.END)
            self.card_detail_input.delete(0, tk.END)
            self.card_index_input.delete(0, tk.END)

            self.card_id_input.insert(0, medal.CardID)
            self.part_input.insert(0, medal.Part)
            self.interaction_input.insert(0, medal.InteractionType)
            self.letter_input.insert(0, medal.Letter)
            self.medal_type.insert(0, medal.MedalType)
            self.unk1_input.insert(0, medal.Unk1)
            self.unk2_input.insert(0, medal.Unk2)
            self.unk3_input.insert(0, medal.Unk3)
            self.unk4_input.insert(0, medal.Unk4)
            self.unk5_input.insert(0, medal.Unk5)
            self.unk6_input.insert(0, medal.Unk6)
            self.patch_input.insert(0, medal.Patch)
            self.unk8_input.insert(0, medal.Unk8)
            self.sfx1_input.insert(0, medal.SFX1)
            self.sfx2_input.insert(0, medal.SFX2)
            self.sfx3_input.insert(0, medal.SFX3)
            self.sfx4_input.insert(0, medal.SFX4)
            self.char_id_input.insert(0, medal.CharacterCode)
            self.dlc_id_input.insert(0, medal.DLCID)
            self.unlock_condition_input.insert(0, medal.UnlockCondition)
            self.cost_input.insert(0, medal.Cost)
            self.medal_name_input.insert(0, medal.Medal)
            self.card_detail_input.insert(0, medal.Detail)
            self.card_index_input.insert(0, medal.Index)

            self.selected_medal = index
            
    def add_medal(self):
        self.listbox.insert(tk.END, f"CCD_CUSTOM_CARD_ID_{len(self.medals) + 1}")
        self.medals.append(Medal())

        self.listbox.selection_set(tk.END)
        self.listbox.activate(tk.END)
        self.listbox.event_generate("<<ListboxSelect>>")
        
    def remove_medal(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            self.medals.pop(index)
            self.listbox.delete(index)
            self.listbox.selection_set(index)
            self.listbox.activate(index)
            self.listbox.event_generate("<<ListboxSelect>>")
    
    def apply_medal(self):
        if self.listbox.curselection():
            index = self.selected_medal
            medal = self.medals[index]

            medal.CardID = self.card_id_input.get()
            medal.Part = int(self.part_input.get())
            medal.InteractionType = int(self.interaction_input.get())
            medal.Letter = self.letter_input.get()
            medal.MedalType = int(self.medal_type.get())
            medal.Unk1 = int(self.unk1_input.get())
            medal.Unk2 = int(self.unk2_input.get())
            medal.Unk3 = int(self.unk3_input.get())
            medal.Unk4 = int(self.unk4_input.get())
            medal.Unk5 = int(self.unk5_input.get())
            medal.Unk6 = int(self.unk6_input.get())
            medal.Patch = int(self.patch_input.get())
            medal.Unk8 = int(self.unk8_input.get())
            medal.SFX1 = self.sfx1_input.get()
            medal.SFX2 = self.sfx2_input.get()
            medal.SFX3 = self.sfx3_input.get()
            medal.SFX4 = self.sfx4_input.get()
            medal.CharacterCode = self.char_id_input.get()
            medal.DLCID = int(self.dlc_id_input.get())
            medal.UnlockCondition = int(self.unlock_condition_input.get())
            medal.Cost = int(self.cost_input.get())
            medal.Medal = self.medal_name_input.get()
            medal.Detail = self.card_detail_input.get()
            medal.Index = int(self.card_index_input.get())

            self.listbox.delete(index)
            self.listbox.insert(index, f"{medal.CharacterCode} {medal.CardID}")
            self.listbox.selection_set(index)
            self.listbox.activate(index)
            self.listbox.event_generate("<<ListboxSelect>>")

    def copy_medal(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            medal = self.medals[index]
            self.copied_medal = Medal()
            for key, value in medal.__dict__.items():
                setattr(self.copied_medal, key, value)
            self.paste_medal_button.config(state=tk.NORMAL)
    
    def copy_multiple(self):
        if self.listbox.curselection():
            Multicopy.custom_cards.clear()

            for i in self.listbox.curselection():
                medal = self.medals[i]
                Multicopy.custom_cards.append(medal)
        
    def paste_medal(self):
        if self.copied_medal:
            self.medals.append(self.copied_medal)
            print(f"medals count: {len(self.medals)}")

            self.listbox.insert(tk.END, f"{self.copied_medal.CharacterCode} {self.copied_medal.CardID}")
            self.listbox.selection_set(tk.END)
            self.listbox.activate(tk.END)
            self.listbox.event_generate("<<ListboxSelect>>")
    
    def paste_multiple(self):
        for i in Multicopy.custom_cards:
            self.medals.append(i)
            print(f"medals count: {len(self.medals)}")

            self.listbox.insert(tk.END, f"{i.CharacterCode} {i.CardID}")
            self.listbox.selection_set(tk.END)
            self.listbox.activate(tk.END)
            self.listbox.event_generate("<<ListboxSelect>>")

    def validate_int_entry(self, new_text):
        if not new_text: # the field is being cleared
            return True
        
        if len(new_text) > 3:
            return False
        else:
            try:
                int(new_text)
                return True
            except ValueError:
                return False
        
    def validate_entry(self, new_text):
        if not new_text:
            return True

        if len(new_text) > 8:
            return False
        else:
            return True


    def save_file(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".xfbin",
            filetypes=[("CustomCardParam", "*.xfbin")]
        )
        if file:
            write_card_param(self.medals, file)

            tk.messagebox.showinfo("Success", "File saved")
    
    def quick_save_file(self):
        if self.old_path:
            write_card_param(self.medals, self.old_path)
        else:
            tk.messagebox.showerror("Error", "No opened file")
    

class PlayerColorGUI(tk.Frame, App):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Player Color Param Editor")
        self.master.geometry("600x300")
        self.pack(fill=tk.BOTH, expand=True)

        self.colors = []
        self.copied_color = None
        self.old_path = ""

        #master frame
        Grid.columnconfigure(self, 0, weight=1, uniform="group1")
        Grid.columnconfigure(self, 1, weight=1, uniform="group1")
        Grid.rowconfigure(self, 0, weight=1, uniform="group2")
        Grid.rowconfigure(self, 1, weight=5, uniform="group2")

        #make multiple frames for each section
        self.frame_l_up = tk.Frame(self)
        self.frame_l_up.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame_l_down = tk.Frame(self)
        self.frame_l_down.grid(row=1, column=0, sticky=tk.NSEW)
        self.frame_r = tk.Frame(self)
        self.frame_r.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)

        

        #left upper buttons
        self.open_button = tk.Button(self.frame_l_up, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.save_button = tk.Button(self.frame_l_up, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.quick_save_button = tk.Button(self.frame_l_up, text="Quick Save", command=self.quick_save_file)
        self.quick_save_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.auto_save_bool = tk.BooleanVar()
        self.auto_save_button = tk.Checkbutton(self.frame_l_up, text="Auto Save", variable=self.auto_save_bool)
        self.auto_save_button.pack(side=tk.LEFT, padx=5, pady=5)

        #left lower frame
        Grid.columnconfigure(self.frame_l_down, 0, weight=1)
        Grid.columnconfigure(self.frame_l_down, 1, weight=1)
        Grid.columnconfigure(self.frame_l_down, 2, weight=1)
        Grid.columnconfigure(self.frame_l_down, 3, weight=1)
        Grid.columnconfigure(self.frame_l_down, 4, weight=0)
        Grid.rowconfigure(self.frame_l_down, 0, weight=1)
        Grid.rowconfigure(self.frame_l_down, 1, weight=0)
        self.listbox = tk.Listbox(self.frame_l_down)
        self.listbox.grid(row=0, column=0, sticky=tk.NSEW, columnspan=4)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_select)
        self.listbox.configure(exportselection=False, selectmode=tk.EXTENDED)

        self.scrollbar = tk.Scrollbar(self.frame_l_down, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=4, sticky=tk.NS)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_button = tk.Button(self.frame_l_down, text="Add", command=self.add_color)
        self.add_button.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.remove_button = tk.Button(self.frame_l_down, text="Remove", command=self.remove_color)
        self.remove_button.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)
        self.copy_color_button = tk.Button(self.frame_l_down, text="Copy Color", command=self.copy_multiple)
        self.copy_color_button.grid(row=1, column=2, sticky=tk.NSEW, padx=5, pady=5)
        self.paste_color_button = tk.Button(self.frame_l_down, text="Paste Color", command=self.paste_multiple) #state=tk.DISABLED)
        self.paste_color_button.grid(row=1, column=3, sticky=tk.NSEW, padx=5, pady=5)
        

        #right frame
        Grid.columnconfigure(self.frame_r, 0, weight=1)
        Grid.columnconfigure(self.frame_r, 1, weight=1)
        Grid.columnconfigure(self.frame_r, 2, weight=1)
        Grid.rowconfigure(self.frame_r, 0, weight=1)
        Grid.rowconfigure(self.frame_r, 1, weight=1)
        Grid.rowconfigure(self.frame_r, 2, weight=1)
        Grid.rowconfigure(self.frame_r, 3, weight=1)
        Grid.rowconfigure(self.frame_r, 4, weight=1)
        Grid.rowconfigure(self.frame_r, 5, weight=1)
        Grid.rowconfigure(self.frame_r, 6, weight=1)
        Grid.rowconfigure(self.frame_r, 7, weight=1)
        Grid.rowconfigure(self.frame_r, 8, weight=1)
        self.chara_code_label = tk.Label(self.frame_r, text="Character Code")
        self.chara_code_label.grid(row=0, column=0, sticky=tk.NSEW, columnspan=3)
        self.chara_code_input = tk.Entry(self.frame_r, validate="key", validatecommand=(self.register(self.validate_entry), "%P"))
        self.chara_code_input.grid(row=1, column=0, sticky=tk.NSEW, columnspan=3)

        self.costume_slot_label = tk.Label(self.frame_r, text="Costume Slot")
        self.costume_slot_label.grid(row=2, column=0, sticky=tk.NSEW, columnspan=3)
        self.costume_slot_input = tk.Entry(self.frame_r, validate="key", validatecommand=(self.register(self.validate_color_entry), "%P"))
        self.costume_slot_input.grid(row=3, column=0, sticky=tk.NSEW, columnspan=3)

        self.color_r_label = tk.Label(self.frame_r, text="Red")
        self.color_r_label.grid(row=4, column=0, sticky=tk.NSEW)

        #limit input to numbers
        self.color_r = tk.Entry(self.frame_r, validate="key", validatecommand=(self.register(self.validate_color_entry), "%P"))
        self.color_r.grid(row=5, column=0, sticky=tk.NSEW)

        self.color_g_label = tk.Label(self.frame_r, text="Green")
        self.color_g_label.grid(row=4, column=1, sticky=tk.NSEW)
        self.color_g = tk.Entry(self.frame_r, validate="key", validatecommand=(self.register(self.validate_color_entry), "%P"))
        self.color_g.grid(row=5, column=1, sticky=tk.NSEW)

        self.color_b_label = tk.Label(self.frame_r, text="Blue")
        self.color_b_label.grid(row=4, column=2, sticky=tk.NSEW)
        self.color_b = tk.Entry(self.frame_r, validate="key", validatecommand=(self.register(self.validate_color_entry), "%P"))
        self.color_b.grid(row=5, column=2, sticky=tk.NSEW)

        #color picker
        self.color_picker = tk.Button(self.frame_r, text="Pick Color", command=self.pick_color)
        self.color_picker.grid(row=6, column=0, sticky=tk.NSEW, columnspan=3)

        #color preview
        self.color_preview = tk.Canvas(self.frame_r, width=100, height=100)
        self.color_preview.grid(row=7, column=0, sticky=tk.NSEW, columnspan=3)

        #Apply button
        self.apply_button = tk.Button(self.frame_r, text="Apply", command=self.apply_color)
        self.apply_button.grid(row=8, column=0, sticky=tk.NSEW, columnspan=3)

        
    def open_file(self):
        file = filedialog.askopenfilename(
            filetypes=[("PlayerColorParam", "*.xfbin")]
        )
        if file:
            self.colors = read_color_param(file)
            self.old_path = file

            #clear the listbox
            self.listbox.delete(0, tk.END)

            for i in range(len(self.colors)):
                
                color = self.colors[i]
                self.listbox.insert(tk.END, f"{color.character_id} {color.costume_slot}")

            #select the first item in the listbox
            if len(self.colors) > 0:
                self.listbox.selection_set(0)
                self.listbox.activate(0)
                self.listbox.event_generate("<<ListboxSelect>>")

    def listbox_select(self, event):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            color = self.colors[index]
            self.chara_code_input.delete(0, tk.END)
            self.costume_slot_input.delete(0, tk.END)
            self.color_r.delete(0, tk.END)
            self.color_g.delete(0, tk.END)
            self.color_b.delete(0, tk.END)


            self.chara_code_input.insert(0, f"{color.character_id}")
            self.costume_slot_input.insert(0, f"{color.costume_slot}")
            self.color_r.insert(0, f"{color.r}")
            self.color_g.insert(0, f"{color.g}")
            self.color_b.insert(0, f"{color.b}")

            self.color_preview.delete("all")
            self.color_preview.create_rectangle(0, 0, 300, 100, fill=f"#{color.r:02x}{color.g:02x}{color.b:02x}")
            
    
    def add_color(self):
        self.listbox.insert(tk.END, "NewCol")
        self.colors.append(Color('dmy00', 0, 0, 0, 0))

        self.listbox.selection_set(tk.END)
        self.listbox.activate(tk.END)
        self.listbox.event_generate("<<ListboxSelect>>")
        

    def remove_color(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            self.colors.pop(index)
            self.listbox.delete(index)
            self.listbox.selection_set(index)
            self.listbox.activate(index)
            self.listbox.event_generate("<<ListboxSelect>>")
    
    def pick_color(self):
        color = askcolor()
        if color:
            self.color_r.delete(0, tk.END)
            self.color_g.delete(0, tk.END)
            self.color_b.delete(0, tk.END)
            self.color_r.insert(0, f"{color[0][0]}")
            self.color_g.insert(0, f"{color[0][1]}")
            self.color_b.insert(0, f"{color[0][2]}")

            self.color_preview.delete("all")
            self.color_preview.create_rectangle(0, 0, 300, 100, fill=f"#{color[0][0]:02x}{color[0][1]:02x}{color[0][2]:02x}")
    
    def apply_color(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            color = self.colors[index]
            color.character_id = self.chara_code_input.get()
            color.costume_slot = int(self.costume_slot_input.get())
            color.r = int(self.color_r.get())
            color.g = int(self.color_g.get())
            color.b = int(self.color_b.get())

            self.listbox.delete(index)
            self.listbox.insert(index, f"{color.character_id} {color.costume_slot}")
            self.listbox.selection_set(index)
            self.listbox.activate(index)
            self.listbox.event_generate("<<ListboxSelect>>")

            if self.old_path != "":
                if self.auto_save_bool.get():
                    write_color_param(self.colors, self.old_path)
    
    def copy_color(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            color = self.colors[index]
            self.copied_color = Color(color.character_id, color.costume_slot, color.r, color.g, color.b)
            self.paste_color_button.config(state=tk.NORMAL)
    
    def copy_multiple(self):
        if self.listbox.curselection():
            Multicopy.colors.clear()

            for i in self.listbox.curselection():
                color = self.colors[i]
                Multicopy.colors.append(color)
                

    def paste_color(self):
        if self.copied_color:
            self.listbox.insert(tk.END, f"{self.copied_color.character_id} {self.copied_color.costume_slot}")
            self.colors.append(self.copied_color)

            self.listbox.selection_set(tk.END)
            self.listbox.activate(tk.END)
            self.listbox.event_generate("<<ListboxSelect>>")
    
    def paste_multiple(self):
        if Multicopy.colors:
            for color in Multicopy.colors:
                self.listbox.insert(tk.END, f"{color.character_id} {color.costume_slot}")
                self.colors.append(color)

                self.listbox.selection_set(tk.END)
                self.listbox.activate(tk.END)
                self.listbox.event_generate("<<ListboxSelect>>")

    def validate_color_entry(self, new_text):
        if not new_text: # the field is being cleared
            return True
        
        if len(new_text) > 3:
            return False
        else:
            try:
                int(new_text)
                return True
            except ValueError:
                return False
        
    def validate_entry(self, new_text):
        if not new_text:
            return True

        if len(new_text) > 8:
            return False
        else:
            return True


    def save_file(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".xfbin",
            filetypes=[("PlayerColorParam", "*.xfbin")]
        )
        if file:
            write_color_param(self.colors, file)
    
    def quick_save_file(self):
        if self.old_path:
            write_color_param(self.colors, self.old_path)
        else:
            tk.messagebox.showerror("Error", "No opened file")


class DuelPlayerGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Duel Player Param Editor")
        self.master.geometry("800x600")
        self.pack(fill=tk.BOTH, expand=True)

        self.dpp_chunks = []
        self.prm_bas = None
        self.copied_dpp = None
        self.old_path = ""

        #master frame
        Grid.columnconfigure(self, 0, weight=1, uniform="group1")
        Grid.columnconfigure(self, 1, weight=1, uniform="group1")
        Grid.rowconfigure(self, 0, weight=0, uniform="group2")
        Grid.rowconfigure(self, 1, weight=5, uniform="group2")
        

        #make multiple frames for each section
        self.frame_l_up = tk.Frame(self)
        self.frame_l_up.grid(row=0, column=0, sticky=tk.NSEW)
        self.frame_l_down = tk.Frame(self)
        self.frame_l_down.grid(row=1, column=0, sticky=tk.NSEW)
        self.frame_r = tk.Frame(self)
        self.frame_r.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)

        #left upper buttons
        self.frame_l_up.grid_rowconfigure(0, weight=1)
        self.frame_l_up.grid_columnconfigure(0, weight=1)
        self.frame_l_up.grid_columnconfigure(1, weight=1)
        self.frame_l_up.grid_columnconfigure(2, weight=1)
        self.frame_l_up.grid_columnconfigure(3, weight=1)
        self.open_button = tk.Button(self.frame_l_up, text="Open", command=self.open_file)
        self.open_button.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.save_button = tk.Button(self.frame_l_up, text="Save")#, command=self.save_file)
        self.save_button.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)
        self.quick_save_button = tk.Button(self.frame_l_up, text="Quick Save")#, command=self.quick_save_file)
        self.quick_save_button.grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5)
        self.auto_save_bool = tk.BooleanVar()
        self.auto_save_button = tk.Checkbutton(self.frame_l_up, text="Auto Save")#, variable=self.auto_save_bool)
        self.auto_save_button.grid(row=0, column=3, sticky=tk.NSEW, padx=5, pady=5)

        #left lower frame
        Grid.columnconfigure(self.frame_l_down, 0, weight=1)
        Grid.columnconfigure(self.frame_l_down, 1, weight=1)
        Grid.columnconfigure(self.frame_l_down, 2, weight=1)
        Grid.columnconfigure(self.frame_l_down, 3, weight=1)
        Grid.columnconfigure(self.frame_l_down, 4, weight=0)
        Grid.rowconfigure(self.frame_l_down, 0, weight=1)
        Grid.rowconfigure(self.frame_l_down, 1, weight=0)
        self.listbox = tk.Listbox(self.frame_l_down)
        self.listbox.grid(row=0, column=0, sticky=tk.NSEW, columnspan=4)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_select)
        self.listbox.configure(exportselection=False)

        self.scrollbar = tk.Scrollbar(self.frame_l_down, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=4, sticky=tk.NS)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_button = tk.Button(self.frame_l_down, text="Add")
        self.add_button.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.remove_button = tk.Button(self.frame_l_down, text="Remove")
        self.remove_button.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)
        self.copy_medal_button = tk.Button(self.frame_l_down, text="Copy DPP")
        self.copy_medal_button.grid(row=1, column=2, sticky=tk.NSEW, padx=5, pady=5)
        self.paste_medal_button = tk.Button(self.frame_l_down, text="Paste DPP")
        self.paste_medal_button.grid(row=1, column=3, sticky=tk.NSEW, padx=5, pady=5)

        #right frame
        self.frame_r.grid_rowconfigure(0, weight=1)
        self.frame_r.grid_rowconfigure(1, weight=1)
        self.frame_r.grid_rowconfigure(2, weight=5)
        self.frame_r.grid_rowconfigure(3, weight=1)
        self.frame_r.grid_columnconfigure(0, weight=1)
        self.frame_r.grid_columnconfigure(1, weight=1)
        self.frame_r.grid_columnconfigure(2, weight=1)
        self.frame_r.grid_columnconfigure(3, weight=1)


        self.chara_code_label = tk.Label(self.frame_r, text="Character Code")
        self.chara_code_label.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        self.chara_code_entry = tk.Entry(self.frame_r)
        self.chara_code_entry.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.prm_bas_label = tk.Label(self.frame_r, text="Prm_bas Code")
        self.prm_bas_label.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.prm_bas_entry = tk.Entry(self.frame_r)
        self.prm_bas_entry.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.stand_code_label = tk.Label(self.frame_r, text="Stand Code")
        self.stand_code_label.grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5)

        self.stand_code_entry = tk.Entry(self.frame_r)
        self.stand_code_entry.grid(row=1, column=2, sticky=tk.NSEW, padx=5, pady=5)

        self.chara_style_label = tk.Label(self.frame_r, text="Style")
        self.chara_style_label.grid(row=0, column=3, sticky=tk.NSEW, padx=5, pady=5)

        self.chara_style_combo = ttk.Combobox(self.frame_r, values=["Unknown", "Vampirism", "Hamon", "Mode", "Stand", "Mounted", "Baoh Armed Phenomenon", "Ogre Street", "Bro and Mammoni", "Best Science in the World"])
        self.chara_style_combo.grid(row=1, column=3, sticky=tk.NSEW, padx=5, pady=5)

        self.CostumeListButton = tk.Button(self.frame_r, text="Costume List", command=self.CostumeList)
        self.CostumeListButton.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)

        self.HurtSpheresButton = tk.Button(self.frame_r, text="Hurt Spheres", command=self.HurtSpheres)
        self.HurtSpheresButton.grid(row=2, column=2, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)

        
        

        
    def open_file(self):
        file = filedialog.askopenfilename(
            filetypes=[("DuelPlayerParam", "*.xfbin")]
        )
        if file:
            self.dpp_chunks = read_dpp_Xfbin(file)
            self.old_path = file

            #clear the listbox
            self.listbox.delete(0, tk.END)

            for i in range(len(self.dpp_chunks)):
                
                dpp_chunk: NuccChunkBinary = self.dpp_chunks[i]

                self.listbox.insert(tk.END, f"{dpp_chunk.name}")

            #select the first item in the listbox
            if len(self.dpp_chunks) > 0:
                self.listbox.selection_set(0)
                self.listbox.activate(0)
                self.listbox.event_generate("<<ListboxSelect>>")
    
    def listbox_select(self, event):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            dpp_chunk: NuccChunkBinary = self.dpp_chunks[index]

            self.prm_bas: PRM_bas = read_prm_bas(dpp_chunk)
            self.chara_code_entry.delete(0, tk.END)
            self.prm_bas_entry.delete(0, tk.END)
            self.stand_code_entry.delete(0, tk.END)

            self.chara_code_entry.insert(0, self.prm_bas.CharacterCode)
            self.prm_bas_entry.insert(0, self.prm_bas.PRM_bas_Code)
            self.stand_code_entry.insert(0, self.prm_bas.StandCode)
            if self.prm_bas.Style != -1:
                self.chara_style_combo.current(self.prm_bas.Style)
            else:
                self.chara_style_combo.current(0)

    #top level for costume list
    def CostumeList(self):
        self.top = tk.Toplevel(self)
        self.top.title("Costume List")
        self.top.geometry("300x300")
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_rowconfigure(1, weight=1)
        self.top.grid_rowconfigure(2, weight=1)
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_columnconfigure(2, weight=1)
        self.top.grid_columnconfigure(3, weight=1)

        self.costume_list = tk.Listbox(self.top, selectmode=tk.SINGLE, exportselection=0)
        self.costume_list.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW, padx=5, pady=5)
        self.costume_list.bind("<<ListboxSelect>>", self.costume_list_select)
        #set max count of items in listbox
        self.costume_list.config(height=16)

        self.scrollbar = tk.Scrollbar(self.top)
        self.scrollbar.grid(row=0, column=4, sticky=tk.NS)

        self.costume_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.costume_list.yview)

        self.costume_code_label = tk.Label(self.top, text="Costume Code")
        self.costume_code_label.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.costume_code_entry = tk.Entry(self.top)
        self.costume_code_entry.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.apply_code_button = tk.Button(self.top, text="Apply", command=self.apply_code)
        self.apply_code_button.grid(row=1, column=2, sticky=tk.NSEW, padx=5, pady=5)

        for i in range(16):
            self.costume_list.insert(tk.END, self.prm_bas.ModelCodes[i])
        
        self.costume_list.selection_set(0)
        self.costume_list.activate(0)
        self.costume_list.event_generate("<<ListboxSelect>>")        

    def costume_list_select(self, event):
        if self.costume_list.curselection():
            index = self.costume_list.curselection()[0]
            self.costume_code_entry.delete(0, tk.END)
            self.costume_code_entry.insert(0, self.prm_bas.ModelCodes[index])
    
    def apply_code(self):
        if self.costume_list.curselection():
            index = self.costume_list.curselection()[0]
            self.prm_bas.ModelCodes[index] = self.costume_code_entry.get()
            self.costume_list.delete(index)
            self.costume_list.insert(index, self.costume_code_entry.get())
            self.costume_list.selection_set(index)
            self.costume_list.activate(index)
            self.costume_list.event_generate("<<ListboxSelect>>")

    def HurtSpheres(self):
        pass

class CharaViewerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Model Viewer Editor")
        self.master.geometry("800x600")
        self.pack(fill=tk.BOTH, expand=True)

        self.viewers = []
        self.copied_viewer = None
        self.old_path = None
        

class CharaCodeGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Character Code Editor")
        self.master.geometry("300x400")
        self.pack(fill=tk.BOTH, expand=True)

        self.viewers = []
        self.copied_viewer = None
        self.old_path = None

        Grid.rowconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 1, weight=4)
        Grid.rowconfigure(self, 2, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

        self.upper_frame = tk.Frame(self)
        self.mid_frame = tk.Frame(self)
        self.lower_frame = tk.Frame(self)

        self.upper_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.mid_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.lower_frame.grid(row=2, column=0, sticky=tk.NSEW)

        self.open_button = tk.Button(self.upper_frame, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.save_button = tk.Button(self.upper_frame, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.listbox = tk.Listbox(self.mid_frame, selectmode=tk.EXTENDED, exportselection=0)
        #self.listbox.configure(exportselection=False, selectmode=tk.EXTENDED)
        self.listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_select)

        self.scrollbar = tk.Scrollbar(self.mid_frame)
        self.scrollbar.pack(fill=tk.BOTH, expand=False, side=tk.LEFT)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        Grid.rowconfigure(self.lower_frame, 0, weight=1)
        Grid.rowconfigure(self.lower_frame, 1, weight=1)
        Grid.rowconfigure(self.lower_frame, 2, weight=1)
        Grid.rowconfigure(self.lower_frame, 3, weight=1)
        Grid.columnconfigure(self.lower_frame, 0, weight=1)
        Grid.columnconfigure(self.lower_frame, 1, weight=1)

        self.add_entry_button = tk.Button(self.lower_frame, text="Add Entry", command=self.add_entry)
        self.add_entry_button.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.delete_entry_button = tk.Button(self.lower_frame, text="Delete Entry", command=self.delete_entry)
        self.delete_entry_button.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.characode_label = tk.Label(self.lower_frame, text="Character Code")
        self.characode_label.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.characode_entry = tk.Entry(self.lower_frame)
        self.characode_entry.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.charaindex_label = tk.Label(self.lower_frame, text="Character Index")
        self.charaindex_label.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.charaindex_entry = tk.Entry(self.lower_frame)
        self.charaindex_entry.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.apply_button = tk.Button(self.lower_frame, text="Apply", command=self.apply)
        self.apply_button.grid(row=3, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

    
    def open_file(self):
        file = filedialog.askopenfilename(
            filetypes=[("CharaCode.bin", "*.xfbin")]
        )
        if file:
            self.characodes = read_chara_code(file)
            self.old_path = file

            #clear the listbox
            self.listbox.delete(0, tk.END)

            for char in self.characodes:
                self.listbox.insert(tk.END, f"{char.code}")

            #select the first item in the listbox
            if len(self.characodes) > 0:
                self.listbox.selection_set(0)
                self.listbox.activate(0)
                self.listbox.event_generate("<<ListboxSelect>>")
    
    def listbox_select(self, event):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            char = self.characodes[index]

            self.characode_entry.delete(0, tk.END)
            self.charaindex_entry.delete(0, tk.END)

            self.characode_entry.insert(0, char.code)
            self.charaindex_entry.insert(0, char.index)
    
    def save_file(self):
        path = filedialog.asksaveasfilename(
            filetypes=[("CharaCode.bin", "*.xfbin")]
        )
        if path:
            write = write_chara_code(path, self.characodes)

            if write:
                tk.messagebox.showinfo("Success", "CharaCode.bin saved successfully!")
            else:
                tk.messagebox.showerror("Error", "Error saving CharaCode.bin!")

    def add_entry(self):
        self.listbox.insert(tk.END, f"dmy01")
        char = Character()
        char.code = "dmy01"
        char.index = len(self.characodes) + 1
        self.characodes.append(char)

        self.listbox.selection_set(tk.END)
        self.listbox.activate(tk.END)
        self.listbox.event_generate("<<ListboxSelect>>")

        #auto scroll to the bottom
        self.listbox.yview_moveto(1)
        

    def delete_entry(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            self.characodes.pop(index)

    def apply(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            char = self.characodes[index]

            char.code = self.characode_entry.get()
            char.index = int(self.charaindex_entry.get())

            self.listbox.delete(index)
            self.listbox.insert(index, char.code)

            self.listbox.selection_set(index)
            self.listbox.activate(index)
            self.listbox.event_generate("<<ListboxSelect>>")


if __name__ == '__main__':
    app = App()
    app.mainloop()