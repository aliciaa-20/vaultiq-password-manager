import unittest
from models import PasswordStrength


class TestPasswordStrength(unittest.TestCase):
    def test_very_weak_short(self):
        score, label = PasswordStrength.calculate("123")
        self.assertLess(score, 20)
        self.assertEqual(label, "Very Weak")

    def test_weak_lowercase_only(self):
        score, label = PasswordStrength.calculate("password")
        self.assertGreaterEqual(score, 20)
        self.assertLess(score, 40)
        self.assertEqual(label, "Weak")

    def test_fair_mixed_case(self):
        score, label = PasswordStrength.calculate("Password")
        self.assertGreaterEqual(score, 40)
        self.assertLess(score, 60)
        self.assertEqual(label, "Fair")

    def test_good_with_digits(self):
        score, label = PasswordStrength.calculate("Password123")
        self.assertGreaterEqual(score, 60)
        self.assertLess(score, 80)
        self.assertEqual(label, "Good")

    def test_very_strong_all_types(self):
        score, label = PasswordStrength.calculate("MyP@ssw0rd!")
        self.assertGreaterEqual(score, 80)
        self.assertEqual(label, "Very Strong")

    def test_score_max_100(self):
        score, label = PasswordStrength.calculate("VeryLongSecureP@ssw0rd!@#$")
        self.assertLessEqual(score, 100)

    def test_uppercase_bonus(self):
        score1, _ = PasswordStrength.calculate("password")
        score2, _ = PasswordStrength.calculate("Password")
        self.assertGreater(score2, score1)

    def test_digit_bonus(self):
        score1, _ = PasswordStrength.calculate("Password")
        score2, _ = PasswordStrength.calculate("Password1")
        self.assertGreater(score2, score1)

    def test_special_char_bonus(self):
        score1, _ = PasswordStrength.calculate("Password1")
        score2, _ = PasswordStrength.calculate("Password1!")
        self.assertGreater(score2, score1)

    def test_length_bonus_short(self):
        score1, _ = PasswordStrength.calculate("Pass")
        score2, _ = PasswordStrength.calculate("Password")
        self.assertGreater(score2, score1)

    def test_length_bonus_long(self):
        score1, _ = PasswordStrength.calculate("MyPassword12")
        score2, _ = PasswordStrength.calculate("MyVeryLongSecurePassword123!")
        self.assertGreater(score2, score1)


if __name__ == "__main__":
    unittest.main()
