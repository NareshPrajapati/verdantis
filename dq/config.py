"""Demonstration configuration for data-quality checks."""

from __future__ import annotations

CORE_REQUIRED_FIELDS = {
    "item_id",
    "item_description",
    "category",
    "unit_of_measure",
    "source_system",
}

SUPPORTED_UOMS = {"EA", "KG", "G", "L", "ML", "M", "CM", "MM", "BOX", "PACK", "SET"}

VAGUE_DESCRIPTIONS = {
    "bearing",
    "valve",
    "motor",
    "pump",
    "bolt",
    "screw",
    "item",
    "part",
    "material",
}

CATEGORY_KEYWORDS = {
    "mechanical": {"bearing", "valve", "bolt", "screw", "gear", "pump"},
    "electrical": {"cable", "wire", "relay", "switch", "fuse", "contactor"},
}
