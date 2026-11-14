"""SVG validation, security sanitization checks, and XML well-formedness audit."""

import os
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple


class SvgValidationError(Exception):
    """Raised when SVG fails structural or security validation."""
    pass


BANNED_ELEMENTS = {
    "script",
    "iframe",
    "embed",
    "object",
    "foreignObject",
    "applet",
    "form",
    "input",
    "button",
}

BANNED_ATTRIBUTES_PREFIX = ("on",)  # onclick, onload, onerror, etc.


def validate_svg_content(svg_content: str, max_size_bytes: int = 50 * 1024) -> Tuple[bool, List[str]]:
    """
    Validate SVG XML string for:
    1. XML well-formedness (parses via ElementTree)
    2. Zero banned tags (script, foreignObject, iframe, etc.)
    3. Zero inline event listeners (onclick, onload, etc.)
    4. Size budget constraint (< 50KB recommended)
    5. Presence of valid viewBox attribute on root element
    """
    errors: List[str] = []

    # 1. Size check
    size = len(svg_content.encode("utf-8"))
    if size > max_size_bytes:
        errors.append(f"SVG payload ({size:,} bytes) exceeds budget of {max_size_bytes:,} bytes.")

    # 2. XML Well-formedness
    try:
        root = ET.fromstring(svg_content)
    except ET.ParseError as pe:
        errors.append(f"XML ParseError: {pe}")
        return False, errors

    # Check root tag is svg
    root_tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if root_tag.lower() != "svg":
        errors.append(f"Root tag is <{root_tag}>, expected <svg>.")

    # Check viewBox
    if "viewBox" not in root.attrib and "viewbox" not in root.attrib:
        errors.append("Root <svg> is missing required 'viewBox' attribute.")

    # 3. Security Inspection: Inspect all descendant tags and attributes
    for elem in root.iter():
        tag_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag_name.lower() in BANNED_ELEMENTS:
            errors.append(f"Security Violation: Forbidden tag <{tag_name}> found in SVG.")

        for attr_name, attr_val in elem.attrib.items():
            attr_clean = attr_name.split("}")[-1] if "}" in attr_name else attr_name
            if any(attr_clean.lower().startswith(p) for p in BANNED_ATTRIBUTES_PREFIX):
                errors.append(f"Security Violation: Banned event handler attribute '{attr_clean}' found.")
            if isinstance(attr_val, str) and "javascript:" in attr_val.lower():
                errors.append(f"Security Violation: 'javascript:' URI detected in attribute '{attr_clean}'.")

    return len(errors) == 0, errors


def validate_svg_file(file_path: str, max_size_bytes: int = 50 * 1024) -> Tuple[bool, List[str]]:
    """Validate SVG file on disk."""
    if not os.path.exists(file_path):
        return False, [f"File not found: {file_path}"]
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return validate_svg_content(content, max_size_bytes=max_size_bytes)
