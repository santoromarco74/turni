"""
ANALISI TURNI OTTIMALI - Con vincolo MAX 9 ore/giorno
Orario nastro: 08:00-21:00 (13 ore totali)
Personale fisso: Matteo, Simona, Sara, Melissa
"""

# ============================================================================
# ANALISI ATTUALE
# ============================================================================

TURNI_ATTUALI = [
    ("08:00", "14:00"),    # Turno 1: 6 ore
    ("08:00", "14:30"),    # Turno 2: 6.5 ore
    ("14:00", "21:00"),    # Turno 3: 7 ore
    ("14:30", "21:00"),    # Turno 4: 6.5 ore
    ("14:00", "18:30"),    # Turno 5: 4.5 ore
    ("14:00", "19:00"),    # Turno 6: 5 ore
    ("08:00", "14:00"),    # Turno 7: 6 ore DUPLICATO!
    ("14:00", "21:00"),    # Turno 8: 7 ore DUPLICATO!
]

CONTRATTI_PERSONALE = {
    "Matteo": {
        "ore_contratto": 20,
        "ore_max": 44,
        "giorni_riposo": [0],  # Domenica
        "giorni_disponibili": 6
    },
    "Simona": {
        "ore_contratto": 38,
        "ore_max": 48,
        "giorni_riposo": [4],  # Giovedì
        "giorni_disponibili": 6
    },
    "Sara": {
        "ore_contratto": 19,
        "ore_max": 19,
        "giorni_riposo": [1, 3, 5, 6],  # Lun, Mer, Ven, Sab
        "giorni_disponibili": 2  # Solo Mar+Gio
    },
    "Melissa": {
        "ore_contratto": 24,
        "ore_max": 44,
        "giorni_riposo": [2],  # Martedì
        "giorni_disponibili": 6
    }
}

# ============================================================================
# SOLUZIONE: TURNI OTTIMALI (Max 9 ore, copertura 08:00-21:00)
# ============================================================================

TURNI_PROPOSTI = [
    ("08:00", "16:00"),    # Turno A: 8 ore - mattina estesa
    ("08:00", "16:30"),    # Turno B: 8.5 ore - mattina molto estesa
    ("09:00", "17:00"),    # Turno C: 8 ore - mattina tardiva
    ("12:00", "21:00"),    # Turno D: 9 ore - pomeriggio completo
    ("13:00", "21:00"),    # Turno E: 8 ore - pomeriggio standard
    ("14:00", "21:00"),    # Turno F: 7 ore - pomeriggio breve (mantenere)
]

# ============================================================================
# ANALISI COPERTURA ORARIA
# ============================================================================

print("=" * 80)
print("ANALISI COPERTURA ORARIA")
print("=" * 80)

FASCE = {
    "08:00-09:00": ["A", "B", "C"],
    "09:00-12:00": ["A", "B", "C"],
    "12:00-13:00": ["A", "B", "C", "D"],
    "13:00-14:00": ["A", "B", "C", "D", "E"],
    "14:00-16:00": ["A", "B", "C", "D", "E", "F"],
    "16:00-16:30": ["B", "D", "E", "F"],
    "16:30-17:00": ["D", "E", "F"],
    "17:00-21:00": ["D", "E", "F"],
}

print("\nFASCE ORARIE E COPERTURA:\n")
for fascia, turni in FASCE.items():
    print(f"  {fascia}: {', '.join(turni)} ({len(turni)} operatori)")

print("\n" + "=" * 80)
print("DETTAGLIO TURNI PROPOSTI")
print("=" * 80)

turni_info = [
    ("A", "08:00", "16:00", 8.0, "Mattina estesa"),
    ("B", "08:00", "16:30", 8.5, "Mattina molto estesa"),
    ("C", "09:00", "17:00", 8.0, "Mattina tardiva"),
    ("D", "12:00", "21:00", 9.0, "Pomeriggio completo"),
    ("E", "13:00", "21:00", 8.0, "Pomeriggio standard"),
    ("F", "14:00", "21:00", 7.0, "Pomeriggio breve"),
]

for sigla, inizio, fine, ore, desc in turni_info:
    print(f"\n  Turno {sigla}: {inizio}-{fine} = {ore:.1f} ore ({desc})")

# ============================================================================
# ANALISI FATTIBILITÀ PER OGNI ADDETTO
# ============================================================================

print("\n" + "=" * 80)
print("FATTIBILITÀ CONTRATTI PERSONALE")
print("=" * 80)

ANALISI = {
    "Matteo": {
        "contratto": 20,
        "max": 44,
        "riposo": "Domenica",
        "giorni_disp": 6,
        "turni_suggeriti": ["A", "B", "C", "F"],
        "ore_medio": 7.5,
        "turni_settimana": 3,
        "ore_totali": 22.5,
        "verdict": "✅ FATTIBILE"
    },
    "Simona": {
        "contratto": 38,
        "max": 48,
        "riposo": "Giovedì",
        "giorni_disp": 6,
        "turni_suggeriti": ["A", "B", "D", "E", "F"],
        "ore_medio": 8.1,
        "turni_settimana": 5,
        "ore_totali": 40.5,
        "verdict": "✅ FATTIBILE"
    },
    "Sara": {
        "contratto": 19,
        "max": 19,
        "riposo": "Lun, Mer, Ven, Sab",
        "giorni_disp": 2,
        "turni_suggeriti": ["D", "E"],
        "ore_medio": 8.5,
        "turni_settimana": 2,
        "ore_totali": 17.0,
        "verdict": "⚠️ CRITICO - Serve 19h, max 17h con 2 giorni"
    },
    "Melissa": {
        "contratto": 24,
        "max": 44,
        "riposo": "Martedì",
        "giorni_disp": 6,
        "turni_suggeriti": ["A", "B", "C", "D", "E", "F"],
        "ore_medio": 7.9,
        "turni_settimana": 3,
        "ore_totali": 23.7,
        "verdict": "✅ FATTIBILE"
    }
}

for addetto, info in ANALISI.items():
    print(f"\n{addetto}:")
    print(f"  Contratto: {info['contratto']} ore/sett (max {info['max']})")
    print(f"  Riposo: {info['riposo']}")
    print(f"  Giorni disponibili: {info['giorni_disp']}/7")
    print(f"  Turni suggeriti: {', '.join(info['turni_suggeriti'])}")
    print(f"  Turni/settimana: {info['turni_settimana']} × {info['ore_medio']:.1f}h = {info['ore_totali']:.1f}h")
    print(f"  Status: {info['verdict']}")

# ============================================================================
# PROBLEMA SARA
# ============================================================================

print("\n" + "=" * 80)
print("⚠️ PROBLEMA CRITICO: SARA")
print("=" * 80)

print("""
Sara ha vincoli molto restrittivi:
  - Ore contratto: 19 ore/settimana
  - Giorni disponibili: SOLO martedì e giovedì (2 giorni!)
  - Ore necessarie/giorno: 19 ÷ 2 = 9.5 ore/giorno

Turni disponibili:
  - Turno D (12:00-21:00): 9 ore ✅
  - Turno E (13:00-21:00): 8 ore ❌ (19-8=11 ore per il 2° giorno, troppo)

SOLUZIONI:

1. OPZIONE A (CONSIGLIATA): Modificare i giorni di riposo di Sara
   Attualmente riposa: Lun, Mer, Ven, Sab (4 giorni)
   Suggerito: Riposa Dom, Lun (2 giorni)
   Risultato: Disponibile Mar, Mer, Gio, Ven, Sab (5 giorni)
   Ore/giorno: 19 ÷ 5 = 3.8 ore/giorno ✅ REALIZZABILE

2. OPZIONE B: Permettere doppi turni nello stesso giorno
   Martedì: Turno D (12:00-21:00, 9 ore)
   Giovedì: Turno D (12:00-21:00, 9 ore) + Turno F (14:00-21:00, 7 ore)
   Problema: 9 ore + 7 ore = 16 ore! (max contratto 19) = solo 10 ore per altri giorni

3. OPZIONE C: Doppio turno suddiviso
   Martedì: Turno E (13:00-21:00, 8 ore)
   Giovedì: Turno A (08:00-16:00, 8 ore) + Turno F (14:00-21:00, 7 ore)
   Problema: 8 ore + 7 ore = 15 ore! (max 19) = solo 4 ore per il 3° giorno

4. OPZIONE D: Aumentare a 3 giorni (Opzione A è migliore)
""")

# ============================================================================
# SCENARIO ROTAZIONE SETTIMANALE PROPOSTO
# ============================================================================

print("\n" + "=" * 80)
print("SCENARIO ROTAZIONE SETTIMANALE PROPOSTO")
print("=" * 80)

ROTAZIONE_PROPOSTA = {
    "Matteo": {
        "Lunedì": "Turno A (08:00-16:00, 8h)",
        "Martedì": "Riposo",
        "Mercoledì": "Turno B (08:00-16:30, 8.5h)",
        "Giovedì": "Turno F (14:00-21:00, 7h)",
        "Venerdì": "Riposo",
        "Sabato": "Turno A (08:00-16:00, 8h)",
        "Domenica": "RIPOSO FISSO",
        "Totale": "23.5 ore"
    },
    "Simona": {
        "Lunedì": "Turno D (12:00-21:00, 9h)",
        "Martedì": "Turno B (08:00-16:30, 8.5h)",
        "Mercoledì": "Turno E (13:00-21:00, 8h)",
        "Giovedì": "RIPOSO FISSO",
        "Venerdì": "Turno C (09:00-17:00, 8h)",
        "Sabato": "Turno A (08:00-16:00, 8h)",
        "Domenica": "Riposo",
        "Totale": "41.5 ore"
    },
    "Sara": {
        "Lunedì": "RIPOSO FISSO",
        "Martedì": "Turno D (12:00-21:00, 9h) + Turno F pomeriggio? NO!",
        "Mercoledì": "Riposo",
        "Giovedì": "Turno E (13:00-21:00, 8h) + extra? NO!",
        "Venerdì": "RIPOSO FISSO",
        "Sabato": "RIPOSO FISSO",
        "Domenica": "Riposo",
        "Nota": "⚠️ SERVE RISOLUZIONE (vedi Opzione A consigliata)"
    },
    "Melissa": {
        "Lunedì": "Turno A (08:00-16:00, 8h)",
        "Martedì": "RIPOSO FISSO",
        "Mercoledì": "Turno D (12:00-21:00, 9h)",
        "Giovedì": "Turno B (08:00-16:30, 8.5h)",
        "Venerdì": "Turno E (13:00-21:00, 8h)",
        "Sabato": "Riposo",
        "Domenica": "Riposo",
        "Totale": "33.5 ore"
    }
}

for addetto, giorni in ROTAZIONE_PROPOSTA.items():
    print(f"\n{addetto}:")
    for giorno, turno in giorni.items():
        print(f"  {giorno:10}: {turno}")

# ============================================================================
# RIEPILOGO E RACCOMANDAZIONI
# ============================================================================

print("\n" + "=" * 80)
print("RIEPILOGO E RACCOMANDAZIONI")
print("=" * 80)

print("""
✅ PUNTI POSITIVI:
  - Turni da 8-9 ore sono gestibili (nessuno oltre 9h)
  - Copertura 08:00-21:00 è completa in tutte le fasce
  - Matteo, Simona, Melissa riescono a coprire i contratti
  - Buona varietà di turni per rotazione equa

⚠️ PROBLEMI:
  1. Turni duplicati nel file JSON (indici 6 e 7) - RIMUOVERE
  2. Sara non riesce a coprire 19 ore con soli 2 giorni

📋 AZIONI CONSIGLIATE:

1. IMMEDIATO: Pulire il JSON
   - Rimuovere indici 6 e 7 (turni duplicati)
   - Tenere solo 6 turni distinti

2. ENTRO 1 GIORNO: Decidere su Sara
   - Opzione A (consigliata): Modificare giorni riposo (Dom+Lun anziché Lun+Mer+Ven+Sab)
   - Opzione B: Permettere doppi turni nello stesso giorno
   - Opzione C: Ridurre contratto da 19 a 14 ore

3. ENTRO 1 SETTIMANA: Testare
   - Eseguire `python3 ESEMPIO_REFACTORING.py` con nuovi turni
   - Verificare che `genera_pianificazione()` funziona
   - Generare Excel di prova per una settimana

4. ONGOING: Monitore performance
   - Monitorare stanchezza del personale (max 9h è limite)
   - Raccogliere feedback su equilibrio turni
   - Aggiustare rotazione se necessario
""")

# ============================================================================
# JSON PROPOSTO PULITO
# ============================================================================

TURNI_JSON_PROPOSTI = [
    ["08:00", "16:00"],    # A: 8h
    ["08:00", "16:30"],    # B: 8.5h
    ["09:00", "17:00"],    # C: 8h
    ["12:00", "21:00"],    # D: 9h (copre pomeriggio completo)
    ["13:00", "21:00"],    # E: 8h
    ["14:00", "21:00"],    # F: 7h
]

print("\n" + "=" * 80)
print("JSON DA COPIARE")
print("=" * 80)

import json

json_proposto = {
    "addetti": {
        "Matteo": {
            "ore_contratto": 20,
            "ore_max": 44,
            "ferie": ["2024-01-15", "2024-02-10", "2024-02-11"],
            "giorni_riposo": [0]
        },
        "Simona": {
            "ore_contratto": 38,
            "ore_max": 48,
            "straordinario": True,
            "giorni_riposo": [4],
            "ferie": []
        },
        "Sara": {
            "ore_contratto": 19,
            "ore_max": 19,
            "straordinario": False,
            "giorni_riposo": [1, 3, 5, 6],
            "ferie": [],
            "nota": "⚠️ Critico: 2 giorni disponibili, 19 ore necessarie. Vedere opzioni di soluzione."
        },
        "Melissa": {
            "ore_contratto": 24,
            "ore_max": 44,
            "straordinario": True,
            "giorni_riposo": [2],
            "ferie": []
        }
    },
    "turni": TURNI_JSON_PROPOSTI,
    "note": "Turni ottimizzati: max 9 ore/giorno, copertura 08:00-21:00 completa"
}

print("\n" + json.dumps(json_proposto, indent=2, ensure_ascii=False))

# ============================================================================
# FINE
# ============================================================================

print("\n" + "=" * 80)
print("✅ ANALISI COMPLETATA")
print("=" * 80)
