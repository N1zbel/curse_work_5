def func_for_clear_text(text):
    result = text.replace('<highlighttext>', '').replace('</highlighttext>', '')
    return result
