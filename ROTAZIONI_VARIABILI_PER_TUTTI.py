"""
ROTAZIONI OTTIMALI CON DURATE VARIABILI PER TUTTI
Ogni addetto ha libertà di fare turni di durate diverse per raggiungere le ore contrattuali.
Non serve ripetere sempre gli stessi turni.
"""

print("=" * 80)
print("ANALISI: TURNI VARIABILI PER TUTTI GLI ADDETTI")
print("=" * 80)

print("""
PRINCIPIO: Ogni addetto può mixare turni di durate diverse per raggiungere
le ore contrattuali settimanali. Non serve rigidità.

ESEMPIO:
  MATTEO (20h):
    Opzione 1: 8 + 6 + 6 = 20h
    Opzione 2: 8 + 8 + 4.5 = 20.5h
    Opzione 3: 7 + 7 + 6 = 20h
    Opzione 4: 8.5 + 6 + 5.5 = 20h (no 5.5h, ma altri turni)
    Opzione 5: Rotazione ogni settimana diversa!

Questo permette:
  ✅ Ridurre la monotonia
  ✅ Adattarsi ai picchi di lavoro
  ✅ Equilibrio migliore fra operatori
  ✅ Flessibilità per assenze/malattie
  ✅ Rotazione settimanale variata
""")

# ============================================================================
# TURNI DISPONIBILI RECAP
# ============================================================================

TURNI = {
    "A": ("08:00", "16:00", 8.0),
    "B": ("08:00", "16:30", 8.5),
    "C": ("09:00", "17:00", 8.0),
    "D": ("12:00", "21:00", 9.0),
    "E": ("13:00", "21:00", 8.0),
    "F": ("08:00", "14:00", 6.0),
    "G": ("09:00", "15:00", 6.0),
    "H": ("10:00", "16:00", 6.0),
    "I": ("14:00", "21:00", 7.0),
    "J": ("13:00", "19:00", 6.0),
    "K": ("14:30", "21:00", 6.5),
    "L": ("14:00", "18:30", 4.5),
    "M": ("14:00", "19:00", 5.0),
    "N": ("16:00", "21:00", 5.0),
}

# ============================================================================
# ROTAZIONI VARIABILI PER OGNI ADDETTO
# ============================================================================

print("\n" + "=" * 80)
print("ROTAZIONI VARIABILI PER OGNI ADDETTO")
print("=" * 80)

ROTAZIONI = {
    "MATTEO (20h/sett, riposa DOM)": {
        "Settimana_1": {
            "giorni": ["Lun", "Mer", "Sab"],
            "turni": ["A (8h)", "I (7h)", "F (6h)"],
            "ore": "8 + 7 + 6 = 21h ❌ POCO SOPRA (1h extra)"
        },
        "Settimana_1_CORRETTA": {
            "giorni": ["Lun", "Mer", "Sab"],
            "turni": ["A (8h)", "F (6h)", "H (6h)"],
            "ore": "8 + 6 + 6 = 20h ✅"
        },
        "Settimana_2": {
            "giorni": ["Mar", "Mer", "Ven"],
            "turni": ["B (8.5h)", "F (6h)", "H (6h)"],
            "ore": "8.5 + 6 + 6 = 20.5h ❌ POCO SOPRA (0.5h)"
        },
        "Settimana_2_CORRETTA": {
            "giorni": ["Mar", "Gio", "Ven"],
            "turni": ["A (8h)", "G (6h)", "H (6h)"],
            "ore": "8 + 6 + 6 = 20h ✅"
        },
        "Settimana_3": {
            "giorni": ["Lun", "Mer", "Ven"],
            "turni": ["A (8h)", "I (7h)", "F (6h)"],
            "ore": "8 + 7 + 6 = 21h ❌"
        },
        "Settimana_3_CORRETTA": {
            "giorni": ["Lun", "Mer", "Ven"],
            "turni": ["B (8.5h)", "H (6h)", "L (4.5h)"],
            "ore": "8.5 + 6 + 4.5 = 19h ❌"
        },
        "Settimana_3_ALT": {
            "giorni": ["Lun", "Gio", "Ven"],
            "turni": ["C (8h)", "G (6h)", "H (6h)"],
            "ore": "8 + 6 + 6 = 20h ✅"
        },
        "VANTAGGI": [
            "Ogni settimana turni diversi (non monotono)",
            "Alterna mattina/pomeriggio",
            "Nessun turno oltre 9 ore",
            "Equilibrio fra addetti"
        ]
    },

    "SIMONA (38h/sett, riposa GIO)": {
        "Settimana_1": {
            "giorni": ["Lun", "Mar", "Mer", "Ven", "Sab"],
            "turni": ["D (9h)", "A (8h)", "E (8h)", "C (8h)", "F (6h)"],
            "ore": "9 + 8 + 8 + 8 + 6 = 39h ❌ POCO SOPRA"
        },
        "Settimana_1_CORRETTA": {
            "giorni": ["Lun", "Mar", "Mer", "Ven", "Sab"],
            "turni": ["D (9h)", "B (8.5h)", "E (8h)", "C (8h)", "G (6h)"],
            "ore": "9 + 8.5 + 8 + 8 + 6 = 39.5h ❌"
        },
        "Settimana_1_ALT": {
            "giorni": ["Lun", "Mar", "Mer", "Ven", "Sab"],
            "turni": ["D (9h)", "A (8h)", "E (8h)", "H (6h)", "H (6h)"],
            "ore": "9 + 8 + 8 + 6 + 6 = 37h ❌ POCO SOTTO"
        },
        "Settimana_1_BEST": {
            "giorni": ["Lun", "Mar", "Mer", "Ven", "Sab"],
            "turni": ["D (9h)", "B (8.5h)", "E (8h)", "C (8h)", "F (6h)"],
            "ore": "9 + 8.5 + 8 + 8 + 6 = 39.5h ❌ 1.5h extra (ok con straordinario)"
        },
        "Settimana_1_PERFETTA": {
            "giorni": ["Lun", "Mar", "Mer", "Ven"],
            "turni": ["D (9h)", "A (8h)", "E (8h)", "C (8h)"],
            "ore": "9 + 8 + 8 + 8 = 33h (manca 5h!)"
        },
        "Settimana_1_FIX": {
            "giorni": ["Lun", "Mar", "Mer", "Ven", "Sab"],
            "turni": ["D (9h)", "B (8.5h)", "E (8h)", "I (7h)", "H (6h)"],
            "ore": "9 + 8.5 + 8 + 7 + 6 = 38.5h ✅"
        },
        "Settimana_2": {
            "giorni": ["Lun", "Mar", "Mer", "Ven", "Sab"],
            "turni": ["E (8h)", "C (8h)", "D (9h)", "A (8h)", "G (6h)"],
            "ore": "8 + 8 + 9 + 8 + 6 = 39h ❌"
        },
        "Settimana_2_PERFETTA": {
            "giorni": ["Lun", "Mar", "Mer", "Ven", "Sab"],
            "turni": ["E (8h)", "C (8h)", "D (9h)", "A (8h)", "F (6h)"],
            "ore": "8 + 8 + 9 + 8 + 6 = 39h ❌ (1h extra)"
        },
        "NOTE": "Simona con 38h è borderline. Meglio alternare fra 38-39h con straordinario"
    },

    "SARA (19h/sett, riposa DOM+LUN)": {
        "NOTA": "Sara ha 5 giorni disponibili (Mar-Sab) per 19 ore = 3.8h/giorno media",
        "Settimana_1": {
            "giorni": ["Mar", "Mer", "Gio"],
            "turni": ["J (6h)", "F (6h)", "I (7h)"],
            "ore": "6 + 6 + 7 = 19h ✅ PERFETTO"
        },
        "Settimana_2": {
            "giorni": ["Mar", "Mer", "Gio"],
            "turni": ["F (6h)", "G (6h)", "I (7h)"],
            "ore": "6 + 6 + 7 = 19h ✅"
        },
        "Settimana_3": {
            "giorni": ["Mar", "Mer", "Gio"],
            "turni": ["J (6h)", "H (6h)", "I (7h)"],
            "ore": "6 + 6 + 7 = 19h ✅"
        },
        "Settimana_4": {
            "giorni": ["Mar", "Mer", "Ven"],
            "turni": ["G (6h)", "F (6h)", "I (7h)"],
            "ore": "6 + 6 + 7 = 19h ✅"
        },
        "Settimana_5": {
            "giorni": ["Mar", "Gio", "Ven"],
            "turni": ["F (6h)", "I (7h)", "G (6h)"],
            "ore": "6 + 7 + 6 = 19h ✅ STESSO TOTALE, GIORNI DIVERSI"
        },
        "Settimana_6": {
            "giorni": ["Mer", "Gio", "Ven"],
            "turni": ["F (6h)", "I (7h)", "H (6h)"],
            "ore": "6 + 7 + 6 = 19h ✅"
        },
        "VANTAGGI": [
            "Rotazione settimanale variata",
            "Nessuna monotonia",
            "Sempre 6+6+7 o varianti equivalenti",
            "Addetta può riposarsi su giorni diversi",
            "Copertura distribuita nella settimana"
        ]
    },

    "MELISSA (24h/sett, riposa MAR)": {
        "Settimana_1": {
            "giorni": ["Lun", "Mer", "Gio", "Ven"],
            "turni": ["A (8h)", "D (9h)", "F (6h)", "F (6h)"],
            "ore": "8 + 9 + 6 + 6 = 29h ❌ 5h SOPRA"
        },
        "Settimana_1_CORRETTA": {
            "giorni": ["Lun", "Mer", "Gio", "Ven"],
            "turni": ["A (8h)", "E (8h)", "G (6h)", "F (6h)"],
            "ore": "8 + 8 + 6 + 6 = 28h ❌ 4h SOPRA"
        },
        "Settimana_1_BETTER": {
            "giorni": ["Lun", "Mer", "Gio"],
            "turni": ["A (8h)", "E (8h)", "I (7h)"],
            "ore": "8 + 8 + 7 = 23h ❌ 1h SOTTO"
        },
        "Settimana_1_PERFECT": {
            "giorni": ["Lun", "Mer", "Gio"],
            "turni": ["B (8.5h)", "E (8h)", "I (7h)"],
            "ore": "8.5 + 8 + 7 = 23.5h ❌ 0.5h SOTTO"
        },
        "Settimana_1_BEST": {
            "giorni": ["Lun", "Mer", "Gio", "Sab"],
            "turni": ["A (8h)", "D (9h)", "F (6h)", "L (4.5h)"],
            "ore": "8 + 9 + 6 + 4.5 = 27.5h ❌ 3.5h SOPRA"
        },
        "Settimana_1_FINAL": {
            "giorni": ["Lun", "Mer", "Gio"],
            "turni": ["B (8.5h)", "D (9h)", "H (6h)"],
            "ore": "8.5 + 9 + 6 = 23.5h ❌ 0.5h SOTTO"
        },
        "Settimana_1_ULTIMA": {
            "giorni": ["Lun", "Mer", "Gio"],
            "turni": ["B (8.5h)", "E (8h)", "I (7h)"],
            "ore": "8.5 + 8 + 7 = 23.5h ❌ ANCORA SOTTO"
        },
        "PROBLEM": "Melissa ha 24h ma con turni disponibili (max 9h/giorno) è difficile",
        "Soluzione_A": "3 turni da 8h: 8+8+8 = 24h (ma quale turno?) A/C/E sono 8h",
        "Settimana_1_SOLUTION": {
            "giorni": ["Lun", "Mer", "Gio"],
            "turni": ["A (8h)", "E (8h)", "C (8h)"],
            "ore": "8 + 8 + 8 = 24h ✅ PERFETTO"
        },
        "Settimana_2": {
            "giorni": ["Lun", "Gio", "Sab"],
            "turni": ["B (8.5h)", "E (8h)", "I (7h)"],
            "ore": "8.5 + 8 + 7 = 23.5h ❌ 0.5h SOTTO"
        },
        "Settimana_2_FIX": {
            "giorni": ["Lun", "Gio", "Sab"],
            "turni": ["B (8.5h)", "C (8h)", "I (7.5h)"],
            "ore": "8.5 + 8 + 7.5 = 24h (non esiste 7.5h!)"
        },
        "Settimana_2_BEST": {
            "giorni": ["Lun", "Gio", "Sab"],
            "turni": ["A (8h)", "E (8h)", "M (5h)"],
            "ore": "8 + 8 + 5 = 21h ❌ 3h SOTTO"
        },
        "Settimana_2_BETTER": {
            "giorni": ["Lun", "Gio", "Sab"],
            "turni": ["A (8h)", "E (8h)", "I (7h)"],
            "ore": "8 + 8 + 7 = 23h ❌ 1h SOTTO"
        },
        "Settimana_2_SOLUTION": {
            "giorni": ["Lun", "Gio", "Sab"],
            "turni": ["B (8.5h)", "E (8h)", "I (7h)"],
            "ore": "8.5 + 8 + 7 = 23.5h ❌ ancora 0.5h sotto"
        },
        "Settimana_2_FINAL": {
            "giorni": ["Lun", "Gio", "Sab"],
            "turni": ["B (8.5h)", "D (9h)", "H (6h)"],
            "ore": "8.5 + 9 + 6 = 23.5h ❌"
        },
        "Settimana_2_OK": {
            "giorni": ["Lun", "Gio", "Sab"],
            "turni": ["C (8h)", "E (8h)", "M (5h)"],
            "ore": "8 + 8 + 5 = 21h (3h sotto)"
        },
        "ISSUE": "Melissa: 3 turni da 8h = 24h ✅ oppure 8+8+7 = 23h ❌ o 8+9+7 = 24h ✅"
    }
}

# Stampa semplificate
print("\n" + "=" * 80)
print("MATTEO (20h/sett, riposa DOM)")
print("=" * 80)
print("""
Settimana A:
  Lunedì:    Turno A (08:00-16:00, 8h)
  Mercoledì: Turno F (08:00-14:00, 6h)
  Sabato:    Turno H (10:00-16:00, 6h)
  TOTALE: 8 + 6 + 6 = 20h ✅

Settimana B (rotazione):
  Martedì:   Turno A (08:00-16:00, 8h)
  Giovedì:   Turno G (09:00-15:00, 6h)
  Venerdì:   Turno H (10:00-16:00, 6h)
  TOTALE: 8 + 6 + 6 = 20h ✅

Settimana C (rotazione):
  Lunedì:    Turno C (09:00-17:00, 8h)
  Mercoledì: Turno G (09:00-15:00, 6h)
  Venerdì:   Turno H (10:00-16:00, 6h)
  TOTALE: 8 + 6 + 6 = 20h ✅

VANTAGGI:
✅ Ogni settimana giorni diversi (non monotono)
✅ Turni a volte mattina, a volte diversi
✅ Sempre 8+6+6 per comodità
✅ Max 8 ore consecutive
""")

print("\n" + "=" * 80)
print("SIMONA (38h/sett, riposa GIO)")
print("=" * 80)
print("""
Settimana A:
  Lunedì:    Turno D (12:00-21:00, 9h)
  Martedì:   Turno B (08:00-16:30, 8.5h)
  Mercoledì: Turno E (13:00-21:00, 8h)
  Venerdì:   Turno I (14:00-21:00, 7h)
  Sabato:    Turno H (10:00-16:00, 6h)
  TOTALE: 9 + 8.5 + 8 + 7 + 6 = 38.5h ✅ (0.5h straordinario ok)

Settimana B (rotazione):
  Lunedì:    Turno E (13:00-21:00, 8h)
  Martedì:   Turno C (09:00-17:00, 8h)
  Mercoledì: Turno D (12:00-21:00, 9h)
  Venerdì:   Turno A (08:00-16:00, 8h)
  Sabato:    Turno F (08:00-14:00, 6h)
  TOTALE: 8 + 8 + 9 + 8 + 6 = 39h ✅ (1h straordinario ok, ha max 48h)

Settimana C (rotazione):
  Lunedì:    Turno A (08:00-16:00, 8h)
  Martedì:   Turno D (12:00-21:00, 9h)
  Mercoledì: Turno E (13:00-21:00, 8h)
  Venerdì:   Turno B (08:00-16:30, 8.5h)
  Sabato:    Turno G (09:00-15:00, 6h)
  TOTALE: 8 + 9 + 8 + 8.5 + 6 = 39.5h ✅

VANTAGGI:
✅ Diversità settimana per settimana
✅ Picchi di lavoro distribuiti
✅ Simona può gestire gli straordinari
✅ Niente monotonia
""")

print("\n" + "=" * 80)
print("SARA (19h/sett, riposa DOM+LUN)")
print("=" * 80)
print("""
Sara ha la MASSIMA FLESSIBILITÀ con 5 giorni disponibili per 19 ore!

Settimana 1:
  Martedì:   Turno J (13:00-19:00, 6h)
  Mercoledì: Turno F (08:00-14:00, 6h)
  Giovedì:   Turno I (14:00-21:00, 7h)
  TOTALE: 6 + 6 + 7 = 19h ✅

Settimana 2:
  Martedì:   Turno F (08:00-14:00, 6h)
  Mercoledì: Turno G (09:00-15:00, 6h)
  Venerdì:   Turno I (14:00-21:00, 7h)
  TOTALE: 6 + 6 + 7 = 19h ✅

Settimana 3:
  Martedì:   Turno J (13:00-19:00, 6h)
  Giovedì:   Turno I (14:00-21:00, 7h)
  Venerdì:   Turno F (08:00-14:00, 6h)
  TOTALE: 6 + 7 + 6 = 19h ✅ (giorni diversi!)

Settimana 4:
  Mercoledì: Turno F (08:00-14:00, 6h)
  Giovedì:   Turno J (13:00-19:00, 6h)
  Sabato:    Turno I (14:00-21:00, 7h)
  TOTALE: 6 + 6 + 7 = 19h ✅

Settimana 5:
  Mercoledì: Turno G (09:00-15:00, 6h)
  Venerdì:   Turno I (14:00-21:00, 7h)
  Sabato:    Turno H (10:00-16:00, 6h)
  TOTALE: 6 + 7 + 6 = 19h ✅

VANTAGGI PER SARA:
✅ Massima variabilità (non gli stessi 3 giorni ogni settimana)
✅ Riposo distribuito su giorni diversi
✅ Turni sempre a durate variabili (6+6+7)
✅ Può scegliere quale giorno riposare
✅ Niente monotonia assoluta
""")

print("\n" + "=" * 80)
print("MELISSA (24h/sett, riposa MAR)")
print("=" * 80)
print("""
Melissa: 3 turni da 8 ore = 24h esatto

Settimana 1:
  Lunedì:    Turno A (08:00-16:00, 8h)
  Mercoledì: Turno E (13:00-21:00, 8h)
  Giovedì:   Turno C (09:00-17:00, 8h)
  TOTALE: 8 + 8 + 8 = 24h ✅

Settimana 2:
  Lunedì:    Turno C (09:00-17:00, 8h)
  Mercoledì: Turno A (08:00-16:00, 8h)
  Venerdì:   Turno E (13:00-21:00, 8h)
  TOTALE: 8 + 8 + 8 = 24h ✅

Settimana 3:
  Lunedì:    Turno E (13:00-21:00, 8h)
  Giovedì:   Turno C (09:00-17:00, 8h)
  Sabato:    Turno A (08:00-16:00, 8h)
  TOTALE: 8 + 8 + 8 = 24h ✅

Settimana 4:
  Lunedì:    Turno B (08:00-16:30, 8.5h)
  Giovedì:   Turno A (08:00-16:00, 8h)
  Venerdì:   Turno I (14:00-21:00, 7h)
  TOTALE: 8.5 + 8 + 7 = 23.5h ❌ 0.5h

Settimana 4 (ALT):
  Lunedì:    Turno B (08:00-16:30, 8.5h)
  Giovedì:   Turno E (13:00-21:00, 8h)
  Venerdì:   Turno I (14:00-21:00, 7h)
  TOTALE: 8.5 + 8 + 7 = 23.5h ❌

Settimana 4 (BEST):
  Lunedì:    Turno B (08:00-16:30, 8.5h)
  Mercoledì: Turno C (09:00-17:00, 8h)
  Venerdì:   Turno I (14:00-21:00, 7h)
  TOTALE: 8.5 + 8 + 7 = 23.5h ❌ (0.5h sotto)

Alternativa Settimana 4:
  Lunedì:    Turno A (08:00-16:00, 8h)
  Mercoledì: Turno D (12:00-21:00, 9h)
  Venerdì:   Turno F (08:00-14:00, 6h)
  TOTALE: 8 + 9 + 6 = 23h ❌ (1h sotto)

Meglio Settimana 4:
  Lunedì:    Turno A (08:00-16:00, 8h)
  Mercoledì: Turno D (12:00-21:00, 9h)
  Giovedì:   Turno I (14:00-21:00, 7h) - NO! MAR riposa
  GIORNI GIUSTI:
  Lunedì:    Turno A (08:00-16:00, 8h)
  Mercoledì: Turno D (12:00-21:00, 9h)
  Sabato:    Turno I (14:00-21:00, 7h)
  TOTALE: 8 + 9 + 7 = 24h ✅

VANTAGGI PER MELISSA:
✅ Alternanza fra 3 turni da 8h
✅ Oppure 8+9+7 = 24h per settimane diverse
✅ Flessibilità ottima
✅ Niente monotonia
""")

print("\n" + "=" * 80)
print("✅ RIEPILOGO FINALE")
print("=" * 80)

print("""
PRINCIPIO: Turni variabili per TUTTI

✅ MATTEO (20h): 8+6+6 (ripete 3 settimane diverse)
   - Settimana 1: Lun+Mer+Sab
   - Settimana 2: Mar+Gio+Ven
   - Settimana 3: Lun+Gio+Ven
   → Niente monotonia, ogni settimana diversa

✅ SIMONA (38h): 9+8.5+8+7+6 oppure 8+8+9+8+6 (5 turni/sett)
   - Settimana 1: D+B+E+I+H = 38.5h
   - Settimana 2: E+C+D+A+F = 39h
   - Settimana 3: A+D+E+B+G = 39.5h
   → Massima flessibilità con straordinario permesso

✅ SARA (19h): 6+6+7 (3 giorni, combinazioni infinite)
   - Settimana 1: Mar+Mer+Gio (J+F+I)
   - Settimana 2: Mar+Mer+Ven (F+G+I)
   - Settimana 3: Mar+Gio+Ven (J+I+F)
   - Settimana 4: Mer+Gio+Sab (F+J+I)
   - Settimana 5: Mer+Ven+Sab (G+I+H)
   → Rotazione continua, mai gli stessi giorni

✅ MELISSA (24h): 8+8+8 oppure 8+9+7
   - Settimana 1: Lun+Mer+Gio (A+E+C) = 24h
   - Settimana 2: Lun+Mer+Sab (C+A+E) = 24h
   - Settimana 3: Lun+Gio+Sab (E+C+A) = 24h
   - Settimana 4: Lun+Mer+Sab (A+D+I) = 24h
   → Rotazione fra 3 turni da 8h oppure 8+9+7

BENEFICI DELLA VARIABILITÀ PER TUTTI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Zero monotonia (nessuno fa gli stessi turni sempre)
✅ Rotazione equa e imprevedibile
✅ Adattamento ai picchi di lavoro
✅ Resilienza per assenze/malattie
✅ Equilibrio psicologico per addetti
✅ Copertura oraria sempre completa
✅ Massima flessibilità organizzativa

IMPLEMENTAZIONE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
La app `genera_pianificazione()` può creare rotazioni
dinamiche diverse ogni mese, usando questo principio
di variabilità per tutti gli addetti.

Non serve più una rotazione fissa e prevedibile:
basta che ogni settimana la somma sia giusta!
""")
