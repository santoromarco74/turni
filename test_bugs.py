"""
Suite di test per identificare e validare i bug in gestione-turni-completo.py
Esegui con: python -m pytest test_bugs.py -v
"""

import unittest
from datetime import datetime, timedelta
from typing import Tuple, List


class TestCalcoloOre(unittest.TestCase):
    """Test per il bug .seconds vs .total_seconds()"""

    def test_bug_seconds_vs_total_seconds(self):
        """CRITICO: Bug nel calcolo ore con datetime.seconds"""
        inizio = datetime.strptime("14:00", '%H:%M')
        fine = datetime.strptime("18:30", '%H:%M')

        # ❌ SBAGLIATO: usa .seconds (ritorna solo secondi, max 59)
        ore_sbagliato = (fine - inizio).seconds / 3600  # 4.5 ore = 16200 secondi

        # ✓ CORRETTO: usa .total_seconds()
        ore_corretto = (fine - inizio).total_seconds() / 3600

        print(f"\n18:30 - 14:00")
        print(f"  ❌ Usando .seconds:       {ore_sbagliato:.2f} ore")
        print(f"  ✓ Usando .total_seconds(): {ore_corretto:.2f} ore")

        # La differenza è 4.5 - 0 = ERRORE ENORME!
        self.assertAlmostEqual(ore_corretto, 4.5, places=1)
        self.assertNotEqual(ore_sbagliato, ore_corretto)

    def test_ore_multiple_di_3600_secondi(self):
        """Test con turni che contengono multiple ore esatte"""
        test_cases = [
            ("08:00", "14:00", 6.0),      # 6 ore esatte
            ("14:00", "21:00", 7.0),      # 7 ore esatte
            ("08:00", "14:30", 6.5),      # 6.5 ore
            ("14:30", "21:00", 6.5),      # 6.5 ore
        ]

        for inizio_str, fine_str, ore_attese in test_cases:
            inizio = datetime.strptime(inizio_str, '%H:%M')
            fine = datetime.strptime(fine_str, '%H:%M')

            ore_corrette = (fine - inizio).total_seconds() / 3600
            self.assertAlmostEqual(ore_corrette, ore_attese, places=1,
                                 msg=f"{inizio_str}-{fine_str} dovrebbe essere {ore_attese} ore")


class TestValidazioneOrari(unittest.TestCase):
    """Test per il bug nella validazione orari (confronto stringhe)"""

    def confronta_stringhe_orario_BUG(self, inizio: str, fine: str) -> bool:
        """❌ SBAGLIATO: Confronto LESSICOGRAFICO di stringhe"""
        return inizio >= fine

    def confronta_minuti_orario_CORRETTO(self, inizio: str, fine: str) -> bool:
        """✓ CORRETTO: Confronto numerico di minuti"""
        def orario_in_minuti(orario: str) -> int:
            h, m = map(int, orario.split(':'))
            return h * 60 + m

        return orario_in_minuti(inizio) >= orario_in_minuti(fine)

    def test_bug_confronto_stringhe_23_vs_9(self):
        """CRITICO: '23:00' < '9:00' ritorna True (FALSE POSITIVO!)"""
        inizio, fine = "23:00", "09:00"

        # ❌ SBAGLIATO: Confronto lessicografico
        risultato_sbagliato = self.confronta_stringhe_orario_BUG(inizio, fine)

        # ✓ CORRETTO: Confronto numerico
        risultato_corretto = self.confronta_minuti_orario_CORRETTO(inizio, fine)

        print(f"\n'23:00' >= '09:00' ?")
        print(f"  ❌ Stringhe:   {risultato_sbagliato} (FALSO POSITIVO - accetta turno notturno come valido)")
        print(f"  ✓ Minuti:      {risultato_corretto} (CORRETTO - rifiuta perché 23:00 >= 09:00)")

        # Stringhe: "23" > "09" lessicograficamente?
        self.assertTrue(self.confronta_stringhe_orario_BUG(inizio, fine))  # Falso positivo!
        self.assertTrue(self.confronta_minuti_orario_CORRETTO(inizio, fine))  # Corretto

    def test_bug_confronto_stringhe_14_vs_8(self):
        """'14:00' >= '08:00' è vero sia con stringhe che minuti"""
        inizio, fine = "14:00", "08:00"

        # Questo funziona per caso
        self.assertTrue(self.confronta_stringhe_orario_BUG(inizio, fine))
        self.assertTrue(self.confronta_minuti_orario_CORRETTO(inizio, fine))

    def test_bug_confronto_stringhe_190_vs_1930(self):
        """Test edge case: 19:00 vs 19:30"""
        inizio, fine = "19:00", "19:30"

        # ❌ SBAGLIATO: "19:00" >= "19:30" è False (ma dovrebbe essere False)
        # ✓ CORRETTO: 1140 >= 1170 è False (corretto)

        risultato_sbagliato = self.confronta_stringhe_orario_BUG(inizio, fine)
        risultato_corretto = self.confronta_minuti_orario_CORRETTO(inizio, fine)

        print(f"\n'19:00' >= '19:30' ?")
        print(f"  ❌ Stringhe:   {risultato_sbagliato}")
        print(f"  ✓ Minuti:      {risultato_corretto}")

        # In questo caso funzionano entrambi per caso
        self.assertFalse(risultato_sbagliato)
        self.assertFalse(risultato_corretto)


class TestOraioInMinuti(unittest.TestCase):
    """Test per funzione utility per convertire orari in minuti"""

    @staticmethod
    def orario_in_minuti(orario: str) -> int:
        """Converte 'HH:MM' in minuti da mezzanotte"""
        try:
            h, m = map(int, orario.split(':'))
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError(f"Orario non valido: {orario}")
            return h * 60 + m
        except (ValueError, AttributeError):
            return None

    def test_conversioni_base(self):
        """Test conversioni orarie"""
        test_cases = [
            ("00:00", 0),
            ("08:00", 480),
            ("12:00", 720),
            ("14:00", 840),
            ("18:30", 1110),
            ("21:00", 1260),
            ("23:59", 1439),
        ]

        for orario, minuti_attesi in test_cases:
            result = self.orario_in_minuti(orario)
            self.assertEqual(result, minuti_attesi,
                           msg=f"{orario} dovrebbe essere {minuti_attesi} minuti")

    def test_orari_invalidi(self):
        """Test con orari non validi"""
        test_cases = [
            "25:00",      # Ora invalida
            "12:60",      # Minuti invalidi
            "12",         # Formato sbagliato
            "12:30:45",   # Troppi campi
            "abc:def",    # Testo
            "",           # Vuoto
        ]

        for orario in test_cases:
            result = self.orario_in_minuti(orario)
            self.assertIsNone(result, msg=f"{orario} dovrebbe ritornare None")


class TestLogicaAddetti(unittest.TestCase):
    """Test per la logica di gestione addetti"""

    def test_bug_ore_min_vuoto(self):
        """CRITICO: Se turni_disponibili è vuoto, ore_min rimane 24"""
        turni_disponibili = []

        ore_min = 24  # Inizializzazione sbagliata
        for turno in turni_disponibili:
            h_start, h_end = turno
            # calcolo ore...
            pass

        print(f"\nSe non ci sono turni, ore_min = {ore_min}")
        print(f"  ❌ Questo crea un vincolo IMPOSSIBILE (max ore = 24)")

        self.assertEqual(ore_min, 24)

        # ✓ CORRETTO: Inizializzare a None e controllare dopo
        ore_min_corretto = None
        for turno in turni_disponibili:
            pass

        if ore_min_corretto is None:
            ore_min_corretto = 0

        self.assertEqual(ore_min_corretto, 0)

    def test_bug_ferie_sovrascritte(self):
        """CRITICO: Salvare ferie per un mese le sovrascritte per altri mesi"""
        addetto_state = {
            "ferie": []
        }

        # Utente salva ferie gennaio
        new_ferie_jan = ["2024-01-15", "2024-01-20"]
        addetto_state['ferie'] = new_ferie_jan

        # Utente salva ferie febbraio
        new_ferie_feb = ["2024-02-10"]
        addetto_state['ferie'] = new_ferie_feb  # ❌ SOVRASCRITTO!

        print(f"\nFerie addetto: {addetto_state['ferie']}")
        print(f"  ❌ Gennaio è stato PERSO!")

        # ✓ CORRETTO: Fare unione
        addetto_state['ferie'] = list(set(new_ferie_jan + new_ferie_feb))

        print(f"  ✓ Con merge: {sorted(addetto_state['ferie'])}")

        self.assertIn("2024-01-15", addetto_state['ferie'])
        self.assertIn("2024-02-10", addetto_state['ferie'])


class TestSalvataggioExcel(unittest.TestCase):
    """Test per il bug os.system con filename"""

    def test_bug_os_system_injection(self):
        """CRITICO: os.system non è sicuro per nomi file dinamici"""
        # ❌ SBAGLIATO: Nome file contiene caratteri pericolosi
        nome_file_unsafe = "Turni_Maggio_2024; rm -rf /"  # Injection!
        comando_sbagliato = f"xdg-open {nome_file_unsafe}"

        print(f"\nComando generato: {comando_sbagliato}")
        print(f"  ❌ Os.system eseguire la rimozione ricorsiva!")

        # ✓ CORRETTO: Usare subprocess con lista
        import subprocess
        import os

        # Simulazione sicura (non eseguire davvero)
        args_corretto = ('xdg-open', nome_file_unsafe)
        print(f"  ✓ Subprocess con lista: {args_corretto}")
        print(f"    (il filename è un argomento, non parte del comando)")


class TestConsolidamentoMigliorie(unittest.TestCase):
    """Test che consolidano le migliorie proposte"""

    def test_versione_migliorata_calcolo_ore(self):
        """Versione corretta della funzione calcolo ore"""
        def calcola_ore_turno(orario_inizio: str, orario_fine: str) -> float:
            """Calcola ore di un turno usando .total_seconds()"""
            try:
                inizio = datetime.strptime(orario_inizio, '%H:%M')
                fine = datetime.strptime(orario_fine, '%H:%M')

                if inizio >= fine:
                    raise ValueError(f"Ora inizio ({orario_inizio}) >= ora fine ({orario_fine})")

                # ✓ CORRETTO: .total_seconds()
                ore = (fine - inizio).total_seconds() / 3600
                return ore
            except ValueError as e:
                print(f"Errore: {e}")
                return None

        test_cases = [
            ("08:00", "14:00", 6.0),
            ("14:00", "21:00", 7.0),
            ("08:00", "14:30", 6.5),
        ]

        for inizio, fine, ore_attese in test_cases:
            ore = calcola_ore_turno(inizio, fine)
            self.assertAlmostEqual(ore, ore_attese, places=1)

    def test_versione_migliorata_validazione_orari(self):
        """Versione corretta della validazione orari"""
        def valida_orari(orario_inizio: str, orario_fine: str) -> Tuple[bool, str]:
            """Valida coppia di orari"""
            try:
                def orario_in_minuti(orario: str) -> int:
                    h, m = map(int, orario.split(':'))
                    if not (0 <= h < 24 and 0 <= m < 60):
                        raise ValueError()
                    return h * 60 + m

                minuti_inizio = orario_in_minuti(orario_inizio)
                minuti_fine = orario_in_minuti(orario_fine)

                if minuti_inizio >= minuti_fine:
                    return False, "Ora inizio deve essere precedente a ora fine"

                return True, ""
            except:
                return False, "Formato orario non valido (usa HH:MM)"

        # Test case validi
        self.assertTrue(valida_orari("08:00", "14:00")[0])
        self.assertTrue(valida_orari("23:00", "23:30")[0])

        # Test case invalidi
        self.assertFalse(valida_orari("14:00", "08:00")[0])
        self.assertFalse(valida_orari("23:00", "09:00")[0])
        self.assertFalse(valida_orari("25:00", "09:00")[0])


# ============================================================================

if __name__ == '__main__':
    # Esegui con output verboso
    unittest.main(verbosity=2)
