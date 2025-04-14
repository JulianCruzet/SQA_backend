import unittest
from tempfile import NamedTemporaryFile
from main import read_merged_bank_transactions

class TestReadMergedBankTransactions(unittest.TestCase):
    def setUp(self):
        """Create a temporary file with test data"""
        self.test_file = NamedTemporaryFile(mode='w', delete=False)
        self.empty_file = NamedTemporaryFile(mode='w', delete=False)
        self.single_transaction_file = NamedTemporaryFile(mode='w', delete=False)

        test_data = [
            "01 John Doe             12345 01000.00 XX",
            "02 Jane Smith           54321 00500.50 XY",
            "03 InvalidUser          ABCDE   700.00 YZ", # Invalid Account Number
            '04 Mike Brown           67890 -0200.00 ZW',# Invalid Amount
            "05 Alice White          13579 01200.75 WA",
            "00 End of Session       99999 00000.00 NA", # End session
            "05 Charlie Brown        13579 00010.50 NA",# Should not be processed after 00

        ]

        # Write each line separately, ensuring exact formatting
        with open(self.test_file.name, 'w') as f:
            for line in test_data:
                f.write(line + '\n')  # Ensure proper line endings
        with open(self.single_transaction_file.name, 'w') as f:
            f.write("01 John Doe             12345 01000.00 XX")

        self.test_file.close()
        self.empty_file.close()
        self.single_transaction_file.close()


    def tearDown(self):
        """Remove the temporary test file"""
        import os
        os.unlink(self.test_file.name)
        os.unlink(self.empty_file.name)
        os.unlink(self.single_transaction_file.name)

    def test_valid_transactions(self):
        """Test processing of valid transactions"""
        transactions = read_merged_bank_transactions(self.test_file.name)
        self.assertEqual(len(transactions), 3)  # Should stop at '00'
        self.assertEqual(transactions[0]['transaction_code'], "01")
        self.assertEqual(transactions[1]['transaction_code'], "02")
        self.assertEqual(transactions[2]['transaction_code'], "05")

    def test_invalid_transactions(self):
        """Test handling of invalid transactions"""
        transactions = read_merged_bank_transactions(self.test_file.name)
        account_numbers = [t['account_number'] for t in transactions]
        self.assertNotIn("ABCDE", account_numbers)  # Invalid account number
        self.assertNotIn("67890", account_numbers)  # Invalid negative amount

    def test_end_of_session(self):
        """Ensure processing stops when '00' transaction code is encountered"""
        transactions = read_merged_bank_transactions(self.test_file.name)
        self.assertFalse(any(t['transaction_code'] == "06" for t in transactions))

    def test_empty_file(self):
        """Test when the file is empty (loop runs 0 times)"""

        transactions = read_merged_bank_transactions(self.empty_file.name)
        self.assertEqual(len(transactions), 0)  # No transactions should be processed

    def test_single_transaction(self):
        """Test when the file has only one transaction (loop runs 1 time)"""

        transactions = read_merged_bank_transactions(self.single_transaction_file.name)
        self.assertEqual(1, len(transactions))  # Should process only one transaction
        self.assertEqual(transactions[0]['transaction_code'], "01")

if __name__ == '__main__':
    unittest.main()
