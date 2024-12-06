# utils/file_handler.py
"""
@file utils/file_handler.py
@brief Provides utilities for scanning directories, applying include/exclude patterns, 
      and reading file contents.
"""
import os
import fnmatch
from logger import get_logger

logger = get_logger(__name__)

class FileHandler:
    @staticmethod
    def scan_files(base_path, includes=None, excludes=None):
        """
        Scan files in base_path applying include and exclude patterns.
        includes and excludes are lists of glob-like patterns.
        """
        logger.debug(f"Scanning files in {base_path} with includes={includes}, excludes={excludes}")
        if not os.path.isabs(base_path):
            # If the base_path is relative, we assume it's relative to the project_path.
            # The caller should ensure correctness.
            pass

        all_files = []
        for root, dirs, files in os.walk(base_path):
            # Filter excluded directories
            dirs[:] = [d for d in dirs if not FileHandler._matches_any(os.path.join(root, d), excludes, is_dir=True)]
            for f in files:
                full_path = os.path.join(root, f)
                # Check excludes
                if FileHandler._matches_any(full_path, excludes):
                    continue
                # Check includes if specified
                if includes:
                    if FileHandler._matches_any(full_path, includes):
                        all_files.append(full_path)
                else:
                    # If no includes specified, include all files unless excluded.
                    all_files.append(full_path)

        return all_files

    @staticmethod
    def _matches_any(path, patterns, is_dir=False):
        """Check if a path matches any given pattern. Patterns can use wildcards and **."""
        if not patterns:
            return False

        # Convert path separators to forward slash for consistency in matching
        normalized_path = path.replace(os.sep, "/")
        for p in patterns:
            # Patterns might also be something like "**/*.py,*.html"
            # We'll split by "," and check each.
            sub_patterns = [pt.strip() for pt in p.split(",")]
            for sp in sub_patterns:
                if fnmatch.fnmatch(normalized_path, sp):
                    return True
        return False

    @staticmethod
    def read_file(path):
        """Read the contents of a file and return as string."""
        logger.debug(f"Reading file {path}")
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def ensure_json5_file(path, default_content):
        """
        Ensure a JSON5 file exists at 'path'. If not, create it with default_content.
        """
        logger.debug(f"Ensuring json5 file at {path}")
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(default_content)
        return path
