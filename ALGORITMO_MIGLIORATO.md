# Algoritmo di Assegnazione Turni - Miglioramenti

## Data: 2025-10-22

## Panoramica

L'algoritmo di assegnazione turni è stato completamente rivisitato per garantire maggiore efficienza, trasparenza e qualità delle soluzioni generate.

---

## Problemi dell'Algoritmo Precedente

### 1. **Approccio Randomico**
- Utilizzava fino a 25 tentativi casuali
- Non garantiva soluzioni ottimali
- Risultati imprevedibili e non riproducibili

### 2. **Copertura Oraria Incompleta**
- Poteva lasciare buchi nella copertura dell'orario del negozio
- Nessuna strategia sistematica per riempire le lacune

### 3. **Distribuzione Non Equa**
- Scarso bilanciamento delle ore tra gli addetti
- Alcuni addetti potevano essere sovraccaricati mentre altri sottoutilizzati

### 4. **Punteggi Complessi**
- Logica di scoring difficile da comprendere e debuggare
- Pesature arbitrarie senza chiara giustificazione

### 5. **Mancanza di Trasparenza**
- Logging minimo
- Difficile capire perché certe decisioni venivano prese

---

## Nuove Caratteristiche dell'Algoritmo Ottimizzato

### 1. **Pre-Validazione delle Risorse**

```python
def _conta_giorni_lavorativi(self, anno, mese)
def _conta_giorni_disponibili(self, nome, anno, mese)
```

**Benefici:**
- Calcola in anticipo se le risorse sono sufficienti
- Avverte l'utente se la pianificazione potrebbe essere impossibile
- Fornisce metriche chiare (ore necessarie vs ore disponibili)

**Output esempio:**
```
=== PRE-VALIDAZIONE RISORSE ===
- Matteo: 25 giorni disponibili, max 176.0 ore
- Simona: 26 giorni disponibili, max 208.0 ore
Ore necessarie totali: 377.0
Ore disponibili totali: 728.0
✓ Risorse sufficienti (surplus: 351.0 ore)
```

### 2. **Sistema di Priorità Dinamiche**

```python
def _calcola_disponibilita_addetti(self, data, ore_assegnate, ...)
```

**Criteri di priorità:**
- **Bilanciamento carico**: chi ha lavorato meno ha priorità maggiore
- **Capacità straordinari**: bonus per chi può fare ore extra
- **Equilibrio mattina/pomeriggio**: penalità per sbilanciamenti
- **Turni recenti**: evita ripetizioni dello stesso turno

**Formula priorità:**
```
priorità_base = 100 - (ore_lavorate / ore_contratto * 100)
priorità += 10 se può_fare_straordinari
priorità -= 2 * |turni_mattina - turni_pomeriggio|
```

### 3. **Algoritmo Greedy Intelligente con Strategie Multiple**

```python
def _assegna_turni_giorno_ottimizzato(self, ...)
```

**Tre strategie di assegnazione:**

1. **Priorità Copertura**: Usa turni più lunghi per massimizzare copertura rapida
2. **Priorità Continuità**: Assegna turni in ordine cronologico per evitare buchi
3. **Priorità Bilanciamento**: Alterna turni mattina/pomeriggio per equità

**Processo:**
- Prova ogni strategia in sequenza
- Si ferma alla prima che fornisce copertura completa
- Se nessuna funziona, usa la migliore soluzione parziale

### 4. **Sistema di Scoring Trasparente**

```python
def _trova_miglior_assegnazione_per_buco(self, ...)
```

**Calcolo score:**
```
score = minuti_copertura_buco          # Base: quanto copriamo
      + priorità_addetto               # Bilanciamento carico
      - penalità_ripetizione * 10      # Evita monotonia
      + bonus_inizio_buco (20)         # Preferisce inizio preciso
```

**Penalità ripetizione quadratica:**
```python
penalità = count_ripetizioni²
```
Esempio:
- 1 ripetizione = penalità 1
- 2 ripetizioni = penalità 4
- 3 ripetizioni = penalità 9

### 5. **Logging Dettagliato e Strutturato**

**Livelli di output:**

**Pre-validazione:**
```
======================================================================
GENERAZIONE CALENDARIO - NOVEMBRE 2025
======================================================================
```

**Per ogni giorno:**
```
──────────────────────────────────────────────────────────────────────
Giorno  1 (Lun 01/11/2025)
──────────────────────────────────────────────────────────────────────
  ✓ Simona         : Disponibile (priorità: 110.0, ore residue: 48.0h)
  - Sara           : RIPOSO SETTIMANALE
```

**Assegnazione turni:**
```
  ✓ Soluzione trovata con strategia: priorita_copertura
  ✓ Simona          → 08:00-14:30 (6.5h) [Tot: 6.5h]
  ✓ Matteo          → 14:30-21:00 (6.5h) [Tot: 13.0h]
```

**Riepilogo finale:**
```
======================================================================
RIEPILOGO FINALE
======================================================================

✓ Matteo         : 176.0h /  44h max
   Contratto: 20h | Mattina: 8 | Pomeriggio: 12
   Stato: Straordinario (+156.0h)

✓ Simona         : 195.0h /  48h max
   Contratto: 38h | Mattina: 15 | Pomeriggio: 15
   Stato: Straordinario (+157.0h)
```

### 6. **Metodi di Supporto Modulari**

Ogni funzione ha una responsabilità specifica:

| Metodo | Responsabilità |
|--------|---------------|
| `_conta_giorni_lavorativi()` | Conta giorni non festivi |
| `_conta_giorni_disponibili()` | Conta disponibilità per addetto |
| `_calcola_ore_turno()` | Calcola durata turno |
| `_calcola_disponibilita_addetti()` | Valuta disponibilità con priorità |
| `_get_turni_recenti()` | Estrae storico turni recenti |
| `_trova_primo_buco()` | Identifica lacune copertura |
| `_trova_miglior_assegnazione_per_buco()` | Seleziona migliore addetto-turno |
| `_penalita_ripetizione_turno()` | Calcola penalità monotonia |
| `_orario_in_minuti()` | Conversione formato orario |
| `_aggiorna_copertura()` | Marca minuti coperti |
| `_verifica_copertura_completa()` | Valida copertura totale |
| `_stampa_riepilogo_finale()` | Output riepilogo formattato |

---

## Vantaggi del Nuovo Algoritmo

### ✅ **Deterministico e Riproducibile**
- A parità di input, produce sempre lo stesso output
- Facilita il debugging e i test

### ✅ **Maggiore Copertura**
- Strategie multiple aumentano le probabilità di copertura completa
- Rileva e segnala chiaramente eventuali buchi

### ✅ **Equità e Bilanciamento**
- Distribuzione equa delle ore tra gli addetti
- Equilibrio tra turni mattina e pomeriggio
- Varietà nei turni assegnati

### ✅ **Trasparenza**
- Logging dettagliato di ogni decisione
- Facile capire perché un addetto è stato scelto
- Metriche chiare per valutare la qualità

### ✅ **Rispetto Rigoroso dei Vincoli**
- Controlli multipli per ore massime
- Rispetto assoluto di ferie e riposi
- Validazione pre e post assegnazione

### ✅ **Manutenibilità**
- Codice modulare e ben documentato
- Ogni metodo ha una responsabilità singola
- Facile estendere con nuove funzionalità

---

## Complessità Computazionale

### Algoritmo Precedente
- **O(k × n × m)** dove:
  - k = tentativi (max 25)
  - n = numero addetti
  - m = numero turni
- Tentativo randomico non garantisce ottimalità

### Nuovo Algoritmo
- **O(s × d × n × m)** dove:
  - s = strategie (3)
  - d = giorni del mese (~30)
  - n = numero addetti
  - m = numero turni
- Approccio greedy deterministico
- Complessità lineare per giorno
- Più efficiente e prevedibile

---

## Possibili Estensioni Future

### 1. **Algoritmi Avanzati**
- Backtracking completo per garantire ottimalità globale
- Programmazione dinamica per ottimizzazione multi-giorno
- Algoritmi genetici per scenari complessi

### 2. **Vincoli Aggiuntivi**
- Preferenze personali degli addetti
- Vincoli di competenze (cassa, scaffali, ecc.)
- Pause obbligatorie e turni notturni

### 3. **Machine Learning**
- Apprendimento da pianificazioni passate
- Predizione di conflitti e problemi
- Suggerimenti automatici di miglioramento

### 4. **Interfaccia Migliorata**
- Visualizzazione grafica dell'algoritmo in azione
- Confronto tra diverse soluzioni
- Modifica manuale con validazione automatica

---

## Test e Validazione

### Test Consigliati

1. **Test con risorse scarse**: Verificare comportamento con pochi addetti
2. **Test con molte ferie**: Validare gestione vincoli complessi
3. **Test bilanciamento**: Confermare equità distribuzione ore
4. **Test copertura**: Assicurare copertura completa 08:00-21:00
5. **Test ripetibilità**: Stessi input → stesso output

### Metriche di Qualità

- **Copertura**: % minuti coperti / minuti totali
- **Equità**: Deviazione standard ore tra addetti
- **Varietà**: Numero turni unici per addetto
- **Efficienza**: Tempo di esecuzione
- **Validità**: Rispetto vincoli hard (ore max, riposi)

---

## Conclusioni

L'algoritmo ottimizzato rappresenta un significativo miglioramento rispetto alla versione precedente:

- ✅ Maggiore qualità delle soluzioni
- ✅ Migliore esperienza utente con logging dettagliato
- ✅ Codice più manutenibile e testabile
- ✅ Base solida per future estensioni

L'approccio modulare e ben documentato facilita la comprensione e la modifica del comportamento dell'algoritmo secondo le esigenze specifiche del supermercato.
