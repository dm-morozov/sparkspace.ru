"""Custom duotone pictograms for the interactive process navigation."""
def icon(role, fallback):
    shapes = {
        'message': '<path fill="#e9e3ff" stroke="none" d="M4 5h24v18H12l-8 5z"/><path d="M4 5h24v18H12l-8 5V5Z"/><path d="M9 11h14M9 16h9"/><circle cx="25" cy="7" r="4" fill="#fff"/><path d="m23 7 1.5 1.5L27 6"/>',
        'person': '<circle cx="13" cy="10" r="5" fill="#e9e3ff"/><path d="M4 27v-3a9 9 0 0 1 18 0v3" fill="#e9e3ff"/><path d="M24 6a5 5 0 0 1 0 10m2 5a7 7 0 0 1 3 6"/>',
        'clipboard': '<rect x="6" y="5" width="21" height="25" rx="3" fill="#e9e3ff"/><rect x="11" y="2" width="11" height="6" rx="2" fill="#fff"/><path d="m10 15 2 2 3-4m3 2h5m-13 8 2 2 3-4m3 2h5"/>',
        'calendar': '<rect x="4" y="6" width="25" height="23" rx="3" fill="#e9e3ff"/><path d="M10 3v6m13-6v6M4 13h25"/><rect x="9" y="18" width="8" height="6" rx="1" fill="#fff"/><path d="m21 21 2 2 4-5"/>',
        'check': '<path d="m16 3 4 2 5 1 1 5 3 5-3 5-1 5-5 1-4 2-4-2-5-1-1-5-3-5 3-5 1-5 5-1z" fill="#e9e3ff"/><path d="m10 16 4 4 8-9" stroke-width="2.2"/>',
    }
    if role in shapes:
        return '<svg class="process-glyph" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+shapes[role]+'</svg>'
    return fallback(role).replace('<svg ', '<svg class="process-glyph" ', 1)
