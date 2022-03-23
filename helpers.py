# Match anchors with href containing the given string
def clean_href_string(string_literal):
    return string_literal.lower().replace(" ", "-")
