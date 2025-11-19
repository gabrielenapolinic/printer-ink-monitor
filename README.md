# Printer Ink Monitor

A Python application to monitor printer ink/toner levels on Linux systems.

*Un'applicazione Python per monitorare il livello di inchiostro delle stampanti su sistemi Linux.*

## Features

- List all configured printers in the system
- Check ink/toner levels via CUPS
- Supports both text and JSON output
- Simple command-line interface

## Installation

### From source

```bash
git clone https://github.com/your-username/printer-ink-monitor
cd printer-ink-monitor
pip install .
```

### Development installation

```bash
pip install -e .
```

## Usage

### List configured printers

```bash
printer-ink-monitor list
```

### Check ink levels

```bash
# All printers
printer-ink-monitor status

# Specific printer
printer-ink-monitor status -p LBP2900
```bash
# JSON output
printer-ink-monitor status --json
```

## Demo Output

### List command
```
$ printer-ink-monitor list
Trovate 2 stampanti:
------------------------------------------------------------
Nome: LBP2900
Modello: Canon LBP-2900 CAPT GDI printer, 0.1.0
Stato: 🔴 Offline - Unplugged or turned off
URI: usb://Canon/LBP2900?serial=0000A277J9i6
------------------------------------------------------------
```

### Status with supported printer (example)
```
=== HP_OfficeJet_Pro ===
Modello: HP OfficeJet Pro 8020 series
Livelli inchiostro:
  - Black (black): 85%
  - Cyan (cyan): 42%
  - Magenta (magenta): 67%
  - Yellow (yellow): 23%
```

## Printer Compatibility

The application works with any printer configured in CUPS. However, ink level information availability depends on:

1. **Driver support**: The printer driver must provide level information
2. **Protocol**: IPP/network printers often have better support for this functionality
3. **Model**: Modern printers tend to have better support

### Printers that typically support monitoring

- HP printers with HPLIP
- Modern Epson printers
- Brother printers with IPP drivers
- Network printers with SNMP support

## Architecture

```
printer-ink-monitor/
├── src/printer_ink_monitor/
│   ├── core/           # Handlers for different protocols
│   ├── cli/            # Command-line interface
│   └── utils/          # Various utilities
├── tests/              # Automated tests
└── pyproject.toml      # Package configuration
```

## Dependencies

- **pycups**: Python interface for CUPS
- **Python 3.8+**: Minimum supported version

## System Dependencies

- **cups**: CUPS print server
- **cups-devel** (for pycups compilation if needed)

## Future Development

- [ ] SNMP support for network printers
- [ ] HPLIP integration for HP printers
- [ ] GUI with PyQt or tkinter
- [ ] Desktop notifications for low levels
- [ ] RPM packaging for Fedora/RHEL
- [ ] Support for more Linux distributions

## License

![GPLv3 License](./GPLv3_Logo.svg.png)

GPLv3 License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request
