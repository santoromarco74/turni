# Sistema di Gestione Turni Supermercato

Sistema completo per la pianificazione automatica dei turni di lavoro in un supermercato, con interfaccia grafica Tkinter ed export Excel.

## 🚀 Caratteristiche Principali

- **Gestione Addetti**: Configurazione completa di dipendenti, ore contrattuali, limiti e straordinari
- **Pianificazione Turni**: Definizione flessibile dei turni disponibili (mattina, pomeriggio, sera)
- **Ferie e Riposi**: Gestione calendari individuali e riposi settimanali
- **Generazione Automatica**: Algoritmo intelligente per la pianificazione mensile
- **Export Excel**: Esportazione formattata con codici colore
- **Statistiche**: Report dettagliati su ore lavorate, turni e conformità contrattuale

## 📋 Requisiti

```bash
pip install tkinter pandas openpyxl
```

**Requisiti di sistema:**
- Python 3.7+
- tkinter (solitamente incluso con Python)
- pandas >= 1.0.0
- openpyxl >= 3.0.0

## 🎯 Utilizzo

### Avvio dell'applicazione

```bash
python gestione-turni-completo.py
```

### Flusso di lavoro tipico

1. **Gestione Addetti**
   - Aggiungi gli addetti del supermercato
   - Configura ore contrattuali e limiti massimi
   - Indica se possono fare straordinari

2. **Gestione Turni**
   - Definisci gli orari dei turni (es. 08:00-14:00, 14:00-21:00)
   - I turni devono coprire l'orario di apertura del negozio (08:00-21:00)

3. **Gestione Ferie e Riposi**
   - Imposta i giorni di riposo settimanali per ogni addetto
   - Pianifica le ferie mensili

4. **Genera Pianificazione**
   - Seleziona mese e anno
   - L'algoritmo genera automaticamente il calendario ottimizzato
   - Viene creato un file Excel con la pianificazione

5. **Visualizza Statistiche**
   - Analizza le ore lavorate
   - Verifica il rispetto dei limiti contrattuali
   - Monitora l'equità nella distribuzione dei turni

## 🧠 Algoritmo di Assegnazione

L'algoritmo ottimizzato utilizza un approccio **greedy con priorità dinamiche** e **strategie multiple**:

### Caratteristiche principali:

✅ **Pre-validazione risorse** - Verifica disponibilità prima della pianificazione
✅ **Priorità dinamiche** - Bilancia automaticamente il carico di lavoro
✅ **Strategie multiple** - Prova diversi approcci per trovare la soluzione migliore
✅ **Copertura garantita** - Assicura copertura completa dell'orario 08:00-21:00
✅ **Rispetto vincoli** - Rispetta ore massime, ferie, riposi
✅ **Logging dettagliato** - Output trasparente di ogni decisione

### Strategie di assegnazione:

1. **Priorità Copertura**: Massimizza la copertura usando turni più lunghi
2. **Priorità Continuità**: Minimizza buchi temporali nella giornata
3. **Priorità Bilanciamento**: Alterna turni mattina/pomeriggio per equità

Per maggiori dettagli sull'algoritmo, consultare [ALGORITMO_MIGLIORATO.md](ALGORITMO_MIGLIORATO.md)

## 📊 Output Excel

Il file Excel generato include:

- **Codici colore**:
  - 🟢 Verde chiaro: Turni mattina
  - 🟠 Arancione chiaro: Turni pomeriggio
  - 🔴 Rosso chiaro: Giorni festivi
  - 🟡 Giallo chiaro: Ferie
  - ⚪ Grigio chiaro: Riposi
  - 🔵 Rosa chiaro: Weekend

- **Formato**: Una riga per giorno, una colonna per addetto
- **Informazioni**: Orari turni (es. "08:00-14:30"), ferie, riposi

## 📁 Struttura File

```
turni/
├── gestione-turni-completo.py      # Applicazione principale (versione ottimizzata)
├── gestione-turni-modificato.py    # Versione precedente
├── dati_turni.json                  # Dati persistenti (addetti, turni, ferie)
├── README.md                        # Questo file
├── ALGORITMO_MIGLIORATO.md         # Documentazione algoritmo
└── turni_YYYY_MM.xlsx              # File Excel generati
```

## 🔧 Configurazione

### Orari del Supermercato

Modificare nel codice:

```python
self.orario_apertura = "08:00"
self.orario_chiusura = "21:00"
```

### Giorni Festivi

Modificare la lista:

```python
self.giorni_festivi = [
    "01-01",  # Capodanno
    "20-04",  # 20 aprile
    "01-05",  # 1 maggio
    "25-12",  # Natale
    "26-12"   # Santo Stefano
]
```

### Colori Excel

Personalizzare i colori nel dizionario `self.colori`.

## 📈 Esempio di Utilizzo

### Scenario: Supermercato con 4 addetti

**Addetti configurati:**
- **Matteo**: 20h/settimana (contratto), max 44h, straordinari: sì, riposo: lunedì
- **Simona**: 38h/settimana, max 48h, straordinari: sì, riposo: venerdì
- **Sara**: 19h/settimana, max 19h, straordinari: no, riposo: martedì, giovedì, sabato, domenica
- **Melissa**: 24h/settimana, max 44h, straordinari: sì, riposo: mercoledì

**Turni disponibili:**
- 08:00-14:00 (6h)
- 08:00-14:30 (6.5h)
- 14:00-21:00 (7h)
- 14:30-21:00 (6.5h)
- 14:00-18:30 (4.5h)
- 14:00-19:00 (5h)

**Risultato:**
L'algoritmo genera automaticamente un calendario mensile che:
- Copre tutto l'orario 08:00-21:00
- Rispetta i riposi settimanali
- Bilancia le ore tra gli addetti
- Alterna turni mattina/pomeriggio
- Rispetta i limiti orari

## 🐛 Risoluzione Problemi

### Problema: "Nessun addetto disponibile"
**Soluzione**: Verificare che ci siano addetti disponibili per quel giorno (controllare ferie e riposi)

### Problema: "Risorse insufficienti"
**Soluzione**: Aumentare ore massime degli addetti o ridurre le ferie

### Problema: "Copertura completa non possibile"
**Soluzione**:
- Aggiungere più turni che coprano le ore critiche
- Aumentare il numero di addetti
- Ridurre i giorni di riposo

### Problema: File Excel non si apre automaticamente
**Soluzione**: Il file viene comunque salvato nella directory corrente con nome `turni_YYYY_MM.xlsx`

## 🔄 Aggiornamenti Recenti

### v2.0 (2025-10-22) - Algoritmo Ottimizzato

- ✨ Nuovo algoritmo di assegnazione con strategie multiple
- ✨ Pre-validazione delle risorse disponibili
- ✨ Sistema di priorità dinamiche per bilanciamento carico
- ✨ Logging dettagliato e strutturato
- ✨ Codice modulare e manutenibile
- 🐛 Risolti problemi di copertura incompleta
- 🐛 Migliorata distribuzione equa delle ore
- 📚 Documentazione completa dell'algoritmo

### v1.0 - Versione Iniziale

- Gestione base addetti e turni
- Generazione calendario con approccio randomico
- Export Excel con formattazione

## 📝 Licenza

Progetto open source per uso interno ed educativo.

## 👥 Contributi

Per segnalare bug o proporre miglioramenti, creare una issue nel repository.

## 📞 Supporto

Per domande o supporto, consultare:
- [ALGORITMO_MIGLIORATO.md](ALGORITMO_MIGLIORATO.md) per dettagli tecnici
- Il codice sorgente è commentato e ben documentato

---

**Nota**: Questo sistema è stato progettato per supermercati di piccole-medie dimensioni. Per esigenze più complesse (turnazioni notturne, competenze specifiche, ecc.), potrebbe essere necessario personalizzare l'algoritmo.
