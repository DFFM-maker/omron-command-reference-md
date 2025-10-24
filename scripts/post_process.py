#!/usr/bin/env python3
"""
Post-processing del Markdown convertito
Ottimizzazioni specifiche per manuali tecnici Omron
"""

import re
import argparse
from pathlib import Path
from typing import List

def clean_extra_whitespace(text: str) -> str:
    """Rimuove spazi bianchi eccessivi"""
    # Rimuovi spazi multipli
    text = re.sub(r' +', ' ', text)
    # Rimuovi righe vuote multiple (max 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

def fix_table_formatting(text: str) -> str:
    """Migliora la formattazione delle tabelle"""
    lines = text.split('\n')
    result = []
    
    for line in lines:
        # Se la riga contiene pipe (|), è probabilmente una tabella
        if '|' in line and line.strip():
            # Assicura spazi attorno ai pipe
            line = re.sub(r'\s*\|\s*', ' | ', line)
            # Rimuovi spazi all'inizio e alla fine
            line = line.strip()
        result.append(line)
    
    return '\n'.join(result)

def improve_code_blocks(text: str) -> str:
    """Migliora i blocchi di codice per comandi Omron"""
    # Identifica pattern di comandi Omron (es. @00RD, @00WR, ecc.)
    # e assicura che siano in blocchi di codice
    pattern = r'(@\d{2}[A-Z]{2,4}[^
]*)'
    
    def wrap_command(match):
        command = match.group(1)
        # Se non è già in un blocco di codice
        return f'`{command}`'
    
    text = re.sub(pattern, wrap_command, text)
    return text

def add_table_of_contents(text: str, filename: str) -> str:
    """Aggiunge un indice basato sui titoli"""
    lines = text.split('\n')
    headers = []
    
    # Trova tutti i titoli
    for i, line in enumerate(lines):
        if line.startswith('#'):
            level = len(re.match(r'^#+', line).group(0))
            title = line.lstrip('#').strip()
            anchor = re.sub(r'[^
w\s-]', '', title).replace(' ', '-').lower()
            headers.append((level, title, anchor))
    
    # Crea l'indice
    if headers:
        toc = [f"# {filename} - Indice\n"]
        toc.append("---\n")
        
        for level, title, anchor in headers:
            indent = "  " * (level - 1)
            toc.append(f"{indent}- [{title}](#{anchor})")
        
        toc.append("\n---\n")
        return '\n'.join(toc) + '\n' + text
    
    return text

def enhance_omron_commands(text: str) -> str:
    """Migliora la presentazione dei comandi Omron"""
    # Pattern per comandi comuni Omron
    patterns = [
        (r'(@\d{2}RD)', r'**\1** _(Read)_'),  # Read commands
        (r'(@\d{2}WR)', r'**\1** _(Write)_'),  # Write commands
        (r'(@\d{2}SC)', r'**\1** _(Status Check)_'),  # Status commands
        (r'(@\d{2}TC)', r'**\1** _(Test Communication)_'),  # Test commands
    ]
    
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    
    return text

def post_process_markdown(input_file: Path, output_file: Path = None):
    """
    Processa il file Markdown convertito
    
    Args:
        input_file: File Markdown da processare
        output_file: File di output (default: sovrascrive l'input)
    """
    print(f"📝 Post-processing: {input_file.name}")
    
    # Leggi il file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Applica le trasformazioni
    print("  🔧 Pulizia whitespace...")
    text = clean_extra_whitespace(text)
    
    print("  📊 Formattazione tabelle...")
    text = fix_table_formatting(text)
    
    print("  💻 Miglioramento blocchi di codice...")
    text = improve_code_blocks(text)
    
    print("  🎯 Enhancement comandi Omron...")
    text = enhance_omron_commands(text)
    
    print("  📑 Aggiunta indice...")
    text = add_table_of_contents(text, input_file.stem)
    
    # Salva il file processato
    if output_file is None:
        output_file = input_file
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"✅ Post-processing completato: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Post-processing del Markdown convertito"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="File Markdown da processare"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="File di output (default: sovrascrive l'input)"
    )
    
    args = parser.parse_args()
    
    input_file = Path(args.input)
    output_file = Path(args.output) if args.output else None
    
    if not input_file.exists():
        print(f"❌ Errore: File non trovato: {input_file}")
        return 1
    
    try:
        post_process_markdown(input_file, output_file)
        return 0
    except Exception as e:
        print(f"❌ Errore durante il post-processing: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
