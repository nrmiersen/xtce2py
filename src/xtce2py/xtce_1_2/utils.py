"""XTCE 1.2 utilities."""

import xtce2py.xtce_1_2.bindings as xtce


def get_description(xtce_obj: xtce.NameDescriptionType) -> str:
    """Extract the description from an XTCE object, preferring long_description over short_description.

    Args:
        xtce_obj (xtce.NameDescriptionType): The XTCE object to extract the description from.

    Returns:
        str: The extracted description, preferring long_description over short_description.

    """
    return xtce_obj.long_description or xtce_obj.short_description or ""


def parse_match_criteria(criteria: xtce.ArgumentMatchCriteriaType, context=None) -> str:
    """Translate XTCE MatchCriteria into a Python boolean expression string.

    Args:
        criteria (xtce.ArgumentMatchCriteriaType): The XTCE MatchCriteria to translate.
        context: Optional context for type information.

    Returns:
        str: The Python boolean expression string representing the match criteria.

    """
    # Simple comparison
    if criteria.comparison:
        return _parse_comparison(criteria.comparison)

    # Comparison list
    if criteria.comparison_list:
        conditions = []
        for comp in criteria.comparison_list.comparison:
            conditions.append(_parse_comparison(comp))
        return " and ".join(conditions)

    # Boolean expression
    if criteria.boolean_expression:
        # TODO
        raise NotImplementedError(
            "Boolean expressions in MatchCriteria are not yet supported."
        )

    # Custom algorithm
    if criteria.custom_algorithm:
        # TODO
        raise NotImplementedError(
            "Custom algorithms in MatchCriteria are not yet supported."
        )

    return "True"


def _parse_comparison(comparison: xtce.ArgumentComparisonType) -> str:
    """Translate a single ComparisonType into a comparison string."""
    if comparison.parameter_instance_ref:
        raise NotImplementedError(
            "parameter_instance_ref in ComparisonType is not yet supported."
        )
    elif comparison.argument_instance_ref:
        raise NotImplementedError(
            "argument_instance_ref in ComparisonType is not yet supported."
        )

    lhs = "unknown_var"  # TODO placeholder

    return f"{lhs} {comparison.comparison_operator.value} {comparison.value}"
