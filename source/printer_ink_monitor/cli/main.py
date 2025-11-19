#!/usr/bin/env python3
"""
CLI principale per Printer Ink Monitor
"""
import sys
import json
import logging
from pathlib import Path

# Aggiungi il path per l'import dei moduli
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.cups_handler import CupsHandler


def setup_logging(verbose: bool = False):
    """Configura il logging"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=level
    )


def list_printers():
    """Lista tutte le stampanti configurate"""
    try:
        handler = CupsHandler()
        printers = handler.get_printers()
        
        if not printers:
            print("Nessuna stampante trovata")
            return
        
        print(f"Trovate {len(printers)} stampanti:")
        print("-" * 60)
        
        for name, info in printers.items():
            status = "🟢 Online" if handler.is_printer_online(name) else "🔴 Offline"
            
            print(f"Nome: {name}")
            print(f"Modello: {info['make_model']}")
            print(f"Stato: {status} - {info['state_message']}")
            print(f"URI: {info['device_uri']}")
            if info['location']:
                print(f"Posizione: {info['location']}")
            print("-" * 60)
            
    except Exception as e:
        print(f"Errore: {e}")
        sys.exit(1)


def check_ink_levels(printer_name: str = None, output_json: bool = False):
    """Controlla i livelli di inchiostro"""
    try:
        handler = CupsHandler()
        printers = handler.get_printers()
        
        if not printers:
            print("Nessuna stampante trovata")
            return
        
        # Se non specificato, controlla tutte le stampanti
        printers_to_check = [printer_name] if printer_name else list(printers.keys())
        
        results = {}
        
        for printer in printers_to_check:
            if printer not in printers:
                print(f"Stampante '{printer}' non trovata")
                continue
            
            ink_info = handler.get_ink_levels(printer)
            results[printer] = ink_info
            
            if not output_json:
                print(f"\n=== {printer} ===")
                print(f"Modello: {printers[printer]['make_model']}")
                
                if ink_info['supported']:
                    print("Livelli inchiostro:")
                    for level in ink_info['levels']:
                        level_val = level['level']
                        if level_val >= 0:
                            percent = f"{level_val}%"
                        else:
                            percent = "N/A"
                        
                        print(f"  - {level['name']} ({level['color']}): {percent}")
                else:
                    print(f"❌ {ink_info.get('error', 'Livelli inchiostro non supportati')}")
        
        if output_json:
            print(json.dumps(results, indent=2))
            
    except Exception as e:
        print(f"Errore: {e}")
        sys.exit(1)


def main():
    """Funzione principale CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Printer Ink Monitor - Controlla i livelli di inchiostro delle stampanti",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  printer-ink-monitor list                    # Lista tutte le stampanti
  printer-ink-monitor status                  # Controlla livelli di tutte le stampanti  
  printer-ink-monitor status -p LBP2900       # Controlla solo stampante specifica
  printer-ink-monitor status --json           # Output in formato JSON
        """
    )
    
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Output verbose')
    
    subparsers = parser.add_subparsers(dest='command', help='Comandi disponibili')
    
    # Comando list
    list_parser = subparsers.add_parser('list', help='Lista stampanti configurate')
    
    # Comando status  
    status_parser = subparsers.add_parser('status', help='Controlla livelli inchiostro')
    status_parser.add_argument('-p', '--printer', type=str,
                              help='Nome stampante specifica da controllare')
    status_parser.add_argument('--json', action='store_true',
                              help='Output in formato JSON')
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    if args.command == 'list':
        list_printers()
    elif args.command == 'status':
        check_ink_levels(args.printer, args.json)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()