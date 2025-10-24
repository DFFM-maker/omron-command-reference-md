#!/usr/bin/env python3
"""
Script di conversione PDF -> Markdown usando Marker
Ottimizzato per manuali tecnici Omron
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    from marker.convert import convert_single_pdf
    from marker.models import load_all_models
except ImportError:
    print("❌ Marker non è installato. Esegui: pip install -r scripts/requirements.txt")
    sys.exit(1)

def setup_directories(output_dir: Path):
    """Crea le directory necessarie"""
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "images").mkdir(exist_ok=True)
    print(f"✅ Directory di output: {output_dir}")

def convert_pdf_to_markdown(pdf_path: Path, output_dir: Path):
    """
    Converte il PDF in Markdown usando Marker
    
    Args:
        pdf_path: Path al file PDF
        output_dir: Directory di output
    """
    print(f"\n🚀 Inizio conversione: {pdf_path.name}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Carica i modelli di Marker
    print("📦 Caricamento modelli Marker...")
    model_lst = load_all_models()
    
    # Converti il PDF
    print("🔄 Conversione in corso...")
    full_text, images, out_meta = convert_single_pdf(
        str(pdf_path),
        model_lst,
        max_pages=None,
        langs=["Italian", "English"],  # Supporto italiano e inglese
        batch_multiplier=2
    )
    
    # Salva il markdown
    output_file = output_dir / f"{pdf_path.stem}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"✅ Markdown salvato: {output_file}")
    
    # Salva le immagini
    if images:
        images_dir = output_dir / "images"
        for img_name, img_data in images.items():
            img_path = images_dir / img_name
            with open(img_path, 'wb') as f:
                f.write(img_data)
        print(f"✅ {len(images)} immagini salvate in: {images_dir}")
    
    # Salva i metadati
    metadata_file = output_dir / f"{pdf_path.stem}_metadata.txt"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        f.write(f"Conversione completata: {datetime.now()}\n")
        f.write(f"File originale: {pdf_path.name}\n")
        f.write(f"Pagine processate: {out_meta.get('pages', 'N/A')}\n")
        f.write(f"Immagini estratte: {len(images)}\n")
    
    print(f"✅ Metadati salvati: {metadata_file}")
    print(f"\n🎉 Conversione completata con successo!")
    
    return output_file

def main():
    parser = argparse.ArgumentParser(
        description="Converti PDF Omron in Markdown usando Marker"
    )
    parser.add_argument(
        "--pdf",
        type=str,
        default="pdf/W560.pdf",
        help="Path al file PDF da convertire (default: pdf/W560.pdf)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="docs/converted",
        help="Directory di output (default: docs/converted)"
    )
    
    args = parser.parse_args()
    
    # Converti in Path objects
    pdf_path = Path(args.pdf)
    output_dir = Path(args.output)
    
    # Validazione
    if not pdf_path.exists():
        print(f"❌ Errore: File PDF non trovato: {pdf_path}")
        sys.exit(1)
    
    # Setup
    setup_directories(output_dir)
    
    # Conversione
    try:
        convert_pdf_to_markdown(pdf_path, output_dir)
    except Exception as e:
        print(f"\n❌ Errore durante la conversione: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()