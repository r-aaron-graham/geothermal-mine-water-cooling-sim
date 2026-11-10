import unittest

from scheduler import BACKUP_COP, FLOW_LPS, INLET_C, JOBS, Job, simulate


class SchedulerTests(unittest.TestCase):
    def test_default_scenario_compares_equal_completed_work(self):
        fifo = simulate(JOBS, FLOW_LPS, INLET_C, False, BACKUP_COP)
        aware = simulate(JOBS, FLOW_LPS, INLET_C, True, BACKUP_COP)
        self.assertEqual(fifo["completed"], len(JOBS))
        self.assertEqual(aware["completed"], len(JOBS))
        self.assertEqual(aware["deadline_misses"], 0)
        self.assertLess(aware["kwh_per_completed_job"], fifo["kwh_per_completed_job"])

    def test_deadline_triggers_backup_cooling(self):
        result = simulate((Job("urgent", 0, 120, 0),), (0,), (16,), True, 3)
        self.assertEqual(result["completed"], 1)
        self.assertEqual(result["modeled_energy_kwh"], 160)
