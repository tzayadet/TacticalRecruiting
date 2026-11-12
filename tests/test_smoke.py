"""Smoke tests for Tactical Recruiting's local data layer."""

import tempfile
import unittest
from pathlib import Path

from database import DatabaseManager
from consent import parse_consent
from questions import QuestionBank
from cv_utils import MAX_CV_BYTES, sanitize_cv_filename, validate_cv_path


class ConsentParsingTests(unittest.TestCase):
    def test_blank_and_negative_answers_do_not_record_consent(self):
        for value in (None, "", " ", "n", "no"):
            with self.subTest(value=value):
                self.assertEqual(parse_consent(value), 0)

    def test_explicit_affirmative_answers_record_consent(self):
        for value in ("s", "si", "sí", "y", "yes", " YES "):
            with self.subTest(value=value):
                self.assertEqual(parse_consent(value), 1)


class DatabaseManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.db = DatabaseManager(
            db_path=str(root / "recruiting.sqlite3"),
            cv_folder=str(root / "cvs"),
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initialization_creates_seed_data(self):
        profiles = self.db.listar_perfiles_empresa()
        self.assertGreater(len(profiles), 0)
        self.assertTrue(any(profile["nombre"] for profile in profiles))


    def test_candidate_registration_requires_affirmative_consent(self):
        with self.assertRaises(ValueError):
            self.db.crear_candidato({"nombre": "No Consent", "gdpr_consent": 0})

    def test_candidate_insert_uses_matching_column_and_value_count(self):
        candidate_id = self.db.crear_candidato({
            "nombre": "Consent Test",
            "email": "consent@example.com",
            "gdpr_consent": 1,
        })
        candidate = self.db.obtener_candidato(candidate_id)
        self.assertEqual(candidate["nombre"], "Consent Test")
        self.assertEqual(candidate["gdpr_consent"], 1)

    def test_cv_filename_is_reduced_to_safe_basename(self):
        self.assertEqual(sanitize_cv_filename("../../private/resume.pdf"), "resume.pdf")
        self.assertEqual(sanitize_cv_filename(r"..\\private\\resume.docx"), "resume.docx")
        with self.assertRaises(ValueError):
            sanitize_cv_filename("../payload.exe")

    def test_cv_storage_is_bounded_and_stays_inside_cv_directory(self):
        candidate_id = self.db.crear_candidato({
            "nombre": "CV Test",
            "gdpr_consent": 1,
            "cv_data": b"%PDF-1.4\\nsynthetic test file",
            "cv_filename": "../../outside.pdf",
        })
        cv_path = Path(self.db.obtener_ruta_cv(candidate_id))
        self.assertTrue(cv_path.is_file())
        self.assertEqual(cv_path.parent, Path(self.temp_dir.name) / "cvs")
        self.assertTrue(cv_path.name.endswith("_outside.pdf"))

    def test_cv_input_rejects_unsupported_extension_and_oversized_files(self):
        root = Path(self.temp_dir.name)
        unsupported = root / "payload.exe"
        unsupported.write_bytes(b"not a CV")
        with self.assertRaises(ValueError):
            validate_cv_path(unsupported)

        oversized = root / "oversized.pdf"
        oversized.write_bytes(b"x" * (MAX_CV_BYTES + 1))
        with self.assertRaises(ValueError):
            validate_cv_path(oversized)

    def test_vacancy_can_be_created_and_listed(self):
        vacancy_id = self.db.crear_vacante({
            "titulo": "Python Backend Developer",
            "departamento": "Engineering",
            "ubicacion": "Remote",
            "modalidad": "Remoto",
            "stack_obligatorio": "Python, REST, SQL",
            "stack_deseable": "Docker",
            "rango_salarial_min": 35000,
            "rango_salarial_max": 45000,
            "responsable": "Recruitment",
        })

        vacancies = self.db.listar_vacantes()
        self.assertTrue(any(vacancy["id"] == vacancy_id for vacancy in vacancies))


class QuestionBankTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "questions.sqlite3"
        self.bank = QuestionBank(db_path=db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initial_questions_are_available_and_anonymized(self):
        questions = self.bank.listar_preguntas()
        self.assertGreater(len(questions), 0)
        combined = " ".join(question["texto"] for question in questions).lower()
        self.assertNotIn("alvatross", combined)
        self.assertNotIn("satec", combined)

    def test_empty_tag_search_returns_no_results(self):
        self.assertEqual(self.bank.buscar_por_tags([]), [])

    def test_backend_interview_guide_contains_questions(self):
        guide = self.bank.generar_guia_entrevista("backend")
        self.assertTrue(guide)
        self.assertTrue(any(section["preguntas"] for section in guide))


if __name__ == "__main__":
    unittest.main()
