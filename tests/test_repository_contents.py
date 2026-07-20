"""Lightweight integrity checks for the bundled notebooks and analysis tables."""

import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NOTEBOOKS = (
    "1_Process_Raw_Steps_data.ipynb",
    "2_Eligibility.ipynb",
    "3_Combine_All_Covariates.ipynb",
    "3_Run_FPCA.ipynb",
    "4_AFT_Analysis_Splines.ipynb",
)

CSV_COLUMNS = {
    "steps_hour.csv": {"SEQN", "PAXDAYM", "HOUR", "steps_in_hour"},
    "Post_2-Restricted_Patients.csv": {"SEQN"},
    "Post_3_FPCA_Scores.csv": {"SEQN", "FPCA_score_1", "FPCA_score_2", "FPCA_score_3"},
    "Post_3_Top3_FPCA_Scores.csv": {"SEQN", "FPCA_score_1", "FPCA_score_2", "FPCA_score_3"},
    "Post_4_Covariates.csv": {"SEQN", "death", "followup_months", "age", "bmi"},
    "nhanes_mean_curve.csv": {"week_hour", "mean_steps"},
    "nhanes_first_eigenfunction.csv": {"week_hour", "eigenfunction_1"},
    "fpca_spline_lookup.csv": {"FPCA_score_1", "spline_1", "spline_2"},
    "cox_baseline_survival.csv": {"time", "surv", "cumhaz"},
}


class RepositoryContentsTests(unittest.TestCase):
    def test_notebooks_are_valid_jupyter_documents(self):
        for filename in NOTEBOOKS:
            with self.subTest(filename=filename):
                with (ROOT / filename).open(encoding="utf-8") as source:
                    notebook = json.load(source)
                self.assertEqual(notebook["nbformat"], 4)
                self.assertTrue(notebook["cells"])

    def test_csv_tables_have_expected_columns_and_rows(self):
        for filename, expected_columns in CSV_COLUMNS.items():
            with self.subTest(filename=filename):
                with (ROOT / filename).open(encoding="utf-8-sig", newline="") as source:
                    reader = csv.DictReader(source)
                    self.assertTrue(expected_columns.issubset(reader.fieldnames or []))
                    self.assertIsNotNone(next(reader, None))

    def test_readme_includes_workflow_image_and_related_project(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        image_path = ROOT / "docs" / "assets" / "nhanes-fpca-aft-pipeline.svg"

        self.assertTrue(image_path.is_file())
        self.assertIn("docs/assets/nhanes-fpca-aft-pipeline.svg", readme)
        self.assertIn("https://github.com/resace3/FPCA_AFT_Health_Addon", readme)
        self.assertIn("actions/workflows/tests.yml/badge.svg", readme)
        self.assertIn("img.shields.io/github/last-commit", readme)


if __name__ == "__main__":
    unittest.main()
