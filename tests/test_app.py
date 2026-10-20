import os
import tempfile
import unittest

from app import app, bmi_guidance


class BmiAppTests(unittest.TestCase):
    def setUp(self):
        self.database_file = tempfile.NamedTemporaryFile(delete=False)
        self.database_file.close()
        app.config["DATABASE"] = self.database_file.name
        self.client = app.test_client()

    def tearDown(self):
        os.unlink(self.database_file.name)

    def test_initial_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("了解自己的<br><em>健康狀況。</em>", page)
        self.assertIn("計算你的 BMI", page)

    def test_calculation_and_advice(self):
        response = self.client.post("/", data={"height": "170", "weight": "65"})
        page = response.get_data(as_text=True)
        self.assertIn("22.5", page)
        self.assertIn("健康體位", page)
        self.assertIn("維持均衡飲食", page)

    def test_abnormal_bmi_is_highlighted_in_red(self):
        for height, weight, tone in [("170", "50", "low"), ("170", "75", "high")]:
            with self.subTest(height=height, weight=weight):
                response = self.client.post("/", data={"height": height, "weight": weight})
                page = response.get_data(as_text=True)
                self.assertIn(f'class="result-number {tone}"', page)

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

    def test_invalid_fields_do_not_produce_result(self):
        for height, weight in [("", "65"), ("0", "65"), ("abc", "65"), ("170", "-2"), ("inf", "65"), ("170", "nan"), ("1e-300", "65"), ("1e308", "65"), ("1", "1e308")]:
            with self.subTest(height=height, weight=weight):
                response = self.client.post("/", data={"height": height, "weight": weight})
                page = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn('aria-invalid="true"', page)
                self.assertNotIn("YOUR RESULT", page)

    def test_input_is_escaped(self):
        response = self.client.post("/", data={"height": '<script>alert(1)</script>', "weight": "65"})
        page = response.get_data(as_text=True)
        self.assertNotIn("<script>", page)
        self.assertIn("請輸入大於 0", page)

    def test_user_history_is_saved_and_linked_from_user_list(self):
        self.client.post("/", data={"user_name": "王小明", "height": "170", "weight": "65"})
        self.client.post("/", data={"user_name": "王小明", "height": "170", "weight": "75"})

        response = self.client.get("/")
        page = response.get_data(as_text=True)
        self.assertIn("王小明", page)
        self.assertIn("2 筆紀錄", page)
        self.assertIn("/users/%E7%8E%8B%E5%B0%8F%E6%98%8E", page)

        response = self.client.get("/users/王小明")
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("王小明的", page)
        self.assertIn("22.5", page)
        self.assertIn("26.0", page)
        self.assertIn("T", page)

    def test_missing_name_is_saved_as_guest(self):
        self.client.post("/", data={"height": "170", "weight": "65"})
        response = self.client.get("/")
        self.assertIn("訪客", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
