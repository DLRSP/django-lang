from typing import Any, Dict, Optional

from django import template, urls

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context: Dict[str, Any], language: Optional[str]) -> str:
    """Get the absolute URL of the current page for the specified language.

    Usage:
        {% translate_url 'en' %}
    """
    url = context["request"].build_absolute_uri()
    return urls.translate_url(url, language)
