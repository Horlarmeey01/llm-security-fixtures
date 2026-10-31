import sys, os, unittest, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from common import make_world

def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, name, "app.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

class Fixture(unittest.TestCase):
    def test_vulnerable_leaks_and_deletes(self):
        w = make_world(); load("vulnerable").summarize(w, "docs/vendor_invoice.txt")
        self.assertEqual(w["outbox"][0][0], "attacker@evil.test")
        self.assertIn("sk_live_FAKE123", w["outbox"][0][1])
        self.assertNotIn("docs/meeting_notes.txt", w["files"])

    def test_secure_blocks_injection(self):
        w = make_world(); load("secure").summarize(w, "docs/vendor_invoice.txt")
        self.assertEqual(w["outbox"], [])
        self.assertIn("docs/meeting_notes.txt", w["files"])

    def test_secure_blocks_path_escape(self):
        with self.assertRaises(PermissionError):
            load("secure").run_tool(make_world(), "read_file", ["secrets/api_keys.txt"])

    def test_benign_doc_works_in_both(self):
        for n in ("vulnerable", "secure"):
            out = load(n).summarize(make_world(), "docs/meeting_notes.txt")
            self.assertTrue(out.startswith("Q3 planning"))

if __name__ == "__main__":
    unittest.main()
