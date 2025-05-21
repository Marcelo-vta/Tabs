def print_tree(node, prefix="", is_left=True):
    """Imprime a árvore de nós no terminal de forma visual."""
    if node is None:
        return

    # Define o símbolo do nó
    connector = "├── " if is_left else "└── "

    # Imprime o valor do nó com a indentação correta
    print(prefix + connector + str(node.value))

    # Ajusta o prefixo para os filhos
    new_prefix = prefix + ("│   " if is_left else "    ")

    # Verifica se o nó tem filhos e imprime recursivamente
    if hasattr(node, "children") and node.children:
        for i, child in enumerate(node.children):
            is_last = (i == len(node.children) - 1)  # Verifica se é o último filho
            print_tree(child, new_prefix, not is_last)

def printSong(song):
    songString = ''
    songString += '"'

    for tab in song:
        songString += ' |'
        for note in tab:
            if note.isnumeric():
                note = int(note)
            songString += f' {note}'

            songString += " -"
        
        songString = songString[:-1] + "|"

    songString += ' "'
    print(songString)
