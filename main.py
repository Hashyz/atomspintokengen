#!/usr/bin/env python3
import requests
import sys
from urllib.parse import urlparse, parse_qs


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════╗
║      AtomSpinZone Token Fetcher       ║
║         Mobile Friendly v1.0          ║
╚═══════════════════════════════════════╝{Colors.END}
""")


def print_status(msg, status="info"):
    icons = {"info": "ℹ️", "success": "✅", "error": "❌", "loading": "⏳"}
    colors = {
        "info": Colors.CYAN,
        "success": Colors.GREEN,
        "error": Colors.RED,
        "loading": Colors.YELLOW
    }
    print(f"{colors.get(status, '')}{icons.get(status, '')} {msg}{Colors.END}")


def main():
    print_banner()

    session = requests.Session()

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    session.headers.update(headers)

    try:
        print_status("Step 1: Requesting initial URL...", "loading")
        initial_url = "http://he.atomspinzone.com/home/GetGWMDN?source=https://billing.atomspinzone.com/freemium"

        response = session.get(initial_url, allow_redirects=False, timeout=30)

        if response.status_code == 302:
            location = response.headers.get('Location', '')
            print_status(f"Got redirect: {location[:50]}...", "success")

            parsed = urlparse(location)
            msisdn = parse_qs(parsed.query).get('msisdn', [None])[0]

            if msisdn:
                print_status(f"MSISDN: {msisdn}", "info")

            print_status("Step 2: Following redirect...", "loading")
            response2 = session.get(location,
                                    allow_redirects=False,
                                    timeout=30)
            print_status(f"Status: {response2.status_code}", "success")

        else:
            print_status(f"Unexpected status: {response.status_code}", "info")

        print_status("Step 3: Checking IP and getting token...", "loading")

        api_headers = {
            'User-Agent':
            'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Origin': 'https://atomspinzone.com',
            'Referer': 'https://atomspinzone.com/',
            'Authorization': ''
        }

        api_url = "https://api.atomspinzone.com/auth/check-ip"
        response3 = session.post(api_url,
                                 headers=api_headers,
                                 json={},
                                 timeout=30)

        if response3.status_code == 200:
            data = response3.json()

            if data.get('success'):
                print_status("Token fetched successfully!", "success")
                print()
                print(f"{Colors.BOLD}{'='*40}{Colors.END}")
                print(f"{Colors.GREEN}{Colors.BOLD}📱 RESULT:{Colors.END}")
                print(f"{Colors.BOLD}{'='*40}{Colors.END}")

                user_data = data.get('data', {})

                print(f"\n{Colors.YELLOW}🔑 Token (copy below):{Colors.END}")
                print(f"{Colors.BOLD}{'─'*40}{Colors.END}")
                token = user_data.get('token', 'N/A')
                print(token)
                print(f"{Colors.BOLD}{'─'*40}{Colors.END}")

                print(
                    f"\n{Colors.CYAN}📞 Phone:{Colors.END} {user_data.get('phone', 'N/A')}"
                )
                print(
                    f"{Colors.GREEN}🎰 Spins:{Colors.END} {user_data.get('spins', 0)}"
                )
                print(
                    f"{Colors.CYAN}👤 Name:{Colors.END} {user_data.get('name', 'N/A') or '(not set)'}"
                )

                print(f"\n{Colors.BOLD}{'='*40}{Colors.END}")
                print(
                    f"{Colors.GREEN}Message: {data.get('message', '')}{Colors.END}"
                )
                print(f"{Colors.BOLD}{'='*40}{Colors.END}")

                return user_data
            else:
                error_msg = data.get('message', 'Unknown error')
                if 'not found' in error_msg.lower() or 'redirect' in error_msg.lower():
                    print()
                    print(f"{Colors.RED}{Colors.BOLD}{'='*40}{Colors.END}")
                    print(f"{Colors.RED}❌ Cannot get token!{Colors.END}")
                    print(f"{Colors.RED}{'='*40}{Colors.END}")
                    print()
                    print(f"{Colors.YELLOW}📵 You are NOT using ATOM mobile data.{Colors.END}")
                    print()
                    print(f"{Colors.CYAN}To fix this:{Colors.END}")
                    print(f"   1. Turn OFF your WiFi")
                    print(f"   2. Make sure you have ATOM SIM card")
                    print(f"   3. Enable Mobile Data")
                    print(f"   4. Run this script again")
                    print()
                    print(f"{Colors.YELLOW}Note: This only works with ATOM operator.{Colors.END}")
                    print(f"{Colors.RED}{'='*40}{Colors.END}")
                else:
                    print_status(f"API Error: {error_msg}", "error")
        else:
            print_status(f"API returned status: {response3.status_code}",
                         "error")
            print(response3.text)

    except requests.exceptions.Timeout:
        print_status("Request timed out. Check your connection.", "error")
    except requests.exceptions.ConnectionError:
        print_status("Connection error. Check your network.", "error")
    except Exception as e:
        print_status(f"Error: {str(e)}", "error")

    return None


if __name__ == "__main__":
    print("\n📲 Termux-friendly script for AtomSpinZone")
    print("─" * 40)
    
    while True:
        result = main()
        if result:
            print("\n✅ Success! Press Enter to exit...")
            try:
                input()
            except:
                pass
            break
        else:
            print("\n🔄 Press Enter to try again (or type 'q' to quit)...")
            try:
                user_input = input().strip().lower()
                if user_input == 'q':
                    print("👋 Goodbye!")
                    break
                print("\n" + "─" * 40 + "\n")
            except:
                break
