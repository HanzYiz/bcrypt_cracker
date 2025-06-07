#!/usr/bin/env python3
import bcrypt
import argparse
from datetime import datetime
import multiprocessing
import sys
import os
from tqdm import tqdm
import signal

def check_password(args):
    target_hash, password = args
    try:
        if bcrypt.checkpw(password.encode('utf-8'), target_hash):
            return password
    except (ValueError, UnicodeEncodeError):
        pass
    return None

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def crack_bcrypt(target_hash, wordlist_path, max_processes=None):
    if not os.path.exists(wordlist_path):
        print(f"\n[!] Error: Wordlist file '{wordlist_path}' not found!")
        sys.exit(1)

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"\n[!] Error reading wordlist: {str(e)}")
        sys.exit(1)

    total_passwords = len(passwords)
    start_time = datetime.now()

    print(f"\n[•] Starting attack on hash: {target_hash.decode()}")
    print(f"[•] Loaded {total_passwords:,} passwords from {wordlist_path}")
    print(f"[•] Using {max_processes or multiprocessing.cpu_count()} processes\n")

    with multiprocessing.Pool(processes=max_processes, initializer=init_worker) as pool:
        try:
            args = ((target_hash, pwd) for pwd in passwords)
            
            for result in tqdm(pool.imap_unordered(check_password, args),
                               total=total_passwords,
                               desc="Cracking progress",
                               unit="passwords"):
                if result is not None:
                    pool.terminate()
                    time_elapsed = datetime.now() - start_time
                    return (True, result, total_passwords, time_elapsed)
        
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
            print("\n[!] Crack interrupted by user. Shutting down gracefully.")
            sys.exit(0)
    
    time_elapsed = datetime.now() - start_time
    return (False, None, total_passwords, time_elapsed)

def main():
    parser = argparse.ArgumentParser(
        usage='python %(prog)s [OPTIONS] <HASH> <WORDLIST>',
        description='==== Bcrypt Hash Cracker ====',
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    
    parser.add_argument(
        'hash', 
        help='Hash bcrypt yang akan di-crack (format: $2a$12$...)'
    )
    parser.add_argument(
        'wordlist', 
        help='Path ke file wordlist (contoh: rockyou.txt)'
    )
    parser.add_argument(
        '-p', '--processes', 
        type=int,
        default=multiprocessing.cpu_count(),
        help='Number of processes to use (default: all CPU cores)'
    )
    parser.add_argument(
        '-h', '--help', 
        action='help',
        default=argparse.SUPPRESS,
        help='Show this help message and exit'
    )
    if len(sys.argv) < 2:
        parser.print_help()
        print("\n[!] Error: You must provide both hash and wordlist arguments!")
        print("Example usage:")
        print("  python bcrypt_cracker.py '$2a$12$...' wordlist.txt")
        print("  python bcrypt_cracker.py '$2b$10$...' passwords.txt -p 8")
        sys.exit(1)

    args = parser.parse_args()

    try:
        target_hash = args.hash.encode() if isinstance(args.hash, str) else args.hash
        
        if not target_hash.startswith((b'$2a$', b'$2b$', b'$2y$')):
            print("\n[!] Error: Invalid bcrypt hash format (should start with $2a$, $2b$ or $2y$)")
            sys.exit(1)
        
        success, password, attempts, time_elapsed = crack_bcrypt(
            target_hash, args.wordlist, args.processes)
        
        print("\n" + "="*50)
        if success:
            print(f"[✓] PASSWORD FOUND: {password}")
        else:
            print("[✗] Password not found in wordlist")
        
        print(f"\nTotal attempts: {attempts:,}")
        print(f"Time elapsed: {time_elapsed}")
        print(f"Speed: {attempts/max(1, time_elapsed.total_seconds()):.1f} attempts/sec")
        print("="*50)
        
    except SystemExit:
        pass
    except Exception as e:
        print(f"\n[!] Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()