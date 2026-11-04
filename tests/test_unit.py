import unittest

from bmi_logic import bmi_gauge_position, bmi_guidance, military_guidance


class BmiUnitTests(unittest.TestCase):
    def test_taiwan_adult_thresholds(self):
        for bmi, category in [
            (18.4, "體重過輕"),
            (18.5, "健康體位"),
            (23.9, "健康體位"),
            (24.0, "體重過重"),
            (26.9, "體重過重"),
            (27.0, "肥胖"),
        ]:
            with self.subTest(bmi=bmi):
                self.assertEqual(bmi_guidance(bmi)["label"], category)

    def test_bmi_gauge_marks_ranges_and_clamps_extremes(self):
        self.assertEqual(bmi_gauge_position(10), 0)
        self.assertEqual(bmi_gauge_position(22.5), 50)
        self.assertEqual(bmi_gauge_position(35), 100)
        self.assertEqual(bmi_gauge_position(5), 0)
        self.assertEqual(bmi_gauge_position(40), 100)

    def test_military_classification(self):
        self.assertEqual(military_guidance(170, 22.5)["label"], "常備役體位（初步篩選）")
        self.assertEqual(military_guidance(170, 15.5)["label"], "替代役體位（初步篩選）")
        self.assertEqual(military_guidance(170, 36)["label"], "免役體位（初步篩選）")
        self.assertEqual(military_guidance(154, 22.5)["label"], "免役體位（初步篩選）")


if __name__ == "__main__":
    unittest.main()
