from storage.db import cur

def has_permission(ctx, command):
    return True  # ALL users can run commands
