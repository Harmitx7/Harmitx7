"""Utility modules for the SVG generation engine."""

from src.utils.colors import (
    COLOR_BG_VOID,
    COLOR_BG_SURFACE,
    COLOR_BG_ELEVATED,
    COLOR_BORDER_SUBTLE,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_FAINT,
    COLOR_ACCENT_CYAN,
    COLOR_ACCENT_TANGERINE,
    COLOR_ACCENT_MINT,
    COLOR_ACCENT_AMBER,
    COLOR_ACCENT_CORAL,
    LANGUAGE_COLORS,
    hex_to_rgb,
    rgba_str,
    get_language_color,
)

from src.utils.formatting import (
    escape_xml,
    generate_unique_id,
    reset_id_registry,
    truncate_text,
    format_bytes,
    format_number,
    format_percentage,
)

from src.utils.validation import (
    validate_svg_content,
    validate_svg_file,
    SvgValidationError,
)

__all__ = [
    "COLOR_BG_VOID",
    "COLOR_BG_SURFACE",
    "COLOR_BG_ELEVATED",
    "COLOR_BORDER_SUBTLE",
    "COLOR_TEXT_PRIMARY",
    "COLOR_TEXT_SECONDARY",
    "COLOR_TEXT_MUTED",
    "COLOR_TEXT_FAINT",
    "COLOR_ACCENT_CYAN",
    "COLOR_ACCENT_TANGERINE",
    "COLOR_ACCENT_MINT",
    "COLOR_ACCENT_AMBER",
    "COLOR_ACCENT_CORAL",
    "LANGUAGE_COLORS",
    "hex_to_rgb",
    "rgba_str",
    "get_language_color",
    "escape_xml",
    "generate_unique_id",
    "reset_id_registry",
    "truncate_text",
    "format_bytes",
    "format_number",
    "format_percentage",
    "validate_svg_content",
    "validate_svg_file",
    "SvgValidationError",
]
