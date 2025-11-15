# Gestione Turni - Sistema di Pianificazione Turni Supermercato

Un'applicazione Python con interfaccia grafica Tkinter per la gestione automatica dei turni di lavoro in un supermercato.

## 📋 Caratteristiche

- **Gestione Addetti**: Aggiungi, modifica e gestisci i dipendenti con loro vincoli orari
- **Gestione Turni**: Definisci i turni disponibili con orari flessibili
- **Ferie e Riposi**: Assegna ferie, giorni di riposo settimanali e gestisci assenze
- **Generazione Automatica**: Pianifica turni mensili rispettando vincoli legali e contrattuali
- **Esportazione Excel**: Genera calendari Excel formattati e colorati
- **Statistiche**: Analizza ore lavorate, straordinari, e copertura oraria

## 🚀 Avvio Rapido

### Prerequisiti

```bash
python3 -m pip install pandas openpyxl
```

> **Nota**: Tkinter è incluso in Python su Windows/Mac. Su Linux: `sudo apt install python3-tk`

### Esecuzione

```bash
python3 gestione-turni-completo.py
```

o la versione refactorizzata:

```bash
python3 gestione-turni-modificato.py
```

## 📁 Struttura File

```
turni/
├── gestione-turni-completo.py          # Versione base (1151 linee)
├── gestione-turni-modificato.py        # Versione refactorizzata (1723 linee)
├── gestione_turni_utilities.py         # Modulo utility NUOVO ✓
├── dati_turni.json                     # File di configurazione
├── test_bugs.py                        # Suite di test per bug identification
├── MIGLIORAMENTI_E_BUG_FIXES.md        # Analisi dettagliata di bug e fix
└── README.md                           # Questo file
```

## 🔴 BUG IDENTIFICATI E CORREZIONI

### Bug Critici Trovati

| Bug | Tipo | Gravità | Stato |
|-----|------|---------|-------|
| `.seconds` vs `.total_seconds()` | Calcolo ore | ⚠️⚠️⚠️ | ✓ Identificato |
| Validazione orari (stringhe vs minuti) | Validazione | ⚠️⚠️ | ✓ Identificato |
| Sovrascrittura ferie | Logica dati | ⚠️⚠️⚠️ | ✓ Identificato |
| `ore_min` non inizializzato | Edge case | ⚠️⚠️⚠️ | ✓ Identificato |
| `os.system` injection | Security | ⚠️⚠️ | ✓ Identificato |
| Import tardivi | Struttura | ⚠️⚠️ | ✓ Identificato |
| Parsing locale problematico | Localizzazione | ⚠️⚠️ | ✓ Identificato |

**Per dettagli tecnici**: Vedi [MIGLIORAMENTI_E_BUG_FIXES.md](./MIGLIORAMENTI_E_BUG_FIXES.md)

## ✅ Modulo Utility Aggiunto

È stato creato **`gestione_turni_utilities.py`** con funzioni corrette e sicure:

### Funzioni Disponibili

#### Gestione Orari
```python
from gestione_turni_utilities import (
    orario_in_minuti,
    minuti_in_orario,
    valida_orari,
    calcola_ore_turno
)

# Convertire orario in minuti da mezzanotte
minuti = orario_in_minuti("14:30")  # → 870

# Convertire minuti in orario
orario = minuti_in_orario(870)  # → "14:30"

# Validare orari
valido, msg = valida_orari("08:00", "14:00")  # → (True, "")
valido, msg = valida_orari("14:00", "08:00")  # → (False, "Ora inizio >= ora fine")

# Calcolare ore di un turno (✓ CORRETTO: usa .total_seconds())
ore = calcola_ore_turno("14:00", "18:30")  # → 4.5
```

#### Gestione Dati
```python
from gestione_turni_utilities import (
    carica_dati_sicuro,
    salva_dati_sicuro,
    aggiungi_ferie
)

# Carica dati con gestione errori
dati = carica_dati_sicuro("dati_turni.json")

# Salva dati sicuramente
salva_dati_sicuro("dati_turni.json", dati)

# Merge ferie (senza sovrascritture)
ferie_nuovo = aggiungi_ferie(
    ferie_esistenti,
    ["2024-02-10", "2024-02-11"]
)
```

#### Turni
```python
from gestione_turni_utilities import (
    calcola_orario_minimo_turni,
    calcola_orario_massimo_turni
)

# Trova turno minimo e massimo
ore_min = calcola_orario_minimo_turni(turni)
ore_max = calcola_orario_massimo_turni(turni)
```

### Test del Modulo

```bash
python3 gestione_turni_utilities.py
# Output: Tutti i test sono passati! ✓
```

## 🧪 Esecuzione Test

Sono inclusi test unitari che identificano e dimostrano i bug:

```bash
python3 test_bugs.py
```

Output:
```
test_bug_seconds_vs_total_seconds ... [INFO BUG DEMONSTRATIONS]
test_bug_confronto_stringhe_23_vs_9 ... [EDGE CASE FOUND]
test_bug_ferie_sovrascritte ... [DATA LOSS DEMONSTRATED]
...
Ran 12 tests - PASSED ✓
```

## 📊 Analisi Comparativa

### versione-completo.py vs versione-modificato.py

| Aspetto | v1 | v2 |
|---------|----|----|
| Linee | 1151 | 1723 |
| Helper functions | ❌ | ✓ |
| DRY score | Bassa | Media |
| Complessità ciclomatica | Alta | Media |
| Error handling | Pessima | Media |
| Security | Bassa | Media |
| Type hints | ❌ | ❌ |
| Test coverage | 0% | 0% |

**Risultato**: v2 è migliore ma ha ancora 9 bug critici non risolti.

## 🛠️ Roadmap di Miglioramento

### Fase 1: BUG FIX (Prioritario)
- [ ] Sostituire `.seconds` con `.total_seconds()` (8 linee)
- [ ] Usare `valida_orari()` dalle utility
- [ ] Usare `aggiungi_ferie()` per merge
- [ ] Usare `calcola_orario_minimo_turni()` per ore_min

### Fase 2: SECURITY (2-3 settimane)
- [ ] Sostituire `os.system()` con `subprocess.run()`
- [ ] Spostare import in cima al file
- [ ] Semplificare parsing locale

### Fase 3: REFACTORING (1-2 mesi)
- [ ] Aggiungere type hints a tutte le funzioni
- [ ] Separare UI da logica business
- [ ] Aggiungere logging completo
- [ ] Coprire 80% con unit test
- [ ] Documentare con docstring

## 📝 File di Configurazione: dati_turni.json

```json
{
  "addetti": {
    "Matteo": {
      "ore_contratto": 20,
      "ore_max": 44,
      "straordinario": true,
      "giorni_riposo": [0],
      "ferie": []
    },
    "Simona": {
      "ore_contratto": 38,
      "ore_max": 48,
      "straordinario": true,
      "giorni_riposo": [4],
      "ferie": []
    }
  },
  "turni": [
    ["08:00", "14:00"],
    ["08:00", "14:30"],
    ["14:00", "21:00"],
    ["14:30", "21:00"],
    ["14:00", "18:30"],
    ["14:00", "19:00"]
  ]
}
```

**Campi per addetto**:
- `ore_contratto`: Ore settimanali previste da contratto
- `ore_max`: Ore massime consentite (incluso straordinario)
- `straordinario`: Se consentito
- `giorni_riposo`: Giorni settimanali fissi di riposo (0=lunedì, 6=domennica)
- `ferie`: Array di date in formato "YYYY-MM-DD"

**Campi per turno**:
- Tupla `[inizio, fine]` in formato "HH:MM"

## 🔍 Esempi di Utilizzo

### Aggiungere un addetto

1. Clicca "Gestione Addetti"
2. Inserisci nome
3. Specifica ore contratto, ore max
4. Seleziona giorni di riposo settimanali
5. Salva

### Definire turni

1. Clicca "Gestione Turni"
2. Aggiungi turno con orari validati
3. Rimuovi turni non più usati
4. Salva

### Generare pianificazione

1. Clicca "Genera Pianificazione"
2. Seleziona mese e anno
3. Sistema genera automaticamente
4. Visualizza risultato
5. Esporta in Excel

### Esportare in Excel

1. Dopo generazione pianificazione
2. File salvato su Desktop come `Turni_Maggio_2024.xlsx`
3. Apribile con Excel, Calc, Sheets

## 📈 Output Excel

Il file Excel generato contiene:

- **Header**: Nome addetto, ore previste, ore max
- **Calendario**: Giorni con turni assegnati
- **Colori**:
  - 🟦 Azzurro: Header
  - 🟩 Verde: Turni mattina
  - 🟨 Giallo: Ferie
  - 🟥 Rosso: Festivi
  - ⬜ Grigio: Riposo

## 💡 Suggerimenti per il Miglioramento

### Breve Termine
1. **Usare le utility**: Importare da `gestione_turni_utilities.py`
2. **Aggiungere validazione**: Input form non è robusto
3. **Migliorare messaggi errore**: Attualmente vago

### Medio Termine
1. **API REST**: Trasformare in web app con Flask/FastAPI
2. **Database**: Sostituire JSON con SQLite/PostgreSQL
3. **Sincronizzazione**: Condividere calendario con cloud

### Lungo Termine
1. **App Mobile**: React Native per smartphone
2. **ML Optimization**: Usare algoritmi di ottimizzazione avanzati
3. **Real-time**: WebSocket per aggiornamenti live

## 🐛 Segnalazione Bug

Se trovi altri bug:

1. Leggi [MIGLIORAMENTI_E_BUG_FIXES.md](./MIGLIORAMENTI_E_BUG_FIXES.md)
2. Esegui test: `python3 test_bugs.py`
3. Apri una issue con:
   - Descrizione del problema
   - Steps per riprodurre
   - Output atteso vs reale

## 📄 Licenza

Non specificata - Contatta l'autore

## ✍️ Autore

santoromarco74 - Versioni originali e refactoring

---

**Ultimo aggiornamento**: Novembre 2025
**Versione corrente**: v2 (gestione-turni-modificato.py)
**Test coverage**: 0% (WIP)
**Status**: ⚠️ Beta - Bug critici identificati, fix proposti

