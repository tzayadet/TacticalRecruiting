"""CV input validation and safe local filename handling."""

import re
from pathlib import Path

ALLOWED_CV_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_CV_BYTES = 10 * 1024 * 1024
_WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def validate_cv_path(path):
    """Return a validated local CV path, limited by type and size."""
    candidate = Path(path).expanduser()
    if not candidate.is_file():
        raise FileNotFoundError(f"CV file does not exist: {candidate}")
    if candidate.suffix.lower() not in ALLOWED_CV_EXTENSIONS:
        raise ValueError("CV format must be PDF, DOC or DOCX.")
    size = candidate.stat().st_size
    if size > MAX_CV_BYTES:
        raise ValueError(
            f"CV exceeds the {MAX_CV_BYTES // (1024 * 1024)} MB size limit."
        )
    return candidate.resolve()


def sanitize_cv_filename(filename):
    """Reduce a supplied filename to a safe, supported basename."""
    if not isinstance(filename, str) or not filename or "\x00" in filename:
        raise ValueError("CV filename is empty or invalid.")

    basename = filename.replace("\\", "/").rsplit("/", 1)[-1].strip()
    if basename in {"", ".", ".."}:
        raise ValueError("CV filename is not valid.")

    suffix = Path(basename).suffix.lower()
    if suffix not in ALLOWED_CV_EXTENSIONS:
        raise ValueError("CV format must be PDF, DOC or DOCX.")

    # Remove Windows-invalid and control characters without losing readable text.
    basename = re.sub(r'[<>:"|?*\x00-\x1f]', "_", basename)
    basename = basename.rstrip(" .")
    if not basename:
        raise ValueError("CV filename is not valid.")

    if len(basename) > 150:
        stem = Path(basename).stem[: 150 - len(suffix)]
        basename = stem + suffix

    if Path(basename).stem.upper() in _WINDOWS_RESERVED_NAMES:
        basename = "_" + basename

    return basename
