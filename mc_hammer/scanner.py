import os
import difflib

class Scanner:
    def __init__(self):
        pass

    def scan(self):
        """
        Perform a scan of the file system.
        Returns a list of file paths.
        """
        scan_results = []
        for root, dirs, files in os.walk('/'):
            for file in files:
                scan_results.append(os.path.join(root, file))
        return scan_results

    def compare(self, current_scan, base_scan):
        """
        Compare the current scan with the base scan.
        Returns a list of discrepancies.
        """
        diff = difflib.unified_diff(base_scan, current_scan)
        discrepancies = list(diff)
        return discrepancies
