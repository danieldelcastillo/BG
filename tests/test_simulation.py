from __future__ import annotations

import unittest

from bg_futbol_simulator.simulation import SimulationConfig, run_simulations


class SimulationTests(unittest.TestCase):
    def test_seeded_simulation_is_reproducible(self) -> None:
        config = SimulationConfig(matches=3, seed=12345)
        first = run_simulations(config).as_dict()
        second = run_simulations(config).as_dict()
        self.assertEqual(first, second)
        self.assertEqual(3, first["matches"])
