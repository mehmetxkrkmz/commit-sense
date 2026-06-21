import subprocess
import re
import os

class GitScanner:
    @staticmethod
    def get_staged_diff():
        """Returns the git diff of currently staged files."""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""
        except FileNotFoundError:
            return "" # Git not installed or not a git repo

class SecretScanner:
    # High-confidence regex patterns for critical secrets
    PATTERNS = {
        "AWS Access Key": r"(?i)AKIA[0-9A-Z]{16}",
        "GitHub Token": r"(?i)ghp_[0-9a-zA-Z]{36}",
        "OpenAI API Key": r"sk-(proj-)?[a-zA-Z0-9]{32,}",
        "RSA Private Key": r"-----BEGIN RSA PRIVATE KEY-----",
        "Generic Secret/Password": r"(?i)(password|secret|api_key|token)[\s:=]+['\"][^\s]+['\"]"
    }

    @classmethod
    def scan(cls, diff_text):
        """
        Scans text for secrets. 
        Returns a list of tuples: (Secret_Type, Matched_Line)
        """
        findings = []
        if not diff_text:
            return findings

        lines = diff_text.split('\n')
        for line in lines:
            # Only scan added lines in the diff
            if line.startswith('+') and not line.startswith('+++'):
                for secret_name, pattern in cls.PATTERNS.items():
                    if re.search(pattern, line):
                        # Redact the actual secret for reporting
                        redacted_line = line[:10] + "..." + line[-5:] if len(line) > 15 else "***REDACTED***"
                        findings.append((secret_name, redacted_line))
        return findings

class CommitGenerator:
    @staticmethod
    def generate_from_diff(diff_text):
        """
        Heuristic-based commit message generator.
        Analyzes the diff to determine the context and action.
        """
        if not diff_text:
            return "chore: minor updates or empty commit"

        added_lines = 0
        deleted_lines = 0
        files_changed = set()

        for line in diff_text.split('\n'):
            if line.startswith('+++ b/'):
                files_changed.add(line[6:])
            elif line.startswith('+') and not line.startswith('+++'):
                added_lines += 1
            elif line.startswith('-') and not line.startswith('---'):
                deleted_lines += 1

        if not files_changed:
            return "chore: updates"

        # Determine scope based on files
        scopes = []
        for f in files_changed:
            if f.endswith('.py'): scopes.append("python")
            elif f.endswith('.js') or f.endswith('.ts'): scopes.append("frontend")
            elif f.endswith('.md'): scopes.append("docs")
            elif f.endswith('.json') or f.endswith('.txt'): scopes.append("config")
        
        # Get dominant scope
        dominant_scope = max(set(scopes), key=scopes.count) if scopes else "core"

        # Determine type based on lines
        if "docs" in scopes and len(scopes) == 1:
            commit_type = "docs"
        elif "config" in scopes and len(scopes) == 1:
            commit_type = "chore"
        elif added_lines > 50 and deleted_lines < 10:
            commit_type = "feat"
        elif deleted_lines > 20 and added_lines < 10:
            commit_type = "refactor"
        else:
            commit_type = "fix" if "test" not in dominant_scope else "test"

        file_list_str = ", ".join(list(files_changed)[:2])
        if len(files_changed) > 2:
            file_list_str += " and others"

        return f"{commit_type}({dominant_scope}): update {file_list_str}"
