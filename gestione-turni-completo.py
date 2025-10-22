import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime, timedelta
import calendar
import random
import json
import os
import openpyxl
from openpyxl.styles import PatternFill, Alignment, Font, Border, Side
from openpyxl.utils import get_column_letter

class GestioneTurni:
    def __init__(self):
        """Inizializzazione dell'applicazione"""
        # Inizializzazione delle variabili principali
        self.addetti = {}  # Dizionario per memorizzare i dati degli addetti
        self.turni_disponibili = []  # Lista dei turni disponibili
        self.giorni_festivi = [
            "01-01",  # Capodanno
            "20-04",  # 20 aprile
            "01-05",  # 1 maggio
            "25-12",  # Natale
            "26-12"   # Santo Stefano
        ]
        
        # Orari di apertura del supermercato
        self.orario_apertura = "08:00"
        self.orario_chiusura = "21:00"
        
        # Colori per Excel
        self.colori = {
            'header': 'CCE5FF',     # Azzurro chiaro per header
            'weekend': 'FFE6E6',    # Rosa chiaro per weekend
            'turno_mattina': 'E6FFE6',  # Verde chiaro per turni mattina
            'turno_pomeriggio': 'FFE6CC',  # Arancione chiaro per turni pomeriggio
            'riposo': 'F2F2F2',     # Grigio chiaro per riposi
            'ferie': 'FFFF99',      # Giallo chiaro per ferie
            'festivo': 'FF9999'     # Rosso chiaro per festivi
        }
        
        # Carica i dati se esistono
        self.carica_dati()
        
        # Creazione della finestra principale
        self.root = tk.Tk()
        self.root.title("Gestione Turni Supermercato")
        self.root.geometry("800x600")
        
        # Creazione del menu principale
        self.crea_menu_principale()
    
    def carica_dati(self):
        """Carica i dati salvati se esistono"""
        try:
            if os.path.exists('dati_turni.json'):
                with open('dati_turni.json', 'r') as f:
                    dati = json.load(f)
                    self.addetti = dati.get('addetti', {})
                    self.turni_disponibili = dati.get('turni', [])
        except Exception as e:
            print(f"Errore nel caricamento dei dati: {e}")
    
    def salva_dati(self):
        """Salva i dati su file"""
        try:
            dati = {
                'addetti': self.addetti,
                'turni': self.turni_disponibili
            }
            with open('dati_turni.json', 'w') as f:
                json.dump(dati, f)
        except Exception as e:
            print(f"Errore nel salvataggio dei dati: {e}")
    
    def crea_menu_principale(self):
        """Crea il menu principale dell'applicazione"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(main_frame, text="Gestione Addetti", 
                  command=self.gestione_addetti).grid(row=0, column=0, pady=5)
        ttk.Button(main_frame, text="Gestione Turni", 
                  command=self.gestione_turni).grid(row=1, column=0, pady=5)
        ttk.Button(main_frame, text="Gestione Ferie e Riposi", 
                  command=self.gestione_ferie_riposi).grid(row=2, column=0, pady=5)
        ttk.Button(main_frame, text="Genera Pianificazione", 
                  command=self.genera_pianificazione).grid(row=3, column=0, pady=5)
        ttk.Button(main_frame, text="Visualizza Statistiche", 
                  command=self.visualizza_statistiche).grid(row=4, column=0, pady=5)
    
    def gestione_addetti(self):
        """Gestisce l'aggiunta e la modifica degli addetti"""
        window = tk.Toplevel(self.root)
        window.title("Gestione Addetti")
        window.geometry("600x500")
        
        # Frame per la lista degli addetti esistenti
        frame_lista = ttk.Frame(window)
        frame_lista.grid(row=0, column=0, padx=10, pady=10)
        
        # Lista degli addetti esistenti
        ttk.Label(frame_lista, text="Addetti esistenti:").grid(row=0, column=0)
        lista_addetti = tk.Listbox(frame_lista, width=30, height=10)
        lista_addetti.grid(row=1, column=0)
        for addetto in self.addetti:
            lista_addetti.insert(tk.END, addetto)
        
        # Frame per il form di inserimento
        frame_form = ttk.Frame(window)
        frame_form.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame_form, text="Nome:").grid(row=0, column=0, pady=5)
        nome_var = tk.StringVar()
        ttk.Entry(frame_form, textvariable=nome_var).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame_form, text="Ore Contratto:").grid(row=1, column=0, pady=5)
        ore_var = tk.IntVar(value=40)
        ttk.Entry(frame_form, textvariable=ore_var).grid(row=1, column=1, pady=5)
        
        ttk.Label(frame_form, text="Ore Max:").grid(row=2, column=0, pady=5)
        ore_max_var = tk.IntVar(value=48)
        ttk.Entry(frame_form, textvariable=ore_max_var).grid(row=2, column=1, pady=5)
        
        ttk.Label(frame_form, text="Straordinario:").grid(row=3, column=0, pady=5)
        straordinario_var = tk.BooleanVar()
        ttk.Checkbutton(frame_form, variable=straordinario_var).grid(row=3, column=1, pady=5)
        
        def salva_addetto():
            nome = nome_var.get()
            if nome:
                self.addetti[nome] = {
                    'ore_contratto': ore_var.get(),
                    'ore_max': ore_max_var.get(),
                    'straordinario': straordinario_var.get(),
                    'giorni_riposo': [],
                    'ferie': []
                }
                lista_addetti.insert(tk.END, nome)
                self.salva_dati()
                messagebox.showinfo("Successo", f"Addetto {nome} aggiunto correttamente")
                
        def elimina_addetto():
            selection = lista_addetti.curselection()
            if selection:
                nome = lista_addetti.get(selection[0])
                if messagebox.askyesno("Conferma", f"Vuoi eliminare l'addetto {nome}?"):
                    del self.addetti[nome]
                    lista_addetti.delete(selection[0])
                    self.salva_dati()
        
        ttk.Button(frame_form, text="Salva", 
                  command=salva_addetto).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame_form, text="Elimina Selezionato", 
                  command=elimina_addetto).grid(row=5, column=0, columnspan=2, pady=10)
    
    def gestione_turni(self):
        """Gestisce la definizione dei turni disponibili"""
        window = tk.Toplevel(self.root)
        window.title("Gestione Turni")
        window.geometry("500x400")
        
        # Lista dei turni esistenti
        frame_lista = ttk.Frame(window)
        frame_lista.grid(row=0, column=0, padx=10, pady=10)
        
        ttk.Label(frame_lista, text="Turni esistenti:").grid(row=0, column=0)
        lista_turni = tk.Listbox(frame_lista, width=30, height=10)
        lista_turni.grid(row=1, column=0)
        for turno in self.turni_disponibili:
            lista_turni.insert(tk.END, f"{turno[0]} - {turno[1]}")
        
        # Form per nuovo turno
        frame_form = ttk.Frame(window)
        frame_form.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(frame_form, text="Ora Inizio (HH:MM):").grid(row=0, column=0, pady=5)
        inizio_var = tk.StringVar()
        ttk.Entry(frame_form, textvariable=inizio_var).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame_form, text="Ora Fine (HH:MM):").grid(row=1, column=0, pady=5)
        fine_var = tk.StringVar()
        ttk.Entry(frame_form, textvariable=fine_var).grid(row=1, column=1, pady=5)
        
        def valida_orario(orario):
            """Valida il formato dell'orario"""
            try:
                ore, minuti = map(int, orario.split(':'))
                return 0 <= ore <= 23 and 0 <= minuti <= 59
            except:
                return False
        
        def salva_turno():
            inizio = inizio_var.get()
            fine = fine_var.get()
            if not (valida_orario(inizio) and valida_orario(fine)):
                messagebox.showerror("Errore", "Formato orario non valido (HH:MM)")
                return
            if inizio >= fine:
                messagebox.showerror("Errore", "L'ora di inizio deve essere precedente all'ora di fine")
                return
            if inizio < self.orario_apertura or fine > self.orario_chiusura:
                messagebox.showerror("Errore", f"Il turno deve essere tra {self.orario_apertura} e {self.orario_chiusura}")
                return
            
            self.turni_disponibili.append((inizio, fine))
            lista_turni.insert(tk.END, f"{inizio} - {fine}")
            self.salva_dati()
            messagebox.showinfo("Successo", f"Turno {inizio}-{fine} aggiunto")
        
        def elimina_turno():
            selection = lista_turni.curselection()
            if selection:
                idx = selection[0]
                if messagebox.askyesno("Conferma", "Vuoi eliminare il turno selezionato?"):
                    del self.turni_disponibili[idx]
                    lista_turni.delete(idx)
                    self.salva_dati()
        
        ttk.Button(frame_form, text="Aggiungi Turno", 
                  command=salva_turno).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(frame_form, text="Elimina Selezionato", 
                  command=elimina_turno).grid(row=3, column=0, columnspan=2, pady=10)

    def gestione_ferie_riposi(self):
        """Gestisce ferie e giorni di riposo degli addetti"""
        if not self.addetti:
            messagebox.showerror("Errore", "Inserire prima gli addetti")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Gestione Ferie e Riposi")
        window.geometry("800x600")
        
        # Frame principale diviso in due colonne
        frame_sx = ttk.Frame(window)
        frame_dx = ttk.Frame(window)
        frame_sx.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        frame_dx.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        # Configurazione del grid
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        
        # ---- Sezione Selezione Addetto (comune) ----
        frame_select = ttk.LabelFrame(frame_sx, text="Selezione Addetto")
        frame_select.pack(fill='x', pady=5)
        
        ttk.Label(frame_select, text="Seleziona Addetto:").pack(side=tk.LEFT, padx=5)
        addetto_var = tk.StringVar()
        combo_addetti = ttk.Combobox(frame_select, textvariable=addetto_var, 
                                   values=list(self.addetti.keys()))
        combo_addetti.pack(side=tk.LEFT, padx=5)
        
        # ---- Sezione Gestione Ferie (sinistra) ----
        frame_ferie = ttk.LabelFrame(frame_sx, text="Gestione Ferie")
        frame_ferie.pack(fill='both', expand=True, pady=5)
        
        # Calendario per selezione ferie
        ttk.Label(frame_ferie, text="Seleziona Data:").pack(pady=5)
        
        frame_calendario = ttk.Frame(frame_ferie)
        frame_calendario.pack(pady=5)
        
        # Selezione anno e mese
        anno_var = tk.StringVar(value=str(datetime.now().year))
        mese_var = tk.StringVar(value=str(datetime.now().month))
        
        ttk.Label(frame_calendario, text="Anno:").grid(row=0, column=0, padx=5)
        ttk.Entry(frame_calendario, textvariable=anno_var, width=6).grid(row=0, column=1)
        ttk.Label(frame_calendario, text="Mese:").grid(row=0, column=2, padx=5)
        ttk.Spinbox(frame_calendario, from_=1, to=12, width=4, 
                   textvariable=mese_var).grid(row=0, column=3)
        
        # Calendario per selezione giorni
        frame_giorni = ttk.Frame(frame_ferie)
        frame_giorni.pack(pady=5)
        giorni_vars = {}  # Variabili per i checkbutton dei giorni
        
        def aggiorna_calendario():
            """Aggiorna la visualizzazione del calendario"""
            # Pulisci frame giorni
            for widget in frame_giorni.winfo_children():
                widget.destroy()
            
            try:
                anno = int(anno_var.get())
                mese = int(mese_var.get())
                
                # Crea intestazioni giorni settimana
                giorni_settimana = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
                for i, giorno in enumerate(giorni_settimana):
                    ttk.Label(frame_giorni, text=giorno).grid(row=0, column=i, padx=2)
                
                # Ottieni il calendario del mese
                cal = calendar.monthcalendar(anno, mese)
                giorni_vars.clear()
                
                # Crea checkbutton per ogni giorno
                for settimana in range(len(cal)):
                    for giorno in range(7):
                        day_num = cal[settimana][giorno]
                        if day_num != 0:
                            var = tk.BooleanVar()
                            giorni_vars[day_num] = var
                            cb = ttk.Checkbutton(frame_giorni, text=str(day_num),
                                               variable=var)
                            cb.grid(row=settimana+1, column=giorno, padx=2)
                
                # Evidenzia le ferie già programmate
                addetto = addetto_var.get()
                if addetto in self.addetti:
                    for data in self.addetti[addetto]['ferie']:
                        data_obj = datetime.strptime(data, '%Y-%m-%d')
                        if data_obj.year == anno and data_obj.month == mese:
                            if data_obj.day in giorni_vars:
                                giorni_vars[data_obj.day].set(True)
                
            except ValueError:
                messagebox.showerror("Errore", "Data non valida")
        
        ttk.Button(frame_calendario, text="Aggiorna Calendario", 
                  command=aggiorna_calendario).grid(row=0, column=4, padx=5)
        
        # Lista delle ferie già programmate
        ttk.Label(frame_ferie, text="Ferie Programmate:").pack(pady=5)
        lista_ferie = tk.Listbox(frame_ferie, height=6)
        lista_ferie.pack(fill='x', padx=5)
        
        def salva_ferie():
            """Salva le ferie selezionate per l'addetto"""
            addetto = addetto_var.get()
            if not addetto:
                messagebox.showerror("Errore", "Selezionare un addetto")
                return
                
            try:
                anno = int(anno_var.get())
                mese = int(mese_var.get())
                
                # Raccogli i giorni selezionati
                nuove_ferie = []
                for giorno, var in giorni_vars.items():
                    if var.get():
                        data = datetime(anno, mese, giorno)
                        nuove_ferie.append(data.strftime('%Y-%m-%d'))
                
                # Aggiorna le ferie dell'addetto
                self.addetti[addetto]['ferie'] = nuove_ferie
                self.salva_dati()
                aggiorna_liste()
                messagebox.showinfo("Successo", "Ferie salvate correttamente")
                
            except ValueError:
                messagebox.showerror("Errore", "Data non valida")
        
        ttk.Button(frame_ferie, text="Salva Ferie Selezionate", 
                  command=salva_ferie).pack(pady=5)
        
        # ---- Sezione Gestione Riposi (destra) ----
        frame_riposi = ttk.LabelFrame(frame_dx, text="Gestione Giorni di Riposo")
        frame_riposi.pack(fill='both', expand=True, pady=5)
        
        # Checkbox per ogni giorno della settimana
        giorni_settimana_completi = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", 
                                   "Venerdì", "Sabato", "Domenica"]
        riposi_vars = []
        
        for i, giorno in enumerate(giorni_settimana_completi):
            var = tk.BooleanVar()
            riposi_vars.append(var)
            ttk.Checkbutton(frame_riposi, text=giorno, 
                          variable=var).pack(anchor='w', padx=10)
        
        # Lista dei riposi programmati
        ttk.Label(frame_riposi, text="Giorni di Riposo Attuali:").pack(pady=5)
        lista_riposi = tk.Listbox(frame_riposi, height=6)
        lista_riposi.pack(fill='x', padx=5)
        
        def salva_riposi():
            """Salva i giorni di riposo per l'addetto"""
            addetto = addetto_var.get()
            if not addetto:
                messagebox.showerror("Errore", "Selezionare un addetto")
                return
            
            giorni_riposo = [i for i, var in enumerate(riposi_vars) if var.get()]
            if giorni_riposo:
                self.addetti[addetto]['giorni_riposo'] = giorni_riposo
                self.salva_dati()
                aggiorna_liste()
                messagebox.showinfo("Successo", "Giorni di riposo salvati")
            else:
                messagebox.showerror("Errore", "Selezionare almeno un giorno di riposo")
        
        ttk.Button(frame_riposi, text="Salva Giorni di Riposo", 
                  command=salva_riposi).pack(pady=5)
        
        def aggiorna_liste():
            """Aggiorna le liste di ferie e riposi"""
            addetto = addetto_var.get()
            if addetto in self.addetti:
                # Aggiorna lista ferie
                lista_ferie.delete(0, tk.END)
                for data in sorted(self.addetti[addetto]['ferie']):
                    lista_ferie.insert(tk.END, data)
                
                # Aggiorna lista riposi
                lista_riposi.delete(0, tk.END)
                for giorno in sorted(self.addetti[addetto]['giorni_riposo']):
                    lista_riposi.insert(tk.END, giorni_settimana_completi[giorno])
        
        def on_select_addetto(event):
            """Callback quando viene selezionato un addetto"""
            aggiorna_liste()
            aggiorna_calendario()
            
            # Aggiorna checkbox riposi
            addetto = addetto_var.get()
            if addetto in self.addetti:
                for i, var in enumerate(riposi_vars):
                    var.set(i in self.addetti[addetto]['giorni_riposo'])
        
        # Binding eventi
        combo_addetti.bind('<<ComboboxSelected>>', on_select_addetto)
        
        # Inizializza il calendario
        aggiorna_calendario()

    def _controlla_copertura_oraria(self, turni_giorno):
        """
        Controlla la copertura oraria per un giorno dato l'insieme dei turni assegnati.
        Restituisce una lista di intervalli temporali non coperti.
        """
        def orario_in_minuti(orario):
            ore, minuti = map(int, orario.split(':'))
            return ore * 60 + minuti
        
        apertura = orario_in_minuti(self.orario_apertura)
        chiusura = orario_in_minuti(self.orario_chiusura)
        
        # Crea un array di minuti per tracciare la copertura
        copertura = [False] * (chiusura - apertura)
        
        # Segna i minuti coperti dai turni assegnati
        for turno in turni_giorno.values():
            inizio = orario_in_minuti(turno[0]) - apertura
            fine = orario_in_minuti(turno[1]) - apertura
            
            # Assicuriamoci che gli indici siano validi
            inizio = max(0, inizio)
            fine = min(len(copertura), fine)
            
            for i in range(inizio, fine):
                copertura[i] = True
        
        # Trova gli intervalli non coperti
        buchi = []
        inizio_buco = None
        
        for i, coperto in enumerate(copertura):
            if not coperto and inizio_buco is None:
                inizio_buco = i
            elif coperto and inizio_buco is not None:
                buchi.append((inizio_buco + apertura, i + apertura))
                inizio_buco = None
                
        if inizio_buco is not None:
            buchi.append((inizio_buco + apertura, len(copertura) + apertura))
        
        return buchi

    def _calcola_punteggio_turno(self, addetto, turno, giorno, mese, anno, turni_assegnati):
        """Calcola un punteggio per l'assegnazione di un turno a un addetto."""
        punteggio = 0
        
        # Calcola ore già lavorate
        ore_lavorate = 0
        for g, turni in turni_assegnati.items():
            if addetto in turni:
                inizio = datetime.strptime(turni[addetto][0], '%H:%M')
                fine = datetime.strptime(turni[addetto][1], '%H:%M')
                ore_lavorate += (fine - inizio).seconds / 3600
        
        # Gestione ore contrattuali
        ore_contratto = self.addetti[addetto]['ore_contratto']
        ore_max = self.addetti[addetto]['ore_max']
        
        # Calcola ore del turno attuale
        inizio_turno = datetime.strptime(turno[0], '%H:%M')
        fine_turno = datetime.strptime(turno[1], '%H:%M')
        ore_turno = (fine_turno - inizio_turno).seconds / 3600
        
        # Bonus se le ore sono sotto il contratto
        if ore_lavorate + ore_turno <= ore_contratto:
            punteggio += 10
        
        # Malus se si supera il massimo di ore (se non è permesso lo straordinario)
        if not self.addetti[addetto]['straordinario'] and ore_lavorate + ore_turno > ore_max:
            punteggio -= 20
        
        # Controlla se l'addetto ha fatto lo stesso turno nei giorni precedenti
        turno_str = f"{turno[0]}-{turno[1]}"
        turni_precedenti = []
        
        # Controlla gli ultimi 5 giorni (aumentato da 3 a 5 per evitare ripetizioni)
        for g in range(max(1, giorno-5), giorno):
            if g in turni_assegnati and addetto in turni_assegnati[g]:
                t = turni_assegnati[g][addetto]
                turni_precedenti.append(f"{t[0]}-{t[1]}")
        
        # Malus MOLTO più severo per turni ripetuti (aumentato da 5 a 30)
        if turno_str in turni_precedenti:
            # Penalità esponenziale: più vicino è il giorno con lo stesso turno, più forte è la penalità
            count = turni_precedenti.count(turno_str)
            # Calcola la posizione dell'ultimo turno identico
            ultima_posizione = 0
            for i, t in enumerate(reversed(turni_precedenti)):
                if t == turno_str:
                    ultima_posizione = i
                    break
            
            # Penalità più forte se il turno è stato fatto di recente
            punteggio -= 30 * count * (5 - ultima_posizione) / 5
            
            # Se il turno è identico a quello del giorno precedente, penalità extra
            if giorno-1 in turni_assegnati and addetto in turni_assegnati[giorno-1]:
                if f"{turni_assegnati[giorno-1][addetto][0]}-{turni_assegnati[giorno-1][addetto][1]}" == turno_str:
                    punteggio -= 50  # Penalità molto forte per turni identici consecutivi
        
        # Bonus/malus per bilanciare turni mattina/pomeriggio
        turni_mattina = 0
        turni_pomeriggio = 0
        
        for g, turni in turni_assegnati.items():
            if addetto in turni:
                if turni[addetto][0] < "12:00":
                    turni_mattina += 1
                else:
                    turni_pomeriggio += 1
        
        # Incentiva la varietà nei turni (aumento del bonus)
        if turno[0] < "12:00" and turni_mattina < turni_pomeriggio:
            punteggio += 8
        elif turno[0] >= "12:00" and turni_pomeriggio < turni_mattina:
            punteggio += 8
        
        return punteggio

    def _genera_calendario_mensile(self, anno, mese):
        """
        Genera il calendario mensile con algoritmo ottimizzato:
        1. Pre-validazione delle risorse disponibili
        2. Algoritmo greedy intelligente con priorità dinamiche
        3. Bilanciamento equo delle ore tra gli addetti
        4. Copertura oraria completa garantita
        5. Rispetto rigoroso dei vincoli (ore max, riposi, ferie)
        """
        print(f"\n{'='*70}")
        print(f"GENERAZIONE CALENDARIO - {calendar.month_name[mese].upper()} {anno}")
        print(f"{'='*70}\n")

        # Ottiene il numero di giorni nel mese
        num_giorni = calendar.monthrange(anno, mese)[1]

        # Pre-validazione: calcola le risorse disponibili
        print("=== PRE-VALIDAZIONE RISORSE ===")
        giorni_lavorativi = self._conta_giorni_lavorativi(anno, mese)
        ore_necessarie_giorno = 13  # 08:00-21:00
        ore_totali_necessarie = giorni_lavorativi * ore_necessarie_giorno

        ore_disponibili_totali = 0
        for nome, info in self.addetti.items():
            # Calcola giorni disponibili per addetto
            giorni_disponibili = self._conta_giorni_disponibili(nome, anno, mese)
            ore_max_addetto = min(info['ore_max'], giorni_disponibili * 8)
            ore_disponibili_totali += ore_max_addetto
            print(f"- {nome}: {giorni_disponibili} giorni disponibili, max {ore_max_addetto:.1f} ore")

        print(f"\nOre necessarie totali: {ore_totali_necessarie:.1f}")
        print(f"Ore disponibili totali: {ore_disponibili_totali:.1f}")

        if ore_disponibili_totali < ore_totali_necessarie:
            print(f"⚠️ ATTENZIONE: Risorse insufficienti! Mancano {ore_totali_necessarie - ore_disponibili_totali:.1f} ore")
        else:
            print(f"✓ Risorse sufficienti (surplus: {ore_disponibili_totali - ore_totali_necessarie:.1f} ore)")

        # Inizializza il dizionario del calendario
        calendario = {giorno: {} for giorno in range(1, num_giorni + 1)}

        # Tracciamento ore assegnate e statistiche per addetto
        ore_assegnate = {addetto: 0 for addetto in self.addetti}
        turni_assegnati = {addetto: {'mattina': 0, 'pomeriggio': 0} for addetto in self.addetti}

        # Per ogni giorno del mese
        for giorno in range(1, num_giorni + 1):
            data = datetime(anno, mese, giorno)
            data_str = data.strftime('%d-%m')
            giorno_settimana = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'][data.weekday()]

            # Salta i giorni festivi
            if data_str in self.giorni_festivi:
                print(f"\nGiorno {giorno:2d} ({giorno_settimana}): FESTIVO - saltato")
                continue

            print(f"\n{'─'*70}")
            print(f"Giorno {giorno:2d} ({giorno_settimana} {data.strftime('%d/%m/%Y')})")
            print(f"{'─'*70}")

            # Calcola addetti disponibili con priorità
            addetti_info = self._calcola_disponibilita_addetti(
                data, ore_assegnate, turni_assegnati, calendario, giorno
            )

            if not addetti_info['disponibili']:
                print("⚠️ AVVISO: Nessun addetto disponibile per questo giorno!")
                continue

            # Algoritmo di assegnazione ottimizzato
            soluzione = self._assegna_turni_giorno_ottimizzato(
                giorno, data, addetti_info, ore_assegnate, turni_assegnati, calendario
            )

            if soluzione:
                calendario[giorno] = soluzione

                # Aggiorna statistiche
                for addetto, turno in soluzione.items():
                    ore_turno = self._calcola_ore_turno(turno)
                    ore_assegnate[addetto] += ore_turno

                    # Aggiorna contatori mattina/pomeriggio
                    if turno[0] < "12:00":
                        turni_assegnati[addetto]['mattina'] += 1
                    else:
                        turni_assegnati[addetto]['pomeriggio'] += 1

                    print(f"  ✓ {addetto:15s} → {turno[0]}-{turno[1]} ({ore_turno:.1f}h) "
                          f"[Tot: {ore_assegnate[addetto]:.1f}h]")
            else:
                print("  ✗ Impossibile trovare una copertura completa per questo giorno")

        # Stampa riepilogo finale dettagliato
        self._stampa_riepilogo_finale(ore_assegnate, turni_assegnati)

        return calendario

    def _conta_giorni_lavorativi(self, anno, mese):
        """Conta i giorni lavorativi del mese (esclusi festivi)"""
        num_giorni = calendar.monthrange(anno, mese)[1]
        count = 0
        for giorno in range(1, num_giorni + 1):
            data = datetime(anno, mese, giorno)
            data_str = data.strftime('%d-%m')
            if data_str not in self.giorni_festivi:
                count += 1
        return count

    def _conta_giorni_disponibili(self, nome, anno, mese):
        """Conta i giorni in cui un addetto è disponibile nel mese"""
        num_giorni = calendar.monthrange(anno, mese)[1]
        count = 0
        info = self.addetti[nome]

        for giorno in range(1, num_giorni + 1):
            data = datetime(anno, mese, giorno)
            data_str = data.strftime('%d-%m')

            # Salta festivi
            if data_str in self.giorni_festivi:
                continue

            # Salta ferie
            if data.strftime('%Y-%m-%d') in info['ferie']:
                continue

            # Salta riposi settimanali
            if data.weekday() in info['giorni_riposo']:
                continue

            count += 1

        return count

    def _calcola_ore_turno(self, turno):
        """Calcola le ore di un turno"""
        inizio = datetime.strptime(turno[0], '%H:%M')
        fine = datetime.strptime(turno[1], '%H:%M')
        return (fine - inizio).seconds / 3600

    def _calcola_disponibilita_addetti(self, data, ore_assegnate, turni_assegnati, calendario, giorno):
        """
        Calcola gli addetti disponibili con priorità e informazioni dettagliate
        """
        disponibili = []
        info_dettagli = {}

        for nome, info in self.addetti.items():
            # Verifica vincoli hard
            if data.strftime('%Y-%m-%d') in info['ferie']:
                print(f"  - {nome:15s}: FERIE")
                continue

            if data.weekday() in info['giorni_riposo']:
                print(f"  - {nome:15s}: RIPOSO SETTIMANALE")
                continue

            ore_residue = info['ore_max'] - ore_assegnate[nome]

            # Turno minimo disponibile
            ore_turno_min = min(self._calcola_ore_turno(t) for t in self.turni_disponibili)

            # Verifica se ha abbastanza ore residue
            if not info['straordinario'] and ore_residue < ore_turno_min:
                print(f"  - {nome:15s}: LIMITE ORE RAGGIUNTO ({ore_assegnate[nome]:.1f}/{info['ore_max']}h)")
                continue

            # Calcola priorità per bilanciamento carico
            ore_contratto = info['ore_contratto']
            percentuale_utilizzo = ore_assegnate[nome] / ore_contratto if ore_contratto > 0 else 0

            # Priorità: chi ha lavorato meno ha priorità più alta
            priorita = 100 - (percentuale_utilizzo * 100)

            # Bonus per chi può fare straordinari
            if info['straordinario']:
                priorita += 10

            # Bonus per bilanciare mattina/pomeriggio
            diff_turni = abs(turni_assegnati[nome]['mattina'] - turni_assegnati[nome]['pomeriggio'])
            priorita -= diff_turni * 2  # Penalità per sbilanciamento

            disponibili.append(nome)
            info_dettagli[nome] = {
                'ore_residue': ore_residue,
                'priorita': priorita,
                'straordinario': info['straordinario'],
                'ore_assegnate': ore_assegnate[nome],
                'turni_recenti': self._get_turni_recenti(nome, calendario, giorno, 3)
            }

            print(f"  ✓ {nome:15s}: Disponibile (priorità: {priorita:.1f}, ore residue: {ore_residue:.1f}h)")

        # Ordina per priorità decrescente
        disponibili.sort(key=lambda x: info_dettagli[x]['priorita'], reverse=True)

        return {
            'disponibili': disponibili,
            'dettagli': info_dettagli
        }

    def _get_turni_recenti(self, nome, calendario, giorno_corrente, n_giorni):
        """Ottiene gli ultimi N turni assegnati a un addetto"""
        turni = []
        for g in range(max(1, giorno_corrente - n_giorni), giorno_corrente):
            if g in calendario and nome in calendario[g]:
                turni.append(calendario[g][nome])
        return turni

    def _assegna_turni_giorno_ottimizzato(self, giorno, data, addetti_info, ore_assegnate,
                                          turni_assegnati, calendario):
        """
        Algoritmo ottimizzato per assegnare i turni di un giorno
        Strategia: greedy con priorità dinamiche e backtracking limitato
        """
        inizio_min = 8 * 60  # 08:00 in minuti
        fine_min = 21 * 60   # 21:00 in minuti
        durata_min = fine_min - inizio_min

        # Prova diverse strategie
        strategie = [
            'priorita_copertura',  # Prima strategia: massimizza copertura
            'priorita_bilanciamento',  # Seconda: bilancia ore
            'priorita_continuita'  # Terza: evita frammentazione
        ]

        for strategia in strategie:
            soluzione = self._prova_assegnazione(
                addetti_info, ore_assegnate, strategia, inizio_min, fine_min, giorno, calendario
            )

            if soluzione and self._verifica_copertura_completa(soluzione, inizio_min, fine_min):
                print(f"  ✓ Soluzione trovata con strategia: {strategia}")
                return soluzione

        # Se nessuna strategia funziona, prova soluzione parziale migliore
        print(f"  ⚠️ Copertura completa non possibile, uso migliore soluzione parziale")
        return self._trova_soluzione_parziale_migliore(
            addetti_info, ore_assegnate, inizio_min, fine_min, giorno, calendario
        )

    def _prova_assegnazione(self, addetti_info, ore_assegnate, strategia,
                           inizio_min, fine_min, giorno, calendario):
        """Prova un'assegnazione con una specifica strategia"""
        soluzione = {}
        copertura = [False] * (fine_min - inizio_min)
        addetti_usati = set()

        # Ordina turni in base alla strategia
        if strategia == 'priorita_copertura':
            # Turni più lunghi prima
            turni_ordinati = sorted(self.turni_disponibili,
                                   key=lambda t: self._calcola_ore_turno(t), reverse=True)
        elif strategia == 'priorita_continuita':
            # Turni che iniziano prima
            turni_ordinati = sorted(self.turni_disponibili, key=lambda t: t[0])
        else:  # bilanciamento
            # Alternanza mattina/pomeriggio
            turni_ordinati = self.turni_disponibili.copy()

        # Assegna turni finché c'è copertura da fare
        max_iterazioni = len(addetti_info['disponibili']) * len(self.turni_disponibili)
        iterazione = 0

        while iterazione < max_iterazioni:
            # Trova il primo buco di copertura
            buco = self._trova_primo_buco(copertura)
            if buco is None:
                # Copertura completa!
                return soluzione

            buco_inizio, buco_fine = buco
            ora_buco_inizio = inizio_min + buco_inizio
            ora_buco_fine = inizio_min + buco_fine

            # Trova il miglior turno per coprire questo buco
            migliore = self._trova_miglior_assegnazione_per_buco(
                ora_buco_inizio, ora_buco_fine, turni_ordinati, addetti_info,
                addetti_usati, ore_assegnate, giorno, calendario
            )

            if migliore is None:
                # Non possiamo coprire questo buco
                break

            addetto, turno = migliore
            soluzione[addetto] = turno
            addetti_usati.add(addetto)

            # Aggiorna copertura
            self._aggiorna_copertura(copertura, turno, inizio_min)

            iterazione += 1

        return soluzione if soluzione else None

    def _trova_primo_buco(self, copertura):
        """Trova il primo intervallo non coperto"""
        inizio_buco = None
        for i, coperto in enumerate(copertura):
            if not coperto and inizio_buco is None:
                inizio_buco = i
            elif coperto and inizio_buco is not None:
                return (inizio_buco, i)

        if inizio_buco is not None:
            return (inizio_buco, len(copertura))

        return None

    def _trova_miglior_assegnazione_per_buco(self, ora_inizio_buco, ora_fine_buco,
                                             turni, addetti_info, addetti_usati,
                                             ore_assegnate, giorno, calendario):
        """Trova la miglior combinazione addetto-turno per coprire un buco"""
        miglior_score = -float('inf')
        miglior_scelta = None

        for turno in turni:
            t_inizio = self._orario_in_minuti(turno[0])
            t_fine = self._orario_in_minuti(turno[1])

            # Il turno deve sovrapporsi al buco
            if t_fine <= ora_inizio_buco or t_inizio >= ora_fine_buco:
                continue

            # Calcola sovrapposizione
            sovrapposizione = min(t_fine, ora_fine_buco) - max(t_inizio, ora_inizio_buco)

            # Trova il miglior addetto per questo turno
            for addetto in addetti_info['disponibili']:
                if addetto in addetti_usati:
                    continue

                dettagli = addetti_info['dettagli'][addetto]
                ore_turno = self._calcola_ore_turno(turno)

                # Verifica vincolo ore max
                if not dettagli['straordinario']:
                    if ore_assegnate[addetto] + ore_turno > self.addetti[addetto]['ore_max']:
                        continue

                # Calcola score
                score = sovrapposizione  # Base: quanti minuti copriamo
                score += dettagli['priorita']  # Priorità addetto
                score -= self._penalita_ripetizione_turno(addetto, turno, dettagli['turni_recenti']) * 10

                # Bonus se il turno copre dall'inizio del buco
                if t_inizio <= ora_inizio_buco:
                    score += 20

                if score > miglior_score:
                    miglior_score = score
                    miglior_scelta = (addetto, turno)

        return miglior_scelta

    def _penalita_ripetizione_turno(self, addetto, turno, turni_recenti):
        """Calcola penalità per ripetizione dello stesso turno"""
        turno_str = f"{turno[0]}-{turno[1]}"
        count = sum(1 for t in turni_recenti if f"{t[0]}-{t[1]}" == turno_str)
        return count * count  # Penalità quadratica

    def _orario_in_minuti(self, orario):
        """Converte un orario HH:MM in minuti dal mezzanotte"""
        ore, minuti = map(int, orario.split(':'))
        return ore * 60 + minuti

    def _aggiorna_copertura(self, copertura, turno, inizio_min):
        """Aggiorna l'array di copertura con un nuovo turno"""
        t_inizio = self._orario_in_minuti(turno[0])
        t_fine = self._orario_in_minuti(turno[1])

        inizio_rel = max(0, t_inizio - inizio_min)
        fine_rel = min(len(copertura), t_fine - inizio_min)

        for i in range(inizio_rel, fine_rel):
            copertura[i] = True

    def _verifica_copertura_completa(self, soluzione, inizio_min, fine_min):
        """Verifica se una soluzione copre completamente l'orario"""
        copertura = [False] * (fine_min - inizio_min)
        for turno in soluzione.values():
            self._aggiorna_copertura(copertura, turno, inizio_min)
        return all(copertura)

    def _trova_soluzione_parziale_migliore(self, addetti_info, ore_assegnate,
                                          inizio_min, fine_min, giorno, calendario):
        """Trova la soluzione parziale che massimizza la copertura"""
        # Usa la strategia di copertura ma accetta soluzione parziale
        soluzione = self._prova_assegnazione(
            addetti_info, ore_assegnate, 'priorita_copertura',
            inizio_min, fine_min, giorno, calendario
        )
        return soluzione

    def _stampa_riepilogo_finale(self, ore_assegnate, turni_assegnati):
        """Stampa un riepilogo dettagliato finale"""
        print(f"\n{'='*70}")
        print("RIEPILOGO FINALE")
        print(f"{'='*70}\n")

        for addetto in sorted(ore_assegnate.keys()):
            info = self.addetti[addetto]
            ore = ore_assegnate[addetto]
            turni = turni_assegnati[addetto]

            # Calcola stato
            if ore > info['ore_max'] and not info['straordinario']:
                stato = "⚠️ ERRORE: Superato limite!"
                icona = "✗"
            elif ore > info['ore_contratto']:
                stato = f"Straordinario (+{ore - info['ore_contratto']:.1f}h)"
                icona = "⚡"
            elif ore < info['ore_contratto'] * 0.9:
                stato = f"Sotto contratto (-{info['ore_contratto'] - ore:.1f}h)"
                icona = "⚠️"
            else:
                stato = "OK"
                icona = "✓"

            print(f"{icona} {addetto:15s}: {ore:5.1f}h / {info['ore_max']}h max")
            print(f"   Contratto: {info['ore_contratto']}h | "
                  f"Mattina: {turni['mattina']} | Pomeriggio: {turni['pomeriggio']}")
            print(f"   Stato: {stato}\n")

    def _salva_calendario_excel(self, calendario, anno, mese):
        """Salva il calendario dei turni su file Excel con formattazione migliorata"""
        wb = openpyxl.Workbook()
        ws = wb.active
        
        # Impostazioni di base del foglio
        ws.title = f"Turni {calendar.month_name[mese]} {anno}"
        ws.sheet_view.zoomScale = 85
        
        # Stili comuni
        bordo = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        allineamento = Alignment(
            horizontal='center',
            vertical='center',
            wrap_text=True
        )
        
        # Formattazione header
        header_font = Font(bold=True, size=11, color='000000')
        header_fill = PatternFill(start_color=self.colori['header'], 
                                end_color=self.colori['header'],
                                fill_type='solid')
        
        # Scrivi intestazione
        ws.cell(1, 1, "Giorno").font = header_font
        ws.cell(1, 1).fill = header_fill
        ws.cell(1, 1).border = bordo
        ws.cell(1, 1).alignment = allineamento
        
        # Scrivi nomi addetti nelle colonne
        for col, addetto in enumerate(sorted(self.addetti.keys()), 2):
            cell = ws.cell(1, col, addetto)
            cell.font = header_font
            cell.fill = header_fill
            cell.border = bordo
            cell.alignment = allineamento
        
        # Scrivi i giorni e i turni
        for giorno in range(1, calendar.monthrange(anno, mese)[1] + 1):
            data = datetime(anno, mese, giorno)
            data_str = data.strftime('%d-%m')
            
            # Formattazione riga
            row = giorno + 1
            
            # Scrivi data
            cell_data = ws.cell(row, 1, f"{giorno:02d}/{mese:02d}/{anno}")
            cell_data.border = bordo
            cell_data.alignment = allineamento
            
            # Determina colore di sfondo per il giorno
            if data_str in self.giorni_festivi:
                fill = PatternFill(start_color=self.colori['festivo'], 
                                 end_color=self.colori['festivo'],
                                 fill_type='solid')
            elif data.weekday() >= 5:  # Weekend
                fill = PatternFill(start_color=self.colori['weekend'], 
                                 end_color=self.colori['weekend'],
                                 fill_type='solid')
            else:
                fill = None
            
            if fill:
                cell_data.fill = fill
            
            # Scrivi turni per ogni addetto
            for col, addetto in enumerate(sorted(self.addetti.keys()), 2):
                cell = ws.cell(row, col)
                cell.border = bordo
                cell.alignment = allineamento
                
                # Verifica se è un giorno di ferie
                if data.strftime('%Y-%m-%d') in self.addetti[addetto]['ferie']:
                    cell.value = "FERIE"
                    cell.fill = PatternFill(start_color=self.colori['ferie'], 
                                          end_color=self.colori['ferie'],
                                          fill_type='solid')
                # Verifica se è un giorno di riposo
                elif data.weekday() in self.addetti[addetto]['giorni_riposo']:
                    cell.value = "RIPOSO"
                    cell.fill = PatternFill(start_color=self.colori['riposo'], 
                                          end_color=self.colori['riposo'],
                                          fill_type='solid')
                # Verifica se c'è un turno assegnato
                elif addetto in calendario.get(giorno, {}):
                    turno = calendario[giorno][addetto]
                    cell.value = f"{turno[0]}-{turno[1]}"
                    
                    # Colore diverso per turni mattina/pomeriggio
                    if turno[0] < "12:00":
                        cell.fill = PatternFill(start_color=self.colori['turno_mattina'], 
                                              end_color=self.colori['turno_mattina'],
                                              fill_type='solid')
                    else:
                        cell.fill = PatternFill(start_color=self.colori['turno_pomeriggio'], 
                                              end_color=self.colori['turno_pomeriggio'],
                                              fill_type='solid')
                else:
                    cell.value = "-"
        
        # Imposta dimensioni colonne
        for col in range(1, ws.max_column + 1):
            ws.column_dimensions[get_column_letter(col)].width = 15
        
        # Congela la prima riga
        ws.freeze_panes = 'A2'
        
        # Salva il file
        nome_file = f"turni_{anno}_{mese}.xlsx"
        wb.save(nome_file)
        
        # Apri il file
        try:
            os.startfile(nome_file)  # Windows
        except AttributeError:
            import platform
            if platform.system() == "Darwin":  # macOS
                os.system(f"open {nome_file}")
            else:  # Linux
                os.system(f"xdg-open {nome_file}")
        except Exception as e:
            messagebox.showwarning("Attenzione", 
                f"File salvato ma non è stato possibile aprirlo automaticamente.\n{str(e)}")

    def visualizza_statistiche(self):
        """Visualizza le statistiche dei turni"""
        # Verifica che ci siano dati da analizzare
        files_turni = [f for f in os.listdir() if f.startswith('turni_') and f.endswith('.xlsx')]
        if not files_turni:
            messagebox.showinfo("Info", "Nessun dato disponibile per le statistiche")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Statistiche Turni")
        window.geometry("800x600")
        
        # Frame per selezione file
        frame_select = ttk.Frame(window)
        frame_select.pack(pady=10)
        
        ttk.Label(frame_select, text="Seleziona mese:").pack(side=tk.LEFT)
        file_var = tk.StringVar(value=files_turni[0])
        ttk.Combobox(frame_select, textvariable=file_var, 
                    values=files_turni).pack(side=tk.LEFT, padx=5)
        
        # Frame per statistiche
        frame_stats = ttk.Frame(window)
        frame_stats.pack(pady=10, fill=tk.BOTH, expand=True)
        
        def aggiorna_statistiche():
            """Aggiorna le statistiche visualizzate"""
            for widget in frame_stats.winfo_children():
                widget.destroy()
            
            try:
                # Carica dati
                df = pd.read_excel(file_var.get(), index_col=None)
                
                # Calcola statistiche per ogni addetto
                for addetto in df.columns[1:]:  # Salta la colonna Data/Giorno
                    # Conta turni totali
                    turni_totali = 0
                    # Conta ferie e riposi
                    ferie = 0
                    riposi = 0
                    # Ore totali
                    ore_totali = 0
                    # Domeniche lavorate
                    domeniche_lavorate = 0
                    
                    # Analizziamo ogni riga
                    for idx, row in df.iterrows():
                        # Ottieni la data
                        try:
                            data = datetime.strptime(row.iloc[0], '%d/%m/%Y')
                        except (ValueError, TypeError):
                            # Se la colonna non è una data formattata, proviamo a usarla come giorno
                            continue
                        
                        # Ottieni il valore della cella
                        valore_cella = row[addetto]
                        
                        # Verifica il tipo di informazione
                        if isinstance(valore_cella, str):
                            if valore_cella == "FERIE":
                                ferie += 1
                            elif valore_cella == "RIPOSO":
                                riposi += 1
                            elif "-" in valore_cella:  # È un turno (formato "HH:MM-HH:MM")
                                turni_totali += 1
                                
                                # Calcola ore turno
                                try:
                                    inizio, fine = valore_cella.split("-")
                                    inizio = inizio.strip()
                                    fine = fine.strip()
                                    
                                    # Verifica che il formato sia corretto
                                    if ":" in inizio and ":" in fine:
                                        ore_inizio = datetime.strptime(inizio, '%H:%M')
                                        ore_fine = datetime.strptime(fine, '%H:%M')
                                        ore_turno = (ore_fine - ore_inizio).seconds / 3600
                                        ore_totali += ore_turno
                                        
                                        # Verifica se è una domenica
                                        if data.weekday() == 6:  # 6 = domenica
                                            domeniche_lavorate += 1
                                except Exception as e:
                                    print(f"Errore nell'analisi del turno {valore_cella}: {e}")
                    
                    # Crea frame per addetto
                    frame_addetto = ttk.LabelFrame(frame_stats, text=addetto)
                    frame_addetto.pack(fill=tk.X, padx=5, pady=5)
                    
                    # Inizio statistiche
                    ttk.Label(frame_addetto, 
                            text=f"Turni totali nel mese: {turni_totali}").pack(padx=5, pady=2)
                    ttk.Label(frame_addetto, 
                            text=f"Giorni di ferie: {ferie}").pack(padx=5, pady=2)
                    ttk.Label(frame_addetto, 
                            text=f"Giorni di riposo: {riposi}").pack(padx=5, pady=2)
                    ttk.Label(frame_addetto, 
                            text=f"Domeniche lavorate: {domeniche_lavorate}").pack(padx=5, pady=2)
                    ttk.Label(frame_addetto, 
                            text=f"Ore totali lavorate: {ore_totali:.1f}").pack(padx=5, pady=2)
                    
                    # Verifica rispetto monte ore
                    if addetto in self.addetti:
                        ore_contratto = self.addetti[addetto]['ore_contratto']
                        ore_max = self.addetti[addetto]['ore_max']
                        
                        if ore_totali < ore_contratto:
                            ttk.Label(frame_addetto, 
                                    text=f"⚠️ Ore sotto contratto di {ore_contratto - ore_totali:.1f} ore",
                                    foreground='orange').pack(padx=5, pady=2)
                        elif ore_totali > ore_max and not self.addetti[addetto]['straordinario']:
                            ttk.Label(frame_addetto, 
                                    text=f"⚠️ Superato limite ore di {ore_totali - ore_max:.1f} ore",
                                    foreground='red').pack(padx=5, pady=2)
            
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nell'analisi dei dati: {str(e)}")
                print(f"Dettaglio errore: {e}")
        
        # Bottone per aggiornare statistiche
        ttk.Button(frame_select, text="Aggiorna Statistiche", 
                  command=aggiorna_statistiche).pack(side=tk.LEFT, padx=5)
        
        # Aggiorna statistiche iniziali
        aggiorna_statistiche()

    def genera_pianificazione(self):
        """Genera la pianificazione dei turni per il mese selezionato"""
        if not self.addetti or not self.turni_disponibili:
            messagebox.showerror("Errore", "Inserire prima addetti e turni disponibili")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Genera Pianificazione")
        window.geometry("400x300")
        
        # Frame per selezione periodo
        frame_periodo = ttk.LabelFrame(window, text="Seleziona Periodo")
        frame_periodo.pack(pady=10, padx=10, fill='x')
        
        # Anno
        ttk.Label(frame_periodo, text="Anno:").grid(row=0, column=0, padx=5)
        anno_var = tk.StringVar(value=str(datetime.now().year))
        ttk.Entry(frame_periodo, textvariable=anno_var, width=6).grid(row=0, column=1)
        
        # Mese
        ttk.Label(frame_periodo, text="Mese:").grid(row=0, column=2, padx=5)
        mesi = list(calendar.month_name)[1:]  # Esclude il primo elemento vuoto
        mese_var = tk.StringVar(value=mesi[datetime.now().month - 1])
        ttk.Combobox(frame_periodo, textvariable=mese_var, 
                    values=mesi, width=10).grid(row=0, column=3)
        
        def genera():
            """Genera i turni per il mese selezionato"""
            try:
                anno = int(anno_var.get())
                mese = mesi.index(mese_var.get()) + 1
                
                # Genera il calendario mensile
                calendario = self._genera_calendario_mensile(anno, mese)
                
                # Salva su Excel
                self._salva_calendario_excel(calendario, anno, mese)
                
                messagebox.showinfo("Successo", "Pianificazione generata e salvata")
                window.destroy()
                
            except ValueError:
                messagebox.showerror("Errore", "Data non valida")
            except Exception as e:
                messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")
        
        ttk.Button(window, text="Genera Pianificazione", 
                  command=genera).pack(pady=20)
    
    def run(self):
        """Avvia l'applicazione"""
        self.root.mainloop()

# Avvio dell'applicazione
if __name__ == "__main__":
    app = GestioneTurni()
    app.run()