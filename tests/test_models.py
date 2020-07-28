import datetime
import unittest

from docbrown.models import calculate_progress, PassedPhase


class ProgressCalculationTest(unittest.TestCase):
    def test_calculate_progress_for_known_process(self):
        now = datetime.datetime.now()
        phases = [
            PassedPhase('one', now - datetime.timedelta(minutes=5)),
            PassedPhase('two', now - datetime.timedelta(minutes=1, seconds=38)),
            PassedPhase('three', now - datetime.timedelta(seconds=3)),
        ]
        timings = {
            '__startup__': 1,
            'one': 200,
            'two': 93,
            'three': 12,
            'four': 60
        }
        progress = calculate_progress(phases, timings, now)
        self.assertEqual(progress.passed_phases, ['one', 'two', 'three'])
        self.assertEqual(progress.expected_phases, ['one', 'two', 'three', 'four'])
        self.assertEqual(progress.current_phase, 'three')
        self.assertEqual(progress.phase_progress, 25)
        self.assertEqual(progress.duration, 300)
        self.assertEqual(progress.expected_duration, 370)
        self.assertAlmostEqual(progress.progress, 80.87, places=1)

    def test_detect_stuck_phase(self):
        now = datetime.datetime.now()
        progress = calculate_progress(
            [PassedPhase('one', now - datetime.timedelta(seconds=10))],
            {'__startup__': 0, 'one': 5},
            now
        )
        self.assertEqual(progress.expected_duration, 10)
        self.assertEqual(progress.duration, 10)
        self.assertEqual(progress.is_stuck, True)

    def test_calculate_progress_for_unknown_phase(self):
        now = datetime.datetime.now()
        phases = [
            PassedPhase('one', now - datetime.timedelta(seconds=15)),
            PassedPhase('two', now - datetime.timedelta(seconds=7)),
        ]
        timings = {
            '__startup__': 0,
            'one': 3,
            'three': 4
        }
        progress = calculate_progress(phases, timings, now)
        self.assertEqual(progress.current_phase, 'two')
        self.assertEqual(progress.expected_duration, 19)

        phases = [
            PassedPhase('one', now - datetime.timedelta(seconds=15)),
            PassedPhase('two', now - datetime.timedelta(seconds=7)),
            PassedPhase('three', now - datetime.timedelta(seconds=3))
        ]
        timings = {
            '__startup__': 0,
            'one': 3,
            'three': 4
        }
        progress = calculate_progress(phases, timings, now)
        self.assertEqual(progress.current_phase, 'three')
        self.assertEqual(progress.expected_duration, 16)
