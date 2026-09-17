from io import StringIO
import unittest

from bg_futbol_simulator.game_state import Team
from bg_futbol_simulator.interactive import _write_summary_report
from bg_futbol_simulator.statistics import SimulationStatistics


class InteractiveReportTests(unittest.TestCase):
    def test_summary_report_has_totals_and_averages_without_turn_trace(self) -> None:
        statistics = SimulationStatistics(
            matches=2,
            total_goals=3,
            total_bot_goals_from_pressure=1,
            total_cr_draws=4,
        )
        output = StringIO()

        _write_summary_report(
            output,
            statistics,
            Team(15, 15, 10),
            Team(15, 16, 9),
            "agresivo",
        )

        report = output.getvalue()
        self.assertIn("Partidos simulados: **2**", report)
        self.assertIn("| Goles del jugador | **3** | **1.50** |", report)
        self.assertIn("| CR robadas | **4** | **2.00** |", report)
        self.assertNotIn("Turno 1", report)
