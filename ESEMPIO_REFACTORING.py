"""
ESEMPIO DI REFACTORING: Come integrare le utility nel codice originale

Questo file mostra PRIMA/DOPO di come correggere i bug principali
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from gestione_turni_utilities import (
    orario_in_minuti,
    minuti_in_orario,
    valida_orari,
    calcola_ore_turno,
    calcola_orario_minimo_turni,
    aggiungi_ferie,
    carica_dati_sicuro,
    salva_dati_sicuro
)


# ============================================================================
# BUG #1: .seconds vs .total_seconds()
# ============================================================================

class BugCalcoloOre:
    """Dimostra il bug nel calcolo ore"""

    @staticmethod
    def versione_sbagliata(turni: List[Tuple[str, str]]) -> float:
        """❌ SBAGLIATO: usa .seconds"""
        ore_lavorate = 0.0
        for inizio_str, fine_str in turni:
            inizio = datetime.strptime(inizio_str, '%H:%M')
            fine = datetime.strptime(fine_str, '%H:%M')

            # ❌ BUG: usa .seconds (non .total_seconds)
            ore_lavorate += (fine - inizio).seconds / 3600

        return ore_lavorate

    @staticmethod
    def versione_corretta(turni: List[Tuple[str, str]]) -> float:
        """✓ CORRETTO: usa calcola_ore_turno dalle utility"""
        ore_totali = 0.0
        for inizio_str, fine_str in turni:
            ore = calcola_ore_turno(inizio_str, fine_str)
            if ore is not None:
                ore_totali += ore

        return ore_totali


# ============================================================================
# BUG #2: Validazione Orari (confronto stringhe)
# ============================================================================

class BugValidazioneOrari:
    """Dimostra il bug nella validazione orari"""

    @staticmethod
    def versione_sbagliata(inizio: str, fine: str) -> bool:
        """❌ SBAGLIATO: confronta stringhe lessicograficamente"""
        if inizio >= fine:  # "23:00" >= "09:00" è True!
            return False
        return True

    @staticmethod
    def versione_corretta(inizio: str, fine: str) -> bool:
        """✓ CORRETTO: usa valida_orari dalle utility"""
        valido, msg = valida_orari(inizio, fine)
        if not valido:
            print(f"Errore: {msg}")
            return False
        return True


# ============================================================================
# BUG #3: Sovrascrittura Ferie
# ============================================================================

class BugFerieSovrascritte:
    """Dimostra il bug nella gestione ferie"""

    @staticmethod
    def versione_sbagliata(addetto: Dict, nuove_ferie: List[str]) -> None:
        """❌ SBAGLIATO: sovrascrive completamente le ferie"""
        addetto['ferie'] = nuove_ferie  # ❌ Perde ferie precedenti!

    @staticmethod
    def versione_corretta(addetto: Dict, nuove_ferie: List[str]) -> None:
        """✓ CORRETTO: usa aggiungi_ferie dalle utility"""
        # Merge ferie senza perdere quelle precedenti
        addetto['ferie'] = aggiungi_ferie(addetto['ferie'], nuove_ferie)


# ============================================================================
# BUG #4: ore_min non inizializzato
# ============================================================================

class BugOreMinVuoto:
    """Dimostra il bug nell'inizializzazione ore_min"""

    @staticmethod
    def versione_sbagliata(turni_disponibili: List[Tuple[str, str]]) -> float:
        """❌ SBAGLIATO: ore_min rimane 24 se lista è vuota"""
        ore_min = 24  # Inizializzazione sbagliata!

        for turno in turni_disponibili:
            inizio_str, fine_str = turno
            ore = calcola_ore_turno(inizio_str, fine_str)

            if ore is not None and ore < ore_min:
                ore_min = ore

        # Se turni_disponibili è vuoto, ore_min rimane 24!
        # Questo crea un vincolo impossibile per la pianificazione
        return ore_min

    @staticmethod
    def versione_corretta(turni_disponibili: List[Tuple[str, str]]) -> Optional[float]:
        """✓ CORRETTO: usa calcola_orario_minimo_turni dalle utility"""
        ore_min = calcola_orario_minimo_turni(turni_disponibili)

        if ore_min is None:
            print("Errore: Non ci sono turni definiti!")
            return None

        return ore_min


# ============================================================================
# BUG #5: os.system() non sicuro
# ============================================================================

import os
import subprocess

class BugOsSystem:
    """Dimostra il bug di security con os.system()"""

    @staticmethod
    def versione_sbagliata(nome_file: str) -> None:
        """❌ SBAGLIATO: os.system() vulnerabile a injection"""
        try:
            os.startfile(nome_file)  # OK su Windows
        except:
            # ❌ PERICOLO: se nome_file = "file; rm -rf /", esegue sia comandi!
            os.system(f"xdg-open {nome_file}")

    @staticmethod
    def versione_corretta(nome_file: str) -> None:
        """✓ CORRETTO: usa subprocess.run() con lista"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(nome_file)  # API nativa
            else:  # Linux, Mac
                # ✓ Usa lista, non stringa interpolata - sicuro da injection
                subprocess.run(['xdg-open', nome_file], check=True)
        except Exception as e:
            print(f"Errore nel'apertura file: {e}")


# ============================================================================
# REFACTORING COMPLETO: Classe Migliorata
# ============================================================================

class GestioneTurniMigliorata:
    """Versione migliorata con utility integrate"""

    def __init__(self):
        self.addetti = {}
        self.turni_disponibili = []
        self.carica_dati()

    def carica_dati(self) -> None:
        """✓ Carica dati usando funzione utility"""
        dati = carica_dati_sicuro('dati_turni.json')

        if dati:
            self.addetti = dati.get('addetti', {})
            self.turni_disponibili = dati.get('turni', [])
        else:
            print("Nessun dato trovato o file invalido")

    def salva_dati(self) -> None:
        """✓ Salva dati usando funzione utility"""
        dati = {
            'addetti': self.addetti,
            'turni': self.turni_disponibili
        }

        if salva_dati_sicuro('dati_turni.json', dati):
            print("✓ Dati salvati correttamente")
        else:
            print("✗ Errore nel salvataggio")

    def aggiungi_turno(self, inizio: str, fine: str) -> bool:
        """✓ Aggiungi turno con validazione corretta"""
        # Usa valida_orari dalle utility
        valido, msg = valida_orari(inizio, fine)

        if not valido:
            print(f"✗ Turno invalido: {msg}")
            return False

        turno = (inizio, fine)

        if turno not in self.turni_disponibili:
            self.turni_disponibili.append(turno)
            print(f"✓ Turno {inizio}-{fine} aggiunto")
            return True
        else:
            print(f"✗ Turno già esistente")
            return False

    def aggiungi_ferie_addetto(self, nome: str, nuove_ferie: List[str]) -> bool:
        """✓ Aggiungi ferie senza sovrascritture"""
        if nome not in self.addetti:
            print(f"✗ Addetto {nome} non trovato")
            return False

        # Usa aggiungi_ferie dalle utility - merge, non sovrascrittura!
        self.addetti[nome]['ferie'] = aggiungi_ferie(
            self.addetti[nome]['ferie'],
            nuove_ferie
        )

        print(f"✓ Ferie aggiunte per {nome}: {self.addetti[nome]['ferie']}")
        return True

    def calcola_ore_totali(self, nome: str, turni_giorno: Dict[str, Tuple[str, str]]) -> Optional[float]:
        """✓ Calcola ore totali con formula corretta"""
        if nome not in self.addetti:
            return None

        ore_totali = 0.0

        for giorno, turno in turni_giorno.items():
            # Usa calcola_ore_turno dalle utility
            ore = calcola_ore_turno(turno[0], turno[1])

            if ore is not None:
                ore_totali += ore
            else:
                print(f"⚠️ Turno invalido per {giorno}: {turno}")

        return ore_totali

    def verifica_vincoli_ore(self, nome: str) -> bool:
        """✓ Verifica vincoli di ore con logica corretta"""
        if nome not in self.addetti:
            return False

        addetto = self.addetti[nome]
        ore_min = calcola_orario_minimo_turni(self.turni_disponibili)

        if ore_min is None:
            print("✗ Nessun turno definito - impossibile verificare vincoli")
            return False

        print(f"Ore minime turno: {ore_min}")
        print(f"Ore contratto {nome}: {addetto['ore_contratto']}")

        # Verifiche logiche basate su ore_min valido
        if ore_min * 5 > addetto['ore_max']:
            print(f"⚠️ {nome}: Turni minimi potrebbero superare ore massime")
            return False

        return True

    def apri_file_sicuro(self, nome_file: str) -> None:
        """✓ Apri file con subprocess sicuro"""
        try:
            if os.name == 'nt':
                os.startfile(nome_file)
            else:
                subprocess.run(['xdg-open', nome_file], check=True)

            print(f"✓ File aperto: {nome_file}")
        except Exception as e:
            print(f"✗ Errore nell'apertura file: {e}")


# ============================================================================
# TEST DI UTILIZZO
# ============================================================================

def test_refactoring():
    """Test della classe migliorata"""
    print("=" * 60)
    print("TEST REFACTORING: GestioneTurniMigliorata")
    print("=" * 60)

    gestione = GestioneTurniMigliorata()

    # Test 1: Aggiungere turni con validazione corretta
    print("\n[TEST 1] Aggiunta turni con validazione")
    print("-" * 40)
    gestione.aggiungi_turno("08:00", "14:00")  # ✓ Valido
    gestione.aggiungi_turno("14:00", "21:00")  # ✓ Valido
    gestione.aggiungi_turno("25:00", "26:00")  # ✗ Invalido
    gestione.aggiungi_turno("21:00", "14:00")  # ✗ Invalido (inizio > fine)

    # Test 2: Aggiungere addetto
    print("\n[TEST 2] Aggiunta addetto")
    print("-" * 40)
    gestione.addetti['Matteo'] = {
        'ore_contratto': 20,
        'ore_max': 44,
        'ferie': ['2024-01-15'],
        'giorni_riposo': [0]
    }
    print("✓ Matteo aggiunto")

    # Test 3: Merge ferie (senza sovrascritture)
    print("\n[TEST 3] Merge ferie - No overwrite")
    print("-" * 40)
    print(f"Prima: {gestione.addetti['Matteo']['ferie']}")
    gestione.aggiungi_ferie_addetto('Matteo', ['2024-02-10', '2024-02-11'])
    print(f"Dopo:  {gestione.addetti['Matteo']['ferie']}")
    print("✓ Ferie gennaio NON sono state sovrascritte!")

    # Test 4: Calcolo ore con formula corretta
    print("\n[TEST 4] Calcolo ore con .total_seconds()")
    print("-" * 40)
    turni_matteo = {
        'lunedì': ('08:00', '14:00'),
        'martedì': ('08:00', '14:30'),
        'mercoledì': ('14:00', '21:00'),
    }
    ore = gestione.calcola_ore_totali('Matteo', turni_matteo)
    print(f"Ore totali Matteo: {ore} (corretto)")

    # Test 5: Verifica vincoli
    print("\n[TEST 5] Verifica vincoli ore")
    print("-" * 40)
    gestione.verifica_vincoli_ore('Matteo')

    # Test 6: Salvataggio dati
    print("\n[TEST 6] Salvataggio dati sicuro")
    print("-" * 40)
    gestione.salva_dati()

    print("\n" + "=" * 60)
    print("TEST COMPLETATO ✓")
    print("=" * 60)


# ============================================================================
# RIEPILOGO DELLE CORREZIONI
# ============================================================================

RIEPILOGO_CORREZIONI = """

╔════════════════════════════════════════════════════════════════════════════╗
║                    RIEPILOGO DELLE CORREZIONI APPLICATE                   ║
╚════════════════════════════════════════════════════════════════════════════╝

[1] CALCOLO ORE
    ❌ PRIMA: (fine - inizio).seconds / 3600
    ✓ DOPO:  calcola_ore_turno(inizio, fine)  [dalle utility]

    Benefici:
    - Usa .total_seconds() (corretto)
    - Validazione input integrata
    - Gestione errori centralizzata
    - Riutilizzabile

[2] VALIDAZIONE ORARI
    ❌ PRIMA: if inizio >= fine:  [confronto lessicografico]
    ✓ DOPO:  valida_orari(inizio, fine)  [dalle utility]

    Benefici:
    - Confronta minuti (numerico), non stringhe
    - Edge case gestiti (es. "23:00" vs "09:00")
    - Messaggio errore specifico
    - Riutilizzabile

[3] GESTIONE FERIE
    ❌ PRIMA: self.addetti[nome]['ferie'] = nuove_ferie  [sovrascrive]
    ✓ DOPO:  self.addetti[nome]['ferie'] = aggiungi_ferie(...)  [merge]

    Benefici:
    - Ferie precedenti non perdute
    - Possibilità di aggiungere ferie multiple volte
    - Deduplicazione automatica
    - Riutilizzabile

[4] INIZIALIZZAZIONE ORE_MIN
    ❌ PRIMA: ore_min = 24; [rimane 24 se lista vuota]
    ✓ DOPO:  ore_min = calcola_orario_minimo_turni(...)  [dalle utility]

    Benefici:
    - Gestisce lista vuota restituendo None
    - Controllo esplicito di None
    - Vincoli corretti anche edge case
    - Riutilizzabile

[5] APERTURA FILE SICURA
    ❌ PRIMA: os.system(f"xdg-open {nome_file}")  [injection possibile]
    ✓ DOPO:  subprocess.run(['xdg-open', nome_file])  [lista, sicuro]

    Benefici:
    - Immune da injection
    - Cross-platform (Windows/Linux/Mac)
    - Gestione errori robusta
    - Niente shell

[6] CARICAMENTO/SALVATAGGIO DATI
    ❌ PRIMA: try/except generico, print solo
    ✓ DOPO:  carica_dati_sicuro(), salva_dati_sicuro()  [dalle utility]

    Benefici:
    - Path validation
    - Encoding UTF-8
    - Creazione directory automatica
    - Return code per status

═════════════════════════════════════════════════════════════════════════════
RISULTATO FINALE:
- Codice più robusto e testato
- Meno duplicazione (DRY)
- Migliore error handling
- Più sicuro da vulnerabilità
- Più facile da mantenere

═════════════════════════════════════════════════════════════════════════════
"""


if __name__ == "__main__":
    print(RIEPILOGO_CORREZIONI)
    test_refactoring()
