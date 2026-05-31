def role_flags(request):
    user = request.user
    is_librarian = False
    is_client = False

    if user.is_authenticated:
        if user.is_superuser or user.groups.filter(name='librarian').exists():
            is_librarian = True
        if user.groups.filter(name='client').exists():
            is_client = True

    return {
        'is_librarian': is_librarian,
        'is_client': is_client,
    }
