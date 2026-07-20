import unittest

from hunter_piggy import HunterPiggyPipeline


TEXT = """
The committee delayed referral for months. Budget screening reduced resources,
and responsibility moved between agencies until the temporary procedure became
normal practice.
"""


class PipelineTests(unittest.TestCase):
    def test_detects_correlated_scam_signals(self):
        result = HunterPiggyPipeline().analyze(
            "Pilne!!! Konto zablokowane. Potwierdź tożsamość: http://bit.ly/verify-account"
        )
        names = {signal.name for signal in result.threat_assessment.signals}
        self.assertTrue({"manipulative_language", "url_shortener", "credential_url_pattern"}.issubset(names))
        self.assertTrue(result.threat_assessment.human_review_recommended)

    def test_pipeline_detects_multiple_pic_levers(self):
        result = HunterPiggyPipeline().analyze(TEXT)
        codes = {lever.code for lever in result.pic_levers}
        self.assertTrue({"PIC-P", "PIC-F", "PIC-J", "PIC-T"}.issubset(codes))
        self.assertTrue(result.trajectory.key_levers)
        self.assertEqual(result.trajectory.dominant_trajectory, "shadow")

    def test_trajectory_is_reproducible(self):
        first = HunterPiggyPipeline().analyze(TEXT)
        second = HunterPiggyPipeline().analyze(TEXT)
        self.assertEqual(first.trajectory.growth.steps, second.trajectory.growth.steps)
        self.assertEqual(first.trajectory.shadow.steps, second.trajectory.shadow.steps)

    def test_empty_text_is_rejected(self):
        with self.assertRaises(ValueError):
            HunterPiggyPipeline().analyze("  ")

    def test_anti_loop_uses_repeated_results(self):
        pipeline = HunterPiggyPipeline()
        self.assertFalse(pipeline.analyze(TEXT).trajectory.anti_loop_detected)
        self.assertFalse(pipeline.analyze(TEXT).trajectory.anti_loop_detected)
        self.assertTrue(pipeline.analyze(TEXT).trajectory.anti_loop_detected)


if __name__ == "__main__":
    unittest.main()
