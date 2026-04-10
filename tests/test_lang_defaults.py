"""Packaged reusable settings dicts in ``lang.defaults``."""

from lang.defaults import LANGUAGE_HREFLANG_MAP, LANGUAGE_WIKIPEDIA_SAMEAS, OG_LOCALE_BY_LANGUAGE


def test_language_hreflang_map_bcp47_examples():
    assert LANGUAGE_HREFLANG_MAP["zh-hans"] == "zh-Hans"
    assert LANGUAGE_HREFLANG_MAP["zh-hant"] == "zh-Hant"


def test_wikipedia_and_og_locale_have_common_codes():
    assert "it" in LANGUAGE_WIKIPEDIA_SAMEAS
    assert OG_LOCALE_BY_LANGUAGE["en"] == "en_US"
