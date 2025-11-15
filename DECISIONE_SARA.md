# ⚠️ DECISIONE CRITICA: COME RISOLVERE IL PROBLEMA DI SARA

## SITUAZIONE

Sara ha vincoli molto restrittivi che rendono impossibile coprire il suo contratto di 19 ore/settimana con i turni attuali:

```
Ore contratto:         19 ore/settimana
Giorni disponibili:    SOLO martedì e giovedì (2 giorni!)
Ore necessarie/giorno: 19 ÷ 2 = 9.5 ore/giorno

Turni disponibili:
  - Turno D (12:00-21:00): 9 ore    ← Massimo possibile
  - Turno E (13:00-21:00): 8 ore    ← Non basta
```

**Impossibile coprire 19 ore in 2 giorni con turni massimi di 9 ore.**

---

## OPZIONI DISPONIBILI

### OPZIONE A: Modificare i giorni di riposo (⭐ CONSIGLIATA)

**Cambio richiesto:**
- ❌ Attualmente riposa: **Lunedì, Mercoledì, Venerdì, Sabato** (4 giorni)
- ✅ Proposto: **Domenica, Lunedì** (2 giorni)

**Risultato:**
- Giorni disponibili: **Martedì, Mercoledì, Giovedì, Venerdì, Sabato** (5 giorni)
- Ore/giorno: 19 ÷ 5 = **3.8 ore/giorno** ✅
- Turni realizzabili: Turno F (14:00-21:00, 7h) + Turno A/C (8h) + brevi

**Vantaggi:**
- ✅ Rispetta massimo 9 ore/giorno
- ✅ Facile da implementare
- ✅ Più equilibrato per Sara
- ✅ Niente doppi turni complessi

**Svantaggi:**
- ⚠️ Sara cambia routine di riposo
- ⚠️ Perde il riposo fisso mercoledì

**Esempio settimana:**
```
Lunedì:      Riposo (fisso)
Martedì:     Turno F (14:00-21:00, 7 ore)
Mercoledì:   Turno A (08:00-16:00, 8 ore)
Giovedì:     Turno E (13:00-21:00, 8 ore)
Venerdì:     Turno F (14:00-21:00, 7 ore) - NO, supera 19h!
Sabato:      Turno F (14:00-21:00, 7 ore) - NO!
Domenica:    Riposo (fisso)

Totale: 7 + 8 + 8 = 23h (troppo!)
```

**Aggiustamento:**
```
Lunedì:      Riposo (fisso)
Martedì:     Turno E (13:00-21:00, 8 ore)
Mercoledì:   Turno A (08:00-16:00, 8 ore)
Giovedì:     Turno F (14:00-21:00, 7 ore) - NO! 8+8+7=23h
Sabato:      Riposo
Domenica:    Riposo (fisso)

Finale:
Lunedì:      Riposo
Martedì:     Turno F (14:00-21:00, 7 ore)
Mercoledì:   Turno A (08:00-16:00, 8 ore)
Giovedì:     Turno F (14:00-21:00, 7 ore) - NO, 7+8+7=22h
Venerdì:     Turno A (08:00-16:00, 8 ore) - NO, 22h!
Sabato:      Riposo
Domenica:    Riposo

ALTERNATIVA:
Lunedì:      Riposo
Martedì:     Turno F (14:00-21:00, 7 ore)
Mercoledì:   Turno F (14:00-21:00, 7 ore) (BUT non ha riposo!)
Giovedì:     Turno F (14:00-21:00, 7 ore) - NO 21h!
Venerdì:     Turno A (08:00-16:00, 8 ore) - NO!
Sabato:      Riposo
Domenica:    Riposo

Soluzione funzionante:
Lunedì:      Riposo (fisso)
Martedì:     Turno F (14:00-21:00, 7 ore)
Mercoledì:   Turno A (08:00-16:00, 8 ore)
Giovedì:     Turno A (08:00-16:00, 8 ore) (ma ha riposo questo giorno!)
Venerdì:     Turno F (14:00-21:00, 7 ore) - Sopra! 7+8+8+7=30h
Sabato:      Riposo
Domenica:    Riposo (fisso)

Meglio:
Lunedì:      Riposo (fisso)
Martedì:     Turno D (12:00-21:00, 9 ore)
Mercoledì:   Turno A (08:00-16:00, 8 ore)
Giovedì:     Turno A (08:00-16:00, 8 ore) - NO, riposa questo giorno!
Venerdì:     Riposo
Sabato:      Riposo
Domenica:    Riposo (fisso)

Totale: 9+8 = 17h (sotto!)

Sara necessita di 19h in 5 giorni = 3.8h/giorno
Combinazioni possibili:
- 3 turni di 6-7 ore + riposo 2 giorni
- Esempio:
  - Martedì: 7h
  - Mercoledì: 6h
  - Giovedì: 6h
  - Venerdì: -
  - Sabato: -
  Total: 19h ✓

Con i turni disponibili:
- Turno F (14:00-21:00): 7h
- Turno A (08:00-16:00): 8h
- Turno B (08:00-16:30): 8.5h
- Turno C (09:00-17:00): 8h
- Turno E (13:00-21:00): 8h
- Turno D (12:00-21:00): 9h

Migliore:
- Martedì: Turno F (7h)
- Mercoledì: Turno A (8h)
- Giovedì: X (ha riposo!)
- Venerdì: Turno F (7h)
- Totale: 7+8+7 = 22h (sopra!)

O:
- Martedì: Turno F (7h)
- Mercoledì: Turno C (8h) - NO, 15h già
- Giovedì: Turno F (7h) - NO,  22h
- Sabato: Turno A (8h) - NO, 23h

Problema: con 5 giorni e media 3.8h/giorno, serve rotazione calibrata.

Turni più corti:
- Turno F: 7h (breve)
- Nient'altro sotto 8h!

SOLUZIONE: Aggiungere turni più corti!
- Turno G: 08:00-13:00 = 5h
- Turno H: 16:00-21:00 = 5h
- Turno I: 14:00-18:30 = 4.5h

Con questi:
- Martedì: Turno F (7h)
- Mercoledì: Turno G (5h)
- Giovedì: Turno F (7h)
- Sabato: - (riposo)
Total: 19h ✓ Con 3 giorni lavorati!
```

**CONCLUSIONE OPZIONE A**: Richiede anche di aggiungere turni brevi (5h) per essere effettiva.

---

### OPZIONE B: Permettere doppi turni nello stesso giorno

**Come funziona:**
- Un giorno Sara fa **2 turni separati** (es. mattina + pomeriggio)
- Secondo giorno fa **1 turno lungo**

**Esempio:**
```
Martedì:   Turno A (08:00-16:00, 8h) + Turno F (14:00-21:00, 7h)
           ⚠️ PROBLEMI:
           1. Sovrappone 14:00-16:00 (2 ore, non è gap!)
           2. Continuità: 08:00-21:00 = 13 ore di "presenza"
           3. Totale ore: 8+7 = 15 ore (ma con solo 2h di pausa è faticante)

Giovedì:   Turno A (08:00-16:00, 8h)
           Totale ore settimanale: 15+8 = 23h (sopra!)

Alternativa:
Martedì:   Turno A (08:00-14:00, 6h) + Turno D (12:00-21:00, 9h)
           ⚠️ PEGGIO: sovrapposizione 12:00-14:00 + totale 15h

O:
Martedì:   Turno B (08:00-16:30, 8.5h)
Giovedì:   Turno F (14:00-21:00, 7h) + Turno G (altro?)
           Non basta 15.5h, serve ancora 3.5h
```

**Vantaggi:**
- ✅ Mantiene i giorni di riposo di Sara
- ✅ Non serve modificare contratti

**Svantaggi:**
- ❌ Doppi turni sono faticanti (13-15 ore di presenza)
- ❌ Richiede coordinamento di break fra i due turni
- ❌ Non rispetta il principio di "max 9 ore consecutive"
- ❌ Difficile da gestire nella pratica

**Fattibilità**: ⚠️ **BASSA - Non consigliato**

---

### OPZIONE C: Ridurre le ore di contratto di Sara

**Cambio richiesto:**
- ❌ Attuale: Sara 19 ore/settimana
- ✅ Proposto: Sara 14 ore/settimana

**Risultato:**
- Con 2 giorni disponibili: 14 ÷ 2 = **7 ore/giorno** ✅
- Realizzabile con un solo turno di 7 ore per giorno

**Esempio settimana:**
```
Martedì:   Turno F (14:00-21:00, 7 ore)
Giovedì:   Turno F (14:00-21:00, 7 ore)
Totale:    14 ore ✓

Semplice, sostenibile, niente problemi.
```

**Vantaggi:**
- ✅ Massima semplicità
- ✅ Un solo turno per giorno
- ✅ Niente doppi turni
- ✅ Facile da pianificare

**Svantaggi:**
- ⚠️ Sara perde 5 ore/settimana di stipendio (-26%)
- ⚠️ Potrebbe non essere accettabile per Sara

**Fattibilità**: ✅ **MOLTO ALTA - Se accettabile per Sara**

---

## CONFRONTO QUICK

| Criterio | Opzione A | Opzione B | Opzione C |
|----------|-----------|-----------|-----------|
| **Implementazione** | Facile (cambia giorni riposo) | Complessa | Molto facile |
| **Fatica Sara** | Media | Alta (doppi turni) | Bassa |
| **Ore contratto** | Mantenuto 19h | Mantenuto 19h | Ridotto a 14h |
| **Semplifica** | No (richiede turni brevi) | No (doppi turni) | Sì (1 turno/giorno) |
| **Consigliato** | ⭐ Con turni brevi | ❌ No | ⭐⭐ Se Sara accetta |

---

## RACCOMANDAZIONE FINALE

### 1️⃣ **PRIMA SCELTA**: Opzione C (Ridurre a 14 ore)
- **Se Sara può accettare la riduzione di stipendio**
- Massima semplicità: 1 turno per giorno
- No complicazioni

### 2️⃣ **SECONDA SCELTA**: Opzione A (Cambiare giorni riposo) + Aggiungere turni brevi
- **Se Sara accetta diversi giorni di riposo**
- Richiede di aggiungere turni da 4-5 ore al file
- Più flessibile ma complesso

### 3️⃣ **SCONSIGLIATO**: Opzione B (Doppi turni)
- ❌ Troppo faticante
- ❌ Difficile da gestire

---

## ☑️ COSA FARE ADESSO

1. **Decidi quale opzione preferisci** (A, B o C)
2. **Comunica la decisione**
3. **Io aggiorno il file JSON** in base alla scelta

**Quale opzione scegli?**
- ✅ A) Modificare giorni di riposo (+ turni brevi)
- ✅ C) Ridurre contratto da 19 a 14 ore
- (B è sconsigliato)
