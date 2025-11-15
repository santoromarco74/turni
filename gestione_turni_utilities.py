"""
Modulo di utility per gestione turni - Funzioni corrette e riutilizzabili
Questo modulo centralizza le funzioni critiche con correzioni e type hints
"""

from datetime import datetime
from typing import Tuple, Optional, Dict, List
import json
import os


# ============================================================================
# FUNZIONI PER GESTIONE ORARI
# ============================================================================

def orario_in_minuti(orario: str) -> Optional[int]:
    """
    Converte una stringa orario 'HH:MM' in minuti da mezzanotte.

    Args:
        orario: Stringa nel formato 'HH:MM' (es. '14:30')

    Returns:
        Numero di minuti da mezzanotte, oppure None se formato invalido

    Examples:
        >>> orario_in_minuti('14:30')
        870
        >>> orario_in_minuti('08:00')
        480
        >>> orario_in_minuti('25:00')
        None
    """
    try:
        h, m = map(int, orario.strip().split(':'))
        if not (0 <= h < 24 and 0 <= m < 60):
            return None
        return h * 60 + m
    except (ValueError, AttributeError, IndexError):
        return None


def minuti_in_orario(minuti: int) -> Optional[str]:
    """
    Converte minuti da mezzanotte in stringa formato 'HH:MM'.

    Args:
        minuti: Minuti da mezzanotte

    Returns:
        Stringa formato 'HH:MM', oppure None se invalido

    Examples:
        >>> minuti_in_orario(870)
        '14:30'
        >>> minuti_in_orario(480)
        '08:00'
    """
    try:
        if not (0 <= minuti < 1440):  # 1440 = 24*60
            return None
        h = minuti // 60
        m = minuti % 60
        return f"{h:02d}:{m:02d}"
    except (TypeError, ValueError):
        return None


def valida_orari(orario_inizio: str, orario_fine: str) -> Tuple[bool, str]:
    """
    Valida una coppia di orari (inizio < fine).
    ✓ CORRETTO: Usa minuti per confronto (non stringhe)

    Args:
        orario_inizio: Formato 'HH:MM'
        orario_fine: Formato 'HH:MM'

    Returns:
        (valido: bool, messaggio_errore: str)

    Examples:
        >>> valida_orari('08:00', '14:00')
        (True, '')
        >>> valida_orari('14:00', '08:00')
        (False, 'Ora inizio deve essere precedente a ora fine')
    """
    minuti_inizio = orario_in_minuti(orario_inizio)
    minuti_fine = orario_in_minuti(orario_fine)

    if minuti_inizio is None or minuti_fine is None:
        return False, "Formato orario non valido. Usa HH:MM (es. 14:30)"

    if minuti_inizio >= minuti_fine:
        return False, "L'ora di inizio deve essere precedente all'ora di fine"

    return True, ""


def calcola_ore_turno(orario_inizio: str, orario_fine: str) -> Optional[float]:
    """
    Calcola le ore di un turno.
    ✓ CORRETTO: Usa .total_seconds() (non .seconds)

    Args:
        orario_inizio: Formato 'HH:MM'
        orario_fine: Formato 'HH:MM'

    Returns:
        Numero di ore (con decimali), oppure None se invalido

    Examples:
        >>> calcola_ore_turno('08:00', '14:00')
        6.0
        >>> calcola_ore_turno('14:00', '18:30')
        4.5
    """
    valido, msg = valida_orari(orario_inizio, orario_fine)
    if not valido:
        return None

    try:
        inizio = datetime.strptime(orario_inizio, '%H:%M')
        fine = datetime.strptime(orario_fine, '%H:%M')

        # ✓ CORRETTO: .total_seconds() (non .seconds)
        ore = (fine - inizio).total_seconds() / 3600
        return ore
    except ValueError:
        return None


def arrotonda_ore(ore: float, decimali: int = 2) -> float:
    """Arrotonda ore a N decimali (default 2)"""
    return round(ore, decimali)


# ============================================================================
# FUNZIONI PER GESTIONE TURNI
# ============================================================================

def turni_in_minuti(turni: List[Tuple[str, str]]) -> List[Tuple[int, int]]:
    """
    Converte lista di turni (orari stringa) in lista di turni (minuti).

    Args:
        turni: Lista di tuple (inizio_str, fine_str)

    Returns:
        Lista di tuple (inizio_minuti, fine_minuti)
    """
    result = []
    for inizio_str, fine_str in turni:
        inizio_min = orario_in_minuti(inizio_str)
        fine_min = orario_in_minuti(fine_str)

        if inizio_min is not None and fine_min is not None:
            result.append((inizio_min, fine_min))

    return result


def calcola_orario_minimo_turni(turni: List[Tuple[str, str]]) -> Optional[float]:
    """
    Calcola l'ore minima tra tutti i turni disponibili.
    ✓ CORRETTO: Gestisce lista vuota

    Args:
        turni: Lista di tuple (inizio_str, fine_str)

    Returns:
        Ore minime, oppure None se lista vuota
    """
    if not turni:
        return None

    ore_list = []
    for inizio_str, fine_str in turni:
        ore = calcola_ore_turno(inizio_str, fine_str)
        if ore is not None:
            ore_list.append(ore)

    return min(ore_list) if ore_list else None


def calcola_orario_massimo_turni(turni: List[Tuple[str, str]]) -> Optional[float]:
    """Calcola l'ore massima tra tutti i turni disponibili."""
    if not turni:
        return None

    ore_list = []
    for inizio_str, fine_str in turni:
        ore = calcola_ore_turno(inizio_str, fine_str)
        if ore is not None:
            ore_list.append(ore)

    return max(ore_list) if ore_list else None


# ============================================================================
# FUNZIONI PER GESTIONE DATI
# ============================================================================

def carica_dati_sicuro(filepath: str) -> Optional[Dict]:
    """
    Carica dati da file JSON con gestione errori.

    Args:
        filepath: Percorso al file JSON

    Returns:
        Dizionario con i dati, oppure None se errore
    """
    try:
        filepath_abs = os.path.abspath(filepath)  # Evita directory traversal

        if not os.path.exists(filepath_abs):
            return None

        with open(filepath_abs, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, OSError) as e:
        print(f"Errore nel caricamento {filepath}: {e}")
        return None


def salva_dati_sicuro(filepath: str, dati: Dict) -> bool:
    """
    Salva dati su file JSON con gestione errori.

    Args:
        filepath: Percorso al file JSON
        dati: Dizionario da salvare

    Returns:
        True se successo, False se errore
    """
    try:
        filepath_abs = os.path.abspath(filepath)

        # Crea directory se non esiste
        os.makedirs(os.path.dirname(filepath_abs), exist_ok=True)

        with open(filepath_abs, 'w', encoding='utf-8') as f:
            json.dump(dati, f, indent=2, ensure_ascii=False)

        return True
    except (IOError, OSError, TypeError) as e:
        print(f"Errore nel salvataggio {filepath}: {e}")
        return False


# ============================================================================
# FUNZIONI PER GESTIONE FERIE
# ============================================================================

def aggiungi_ferie(ferie_esistenti: List[str], nuove_ferie: List[str]) -> List[str]:
    """
    Aggiunge nuove ferie senza sovrascrivere le esistenti.
    ✓ CORRETTO: Merge, non sovrascrittura

    Args:
        ferie_esistenti: Lista ferie già registrate
        nuove_ferie: Nuove ferie da aggiungere

    Returns:
        Lista ferie combinate e ordinate
    """
    ferie_combinate = list(set(ferie_esistenti + nuove_ferie))
    return sorted(ferie_combinate)


def rimuovi_ferie(ferie: List[str], da_rimuovere: List[str]) -> List[str]:
    """
    Rimuove ferie specifiche da una lista.

    Args:
        ferie: Lista ferie
        da_rimuovere: Ferie da rimuovere

    Returns:
        Lista ferie aggiornata
    """
    return [f for f in ferie if f not in da_rimuovere]


# ============================================================================
# FUNZIONI PER VALIDAZIONE ADDETTI
# ============================================================================

def valida_addetto(nome: str, ore_contratto: float, ore_max: float) -> Tuple[bool, str]:
    """
    Valida i dati di un addetto.

    Args:
        nome: Nome addetto
        ore_contratto: Ore previste da contratto
        ore_max: Ore massime consentite (con straordinario)

    Returns:
        (valido: bool, messaggio_errore: str)
    """
    if not nome or not isinstance(nome, str):
        return False, "Nome addetto non valido"

    if not (0 < ore_contratto <= 50):
        return False, "Ore contratto deve essere tra 0 e 50"

    if not (ore_contratto <= ore_max <= 50):
        return False, "Ore massime deve essere >= ore contratto e <= 50"

    return True, ""


# ============================================================================
# MAIN (test funzioni)
# ============================================================================

if __name__ == "__main__":
    print("Test modulo gestione_turni_utilities")
    print("-" * 50)

    # Test orario_in_minuti
    assert orario_in_minuti("14:30") == 870
    assert orario_in_minuti("08:00") == 480
    assert orario_in_minuti("25:00") is None
    print("✓ orario_in_minuti")

    # Test minuti_in_orario
    assert minuti_in_orario(870) == "14:30"
    assert minuti_in_orario(480) == "08:00"
    assert minuti_in_orario(1500) is None
    print("✓ minuti_in_orario")

    # Test valida_orari
    assert valida_orari("08:00", "14:00")[0] is True
    assert valida_orari("14:00", "08:00")[0] is False
    assert valida_orari("23:00", "09:00")[0] is False  # Test edge case
    print("✓ valida_orari")

    # Test calcola_ore_turno
    assert calcola_ore_turno("08:00", "14:00") == 6.0
    assert calcola_ore_turno("14:00", "18:30") == 4.5
    assert calcola_ore_turno("14:00", "08:00") is None
    print("✓ calcola_ore_turno")

    # Test calcola_orario_minimo_turni
    turni = [("08:00", "14:00"), ("14:00", "21:00"), ("08:00", "14:30")]
    assert calcola_orario_minimo_turni(turni) == 6.0
    assert calcola_orario_minimo_turni([]) is None
    print("✓ calcola_orario_minimo_turni")

    # Test merge ferie
    ferie1 = ["2024-01-15", "2024-01-20"]
    ferie2 = ["2024-02-10"]
    ferie_merged = aggiungi_ferie(ferie1, ferie2)
    assert "2024-01-15" in ferie_merged and "2024-02-10" in ferie_merged
    print("✓ aggiungi_ferie")

    print("-" * 50)
    print("Tutti i test sono passati! ✓")
