def get_error(errors):
    for field in errors:
        return errors.get(field).as_text().lstrip('* ')
