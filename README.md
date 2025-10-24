# 📚 Omron Command Reference - Markdown

> Conversione automatica della manualistica Omron da PDF a Markdown

[![Convert PDF](https://github.com/DFFM-maker/omron-command-reference-md/actions/workflows/convert-pdf.yml/badge.svg)](https://github.com/DFFM-maker/omron-command-reference-md/actions/workflows/convert-pdf.yml)

## 🎯 Obiettivo

Questo repository contiene la manualistica tecnica Omron convertita in formato Markdown per una consultazione più facile e ricercabile.

## 📁 Struttura

```
omron-command-reference-md/
├── .github/workflows/     # Automazione GitHub Actions
├── pdf/                   # PDF originali
├── docs/converted/        # Markdown convertiti
├── scripts/              # Script di conversione
│   ├── convert.py        # Conversione PDF → Markdown
│   ├── post_process.py   # Post-processing
│   └── requirements.txt  # Dipendenze Python
└── README.md
```

## 🚀 Utilizzo

### Conversione Manuale

1. **Installa le dipendenze:**
   ```bash
   pip install -r scripts/requirements.txt
   ```

2. **Converti il PDF:**
   ```bash
   python scripts/convert.py --pdf pdf/W560.pdf --output docs/converted
   ```

3. **Post-processa il Markdown:**
   ```bash
   python scripts/post_process.py --input docs/converted/W560.md
   ```

### Conversione Automatica

Il workflow GitHub Actions si attiva automaticamente quando:
- Viene caricato/modificato un PDF nella cartella `pdf/`
- Viene eseguito manualmente dalla tab Actions

## 🛠️ Tecnologie

- **[Marker](https://github.com/datalab-to/marker)**: Conversione PDF → Markdown
- **Python 3.11+**: Script di processing
- **GitHub Actions**: Automazione CI/CD

## 📖 Documentazione Convertita

- [W560 Command Reference](docs/converted/W560.md)

## 🤝 Contributi

Per aggiungere nuovi manuali:
1. Carica il PDF nella cartella `pdf/`
2. Il workflow convertirà automaticamente il documento
3. Controlla il risultato in `docs/converted/`

## 📝 Note

- I PDF vengono convertiti con supporto per italiano e inglese
- Le immagini vengono estratte nella cartella `docs/converted/images/`
- I comandi Omron vengono formattati automaticamente

## 📄 Licenza

Questo repository contiene documentazione tecnica Omron. I diritti sui contenuti originali appartengono a Omron Corporation.

---

**Generato con ❤️ usando [Marker](https://github.com/datalab-to/marker)**