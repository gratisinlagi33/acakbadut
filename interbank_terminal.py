#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║          INTERBANK SETTLEMENT TERMINAL - SIMULATION ENGINE          ║
║                     Version 2.0 | Build 2026.05                     ║
║                                                                      ║
║  DISCLAIMER: This is a SIMULATION/DEMONSTRATION tool only.           ║
║  No real banking transactions are performed.                         ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import time
import random
import os
import sys
import hashlib
import datetime

# =====================================================================
# [ CONFIGURATION ]
# =====================================================================
CONFIG = {
    "target_bank": "HSBC",
    "target_account_last4": "1411",
    "target_balance_eur": 14_564_000,
    "beneficiary_name": "JOHN DOE",
    "currency": "EUR",
    "session_timeout": 300,  # seconds
}

# Credentials (hashed for "security" simulation)
CREDENTIALS = {
    "username": "admin",
    "password_hash": hashlib.sha256("admin".encode()).hexdigest(),
}

# Global Bank Registry
BANK_REGISTRY = [
    "AFFIN", "HSBC", "CHASE", "CITI", "BARCLAYS",
    "BOC", "DBS", "MUFG", "SANTANDER", "ING",
    "SCB", "DEUTSCHE", "UBS", "WELLS", "JPMORGAN",
    "BNP PARIBAS", "CREDIT SUISSE", "GOLDMAN SACHS",
]

# Supported Crypto Assets
SUPPORTED_ASSETS = ["USDT", "BTC", "ETH"]

# BTC approximate rate (simulation)
CRYPTO_RATES = {
    "BTC": 68_500.00,
    "ETH": 3_850.00,
    "USDT": 1.00,
}


# =====================================================================
# [ TERMINAL COLORS & STYLING ]
# =====================================================================
class Style:
    """ANSI escape codes for terminal styling."""
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    @staticmethod
    def init():
        """Enable ANSI on Windows."""
        if os.name == 'nt':
            os.system('')


# =====================================================================
# [ UTILITY FUNCTIONS ]
# =====================================================================
def clear():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def timestamp():
    """Get current timestamp string."""
    return datetime.datetime.now().strftime("%H:%M:%S")


def print_header(title, subtitle=None, width=60):
    """Print a formatted header box."""
    border = "═" * width
    print(f"\n{Style.CYAN}{Style.BOLD}╔{border}╗{Style.RESET}")
    padding = (width - len(title)) // 2
    print(f"{Style.CYAN}{Style.BOLD}║{' ' * padding}{Style.WHITE}{title}{Style.CYAN}{' ' * (width - padding - len(title))}║{Style.RESET}")
    if subtitle:
        padding_s = (width - len(subtitle)) // 2
        print(f"{Style.CYAN}{Style.BOLD}║{Style.DIM}{' ' * padding_s}{subtitle}{' ' * (width - padding_s - len(subtitle))}{Style.CYAN}{Style.BOLD}║{Style.RESET}")
    print(f"{Style.CYAN}{Style.BOLD}╚{border}╝{Style.RESET}")


def print_separator(width=60, char="─"):
    """Print a separator line."""
    print(f"{Style.DIM}{char * width}{Style.RESET}")


def print_status(tag, message, status=None, color=Style.CYAN):
    """Print a formatted status message."""
    tag_str = f"{color}[{tag}]{Style.RESET}"
    if status:
        status_color = Style.GREEN if status == "OK" else Style.RED if status == "FAIL" else Style.YELLOW
        print(f"  {tag_str} {message} {status_color}[{status}]{Style.RESET}")
    else:
        print(f"  {tag_str} {message}")


def slow_print(text, delay=0.06, color=Style.RESET):
    """Print text character by character with delay."""
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(Style.RESET + '\n')


def progress_bar(label, duration=3.0, width=30, color=Style.GREEN):
    """Display an animated progress bar."""
    sys.stdout.write(f"  {Style.CYAN}[SYS]{Style.RESET} {label}: [")
    sys.stdout.flush()
    step_delay = duration / width
    for i in range(width):
        sys.stdout.write(f"{color}█{Style.RESET}")
        sys.stdout.flush()
        time.sleep(step_delay)
    sys.stdout.write(f"] {Style.GREEN}100%{Style.RESET}\n")


def spinner(label, duration=2.0, color=Style.CYAN):
    """Display a spinner animation."""
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start = time.time()
    i = 0
    while time.time() - start < duration:
        sys.stdout.write(f"\r  {color}[{chars[i % len(chars)]}]{Style.RESET} {label}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r  {Style.GREEN}[✓]{Style.RESET} {label}\n")


def get_masked_input(prompt=""):
    """Get password input with masking (cross-platform)."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    password = ""

    if os.name == 'nt':
        import msvcrt
        while True:
            ch = msvcrt.getch()
            if ch in (b'\r', b'\n'):
                sys.stdout.write('\n')
                break
            elif ch == b'\x08':
                if password:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            elif ch not in (b'\x00', b'\xe0'):
                password += ch.decode('utf-8', errors='ignore')
                sys.stdout.write('•')
                sys.stdout.flush()
    else:
        try:
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                while True:
                    ch = sys.stdin.read(1)
                    if ch in ('\r', '\n'):
                        sys.stdout.write('\r\n')
                        break
                    elif ch in ('\x7f', '\x08'):
                        if password:
                            password = password[:-1]
                            sys.stdout.write('\b \b')
                            sys.stdout.flush()
                    elif ch == '\x03':  # Ctrl+C
                        sys.stdout.write('\r\n')
                        raise KeyboardInterrupt
                    else:
                        password += ch
                        sys.stdout.write('•')
                        sys.stdout.flush()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except (ImportError, OSError):
            # Fallback for environments without tty support
            import getpass
            password = getpass.getpass(prompt="")

    return password


def generate_session_id():
    """Generate a unique session ID."""
    seed = f"{time.time()}{random.randint(0, 99999)}"
    return hashlib.md5(seed.encode()).hexdigest()[:16].upper()


def generate_transaction_row():
    """Generate a randomized transaction row for the live feed."""
    trn = f"TRN-{random.randint(1000, 9999)}-{random.choice('ABCDEF')}{random.randint(10, 99)}"
    bank = random.choice(BANK_REGISTRY)
    amount = random.randint(50_000, 9_999_999)
    masked_acc = f"{bank}-{'*' * 8}"
    return (
        f"  {Style.DIM}│{Style.RESET} "
        f"{Style.YELLOW}{trn:<18}{Style.RESET} "
        f"{Style.DIM}│{Style.RESET} "
        f"{Style.CYAN}{masked_acc:<20}{Style.RESET} "
        f"{Style.DIM}│{Style.RESET} "
        f"{Style.WHITE}{amount:>12,} EUR{Style.RESET} "
        f"{Style.DIM}│{Style.RESET}"
    )


# =====================================================================
# [ PHASE 1: SECURE CONNECTION ESTABLISHMENT ]
# =====================================================================
def phase_connection():
    """Simulate establishing a secure interbank connection."""
    clear()
    print_header("SECURE INTERBANK PROTOCOL", "Establishing Encrypted Connection")
    print()

    spinner("Initializing RSA-4096 Encrypted Handshake", 1.5)

    modules = [
        ("Mounting SWIFT MT103/GPI Gateway Ledger", "OK"),
        ("Validating X.509 Certificate Chain", "OK"),
        ("Binding to Regional Core Node (EU-WEST)", "OK"),
        ("Allocating Secure Memory Partition", "OK"),
        ("Synchronizing NTP Clock Reference", "OK"),
        ("Establishing End-to-End Tunnel", "OK"),
    ]

    for module, status in modules:
        print_status("SYS", module, status)
        time.sleep(0.4)

    print()
    progress_bar("Synchronizing Mainframe Session", duration=2.5)
    print()
    print(f"  {Style.GREEN}{Style.BOLD}[✓] CONNECTION ESTABLISHED — SECURE CHANNEL ACTIVE{Style.RESET}")
    time.sleep(1.0)


# =====================================================================
# [ PHASE 2: AUTHENTICATION ]
# =====================================================================
def phase_authentication():
    """Handle user login with credential verification."""
    clear()
    print_header("AUTHENTICATION GATEWAY", "Multi-Factor Verification Required")
    print()
    print(f"  {Style.DIM}Session initiated at {timestamp()}{Style.RESET}")
    print(f"  {Style.DIM}Protocol: TLS 1.3 | Cipher: AES-256-GCM-SHA384{Style.RESET}")
    print()
    print_separator()
    print()

    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        username = input(f"  {Style.YELLOW}▸ Username : {Style.RESET}")
        password = get_masked_input(f"  {Style.YELLOW}▸ Password : {Style.RESET}")

        # Verify credentials
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if username == CREDENTIALS["username"] and password_hash == CREDENTIALS["password_hash"]:
            print()
            print(f"  {Style.GREEN}[✓] Authentication successful.{Style.RESET}")
            time.sleep(0.8)
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print(f"\n  {Style.RED}[✗] Invalid credentials. {remaining} attempt(s) remaining.{Style.RESET}\n")

    print(f"\n  {Style.RED}{Style.BOLD}[!] Maximum attempts exceeded. Terminal locked.{Style.RESET}")
    time.sleep(2)
    return False


# =====================================================================
# [ PHASE 3: ENVIRONMENT VERIFICATION ]
# =====================================================================
def phase_environment_check():
    """Simulate security environment verification."""
    clear()
    print_header("SECURITY VALIDATION", "Environment Fingerprint Analysis")
    print()

    checks = [
        ("Analyzing Client Environment Fingerprint", "VERIFIED"),
        ("Validating Session Token Integrity", "VERIFIED"),
        ("Checking Geo-IP Compliance (Whitelist)", "VERIFIED"),
        ("Scanning for MITM Attack Vectors", "CLEAN"),
        ("Verifying Hardware Security Module (HSM)", "ACTIVE"),
    ]

    for check, status in checks:
        spinner(check, 0.8)
        time.sleep(0.2)

    print()
    print_status("SEC", "Masking Client IP via Secure Proxy", "OK", Style.BLUE)
    time.sleep(0.5)
    print_status("SEC", "Allocating Encrypted VPS Instance", "OK", Style.BLUE)
    time.sleep(0.5)
    print_status("SEC", "Purging Ephemeral Session Artifacts", "OK", Style.BLUE)
    time.sleep(0.5)

    print()
    session_id = generate_session_id()
    print(f"  {Style.DIM}Session ID: {session_id}{Style.RESET}")
    print(f"\n  {Style.GREEN}{Style.BOLD}[✓] ENVIRONMENT SECURE — PROCEEDING TO COMMAND CENTER{Style.RESET}")
    time.sleep(1.0)


# =====================================================================
# [ PHASE 4: DEEP TRACE PROTOCOL ]
# =====================================================================
def phase_deep_trace():
    """Simulate the deep fund tracing protocol."""
    clear()
    print_header("COMMAND CENTER", "Global Interbank Operations")
    print()
    print(f"  {Style.GREEN}[ACTIVE]{Style.RESET} Deep Fund Tracing Protocol v3.2")
    print(f"  {Style.DIM}Timestamp: {timestamp()} | Network: SWIFT-GPI{Style.RESET}")
    print()
    print_separator()
    print()

    trn_input = input(f"  {Style.YELLOW}▸ Enter Target TRN Code : {Style.RESET}")

    if not trn_input.strip():
        trn_input = f"TRN-{random.randint(1000, 9999)}-AUTO"
        print(f"  {Style.DIM}  (Auto-generated: {trn_input}){Style.RESET}")

    time.sleep(0.5)
    clear()

    # --- Live Network Feed ---
    print_header("LIVE TRANSACTION NETWORK", "Global Mutation Feed — Real-Time")
    print()
    print(f"  {Style.CYAN}[SYS]{Style.RESET} Locking Target TRN: {Style.YELLOW}{trn_input}{Style.RESET}")
    time.sleep(0.8)

    spinner("Deploying trace algorithms across network nodes", 1.5)
    print()

    # Table header
    print(f"  {Style.DIM}┌{'─' * 18}┬{'─' * 22}┬{'─' * 17}┐{Style.RESET}")
    print(f"  {Style.DIM}│{Style.BOLD} {'TRN CODE':<16} {Style.DIM}│{Style.BOLD} {'SOURCE BANK':<20} {Style.DIM}│{Style.BOLD} {'AMOUNT':>15} {Style.DIM}│{Style.RESET}")
    print(f"  {Style.DIM}├{'─' * 18}┼{'─' * 22}┼{'─' * 17}┤{Style.RESET}")

    # Streaming data
    start_time = time.time()
    feed_duration = 8
    while time.time() - start_time < feed_duration:
        print(generate_transaction_row())
        time.sleep(0.05)

    print(f"  {Style.DIM}└{'─' * 18}┴{'─' * 22}┴{'─' * 17}┘{Style.RESET}")

    # --- Match Found ---
    print()
    time.sleep(0.5)
    print(f"\a  {Style.RED}{Style.BOLD}  ⚠  SIGNAL INTERCEPTED — DATA ANOMALY DETECTED  ⚠{Style.RESET}")
    time.sleep(1.0)
    print()
    slow_print("  [ALERT] Encrypted packet payload matched target signature...", 0.04, Style.YELLOW)
    time.sleep(0.5)

    spinner("Decrypting target ledger entry", 2.0)
    print()

    # Display found data
    found_bank = f"{CONFIG['target_bank']}-****{CONFIG['target_account_last4']}"
    balance = CONFIG["target_balance_eur"]

    print_separator()
    print(f"  {Style.BOLD}  TARGET ACCOUNT  : {Style.CYAN}{found_bank}{Style.RESET}")
    time.sleep(0.5)
    print(f"  {Style.BOLD}  TOTAL BALANCE   : {Style.GREEN}{CONFIG['currency']} {balance:,.2f}{Style.RESET}")
    time.sleep(0.5)
    print(f"  {Style.BOLD}  BENEFICIARY     : {Style.WHITE}{CONFIG['beneficiary_name']}{Style.RESET}")
    time.sleep(0.5)
    print(f"  {Style.BOLD}  STATUS          : {Style.GREEN}VERIFIED & LOCKED{Style.RESET}")
    print_separator()

    print(f"\n  {Style.GREEN}{Style.BOLD}[✓] Funds totaling {CONFIG['currency']} {balance:,.2f} secured in escrow.{Style.RESET}")
    time.sleep(1.5)

    return trn_input


# =====================================================================
# [ PHASE 5: MANUAL BANK ROUTING ]
# =====================================================================
def phase_bank_routing():
    """Collect destination bank routing information."""
    clear()
    print_header("BANK ROUTING MODULE", "Manual Settlement Configuration")
    print()
    print(f"  {Style.DIM}Configure destination for fund settlement.{Style.RESET}")
    print()
    print_separator()
    print()

    bank_name = input(f"  {Style.YELLOW}▸ Destination Bank Name : {Style.RESET}")
    account_no = input(f"  {Style.YELLOW}▸ Account Number        : {Style.RESET}")
    swift_code = input(f"  {Style.YELLOW}▸ SWIFT/BIC Code        : {Style.RESET}")

    # Validation
    if not bank_name.strip() or not account_no.strip() or not swift_code.strip():
        print(f"\n  {Style.RED}[!] All fields are required. Using placeholder data.{Style.RESET}")
        bank_name = bank_name or "UNKNOWN"
        account_no = account_no or "0000000000"
        swift_code = swift_code or "XXXXXXXXX"

    print()
    spinner("Verifying bank routing via Global Mainframe", 2.0)
    print()

    # Mask account number for display
    if len(account_no) > 4:
        masked_account = '*' * (len(account_no) - 4) + account_no[-4:]
    else:
        masked_account = '*' * len(account_no)

    # Confirmation display
    print_separator()
    print(f"\n  {Style.GREEN}{Style.BOLD}  ✓ BANK ROUTING VERIFIED{Style.RESET}\n")
    print(f"  {Style.BOLD}  Bank         : {Style.WHITE}{bank_name.upper()}{Style.RESET}")
    print(f"  {Style.BOLD}  Account      : {Style.WHITE}{masked_account}{Style.RESET}")
    print(f"  {Style.BOLD}  SWIFT/BIC    : {Style.WHITE}{swift_code.upper()}{Style.RESET}")
    print(f"  {Style.BOLD}  Beneficiary  : {Style.WHITE}{CONFIG['beneficiary_name']}{Style.RESET}")
    print()
    print_separator()

    input(f"\n  {Style.YELLOW}▸ Press ENTER to proceed to settlement bridge...{Style.RESET}")

    return {
        "bank_name": bank_name.upper(),
        "account_no": account_no,
        "masked_account": masked_account,
        "swift_code": swift_code.upper(),
    }


# =====================================================================
# [ PHASE 6: SETTLEMENT BRIDGE ]
# =====================================================================
def phase_settlement_bridge():
    """Simulate the settlement bridge connection."""
    clear()
    print_header("SETTLEMENT BRIDGE", "Decentralized Network Router")
    print()

    spinner("Pinging CryptoHost Settlement Gateway", 1.5)

    firewalls = [
        "SWIFT-SEC-NODE",
        "FED-RESERVE-BRIDGE",
        "INTERPOL-MONITOR-V2",
        "COLD-WALLET-GATE",
        "TREASURY-UPLINK",
    ]

    print()
    print(f"  {Style.CYAN}[BRIDGE]{Style.RESET} Traversing institutional security layers:")
    print()
    for fw in firewalls:
        print_status("→", f"Negotiating with {fw:<22}", "PASSED", Style.BLUE)
        time.sleep(0.4)

    print()
    spinner("Overriding Escrow Multi-Signature Lock", 2.0)
    progress_bar("Syncing Settlement Tunnel", duration=2.0)
    print()
    print(f"  {Style.GREEN}{Style.BOLD}[✓] SETTLEMENT BRIDGE ACTIVE — CRYPTOHOST READY{Style.RESET}")
    time.sleep(1.0)


# =====================================================================
# [ PHASE 7: CRYPTO SETTLEMENT (with intentional failure) ]
# =====================================================================
def phase_crypto_settlement(routing_info):
    """Simulate crypto settlement process (always fails by design)."""
    clear()
    print_header("CRYPTOHOST SETTLEMENT", "Blockchain Network Bridge")
    print()
    print(f"  {Style.DIM}Available assets: {', '.join(SUPPORTED_ASSETS)}{Style.RESET}")
    print()
    print_separator()
    print()

    wallet_address = input(f"  {Style.YELLOW}▸ Destination Wallet Address : {Style.RESET}")
    coin_choice = input(f"  {Style.YELLOW}▸ Select Asset ({'/'.join(SUPPORTED_ASSETS)})   : {Style.RESET}").upper().strip()

    # Validate asset selection
    if coin_choice not in SUPPORTED_ASSETS:
        print(f"  {Style.YELLOW}  (Invalid selection, defaulting to USDT){Style.RESET}")
        coin_choice = "USDT"

    if not wallet_address.strip():
        wallet_address = "0x" + hashlib.md5(str(time.time()).encode()).hexdigest()[:40]
        print(f"  {Style.DIM}  (Auto-generated: {wallet_address}){Style.RESET}")

    balance = CONFIG["target_balance_eur"]
    rate = CRYPTO_RATES.get(coin_choice, 1.0)
    crypto_amount = balance / rate

    print()
    print(f"  {Style.CYAN}[SYS]{Style.RESET} Initiating blockchain network bridge...")
    time.sleep(1.0)
    print(f"  {Style.CYAN}[SYS]{Style.RESET} Conversion: {Style.GREEN}{CONFIG['currency']} {balance:,.2f}{Style.RESET} → {Style.GREEN}{crypto_amount:,.4f} {coin_choice}{Style.RESET}")
    print(f"  {Style.DIM}        Rate: 1 {coin_choice} = {CONFIG['currency']} {rate:,.2f}{Style.RESET}")
    time.sleep(1.0)

    # Progress bar that "fails" at ~78%
    print()
    sys.stdout.write(f"  {Style.CYAN}[SYS]{Style.RESET} Broadcasting to decentralized ledger: [")
    sys.stdout.flush()
    fail_point = 23  # out of 30
    for i in range(fail_point):
        sys.stdout.write(f"{Style.GREEN}█{Style.RESET}")
        sys.stdout.flush()
        time.sleep(0.2)

    # Simulate failure
    time.sleep(1.5)
    for i in range(3):
        sys.stdout.write(f"{Style.RED}█{Style.RESET}")
        sys.stdout.flush()
        time.sleep(0.5)

    remaining = 30 - fail_point - 3
    sys.stdout.write(f"{Style.DIM}{'░' * remaining}{Style.RESET}] {Style.RED}FAILED{Style.RESET}\n")
    time.sleep(0.8)

    # Error output
    print()
    print(f"  {Style.RED}[✗] CRITICAL: Uplink connection severed at 78%{Style.RESET}")
    time.sleep(0.5)
    print(f"  {Style.RED}[✗] SYNC FAILED: Remote node rejected encrypted packet{Style.RESET}")
    time.sleep(1.0)

    # Final failure report
    print()
    error_code = f"ERR_BRIDGE_TIMEOUT_0x{random.randint(1000, 9999):04X}"
    print_separator(60, "═")
    print(f"\n  {Style.RED}{Style.BOLD}  ╳  SETTLEMENT FAILED  ╳{Style.RESET}\n")
    print(f"  {Style.BOLD}  Reason       : {Style.RED}Network handshake aborted by remote node{Style.RESET}")
    print(f"  {Style.BOLD}  Error Code   : {Style.YELLOW}{error_code}{Style.RESET}")
    print(f"  {Style.BOLD}  Beneficiary  : {Style.WHITE}{CONFIG['beneficiary_name']}{Style.RESET}")
    print(f"  {Style.BOLD}  Bank Route   : {Style.WHITE}{routing_info['bank_name']} ({routing_info['masked_account']}){Style.RESET}")
    print(f"  {Style.BOLD}  Target Vault : {Style.CYAN}{wallet_address}{Style.RESET}")
    print(f"  {Style.BOLD}  Amount       : {Style.WHITE}{crypto_amount:,.4f} {coin_choice}{Style.RESET}")
    print(f"  {Style.BOLD}  Status       : {Style.RED}ROLLBACK — FUNDS RETAINED IN ESCROW{Style.RESET}")
    print()
    print_separator(60, "═")
    print()
    print(f"  {Style.DIM}Secure connection terminated. Session ended at {timestamp()}.{Style.RESET}")
    print()


# =====================================================================
# [ MAIN EXECUTION ]
# =====================================================================
def main():
    """Main execution flow."""
    Style.init()

    # Phase 1: Connection
    phase_connection()

    # Phase 2: Authentication
    clear()
    if not phase_authentication():
        clear()
        print(f"\n  {Style.RED}{Style.BOLD}[TERMINAL LOCKED] Too many failed attempts.{Style.RESET}")
        print(f"  {Style.DIM}Contact system administrator for access recovery.{Style.RESET}\n")
        sys.exit(1)

    # Phase 3: Environment Check
    phase_environment_check()

    # Phase 4: Deep Trace
    trn_code = phase_deep_trace()

    # Phase 5: Bank Routing
    routing_info = phase_bank_routing()

    # Phase 6: Settlement Bridge
    phase_settlement_bridge()

    # Phase 7: Crypto Settlement
    phase_crypto_settlement(routing_info)


# =====================================================================
# [ ENTRY POINT ]
# =====================================================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {Style.RED}[!] Session terminated by user.{Style.RESET}")
        print(f"  {Style.DIM}All ephemeral data purged.{Style.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {Style.RED}[FATAL] Unexpected error: {e}{Style.RESET}")
        print(f"  {Style.DIM}Please restart the terminal.{Style.RESET}\n")
        sys.exit(1)
