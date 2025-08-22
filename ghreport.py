import os
import json
import getpass
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError

CONFIG_FILE = "github_config.json"

def setup_credentials():
    """One-time credential setup"""
    print("🐙 GitHub Repository Reporter")
    if os.path.exists(CONFIG_FILE):
        print("✓ Credentials already set up!")
        return
    
    print("First-time setup:")
    username = input("GitHub username: ")
    token = getpass.getpass("GitHub token: ")
    
    config = {"username": username, "token": token}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
    print("✓ Credentials saved!")

def load_credentials():
    """Load stored credentials"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        return config["username"], config["token"]
    except FileNotFoundError:
        print("❌ Run script first to set up credentials!")
        return None, None
    except:
        print("❌ Error reading credentials!")
        return None, None

def parse_repo_url(url):
    """Extract owner and repo from GitHub URL"""
    try:
        path = urllib.parse.urlparse(url).path.strip('/')
        parts = path.split('/')
        if len(parts) >= 2:
            return parts[0], parts[1]
        return None, None
    except:
        return None, None

def get_repo_report(repo_url):
    """Download repository information"""
    # Parse URL
    owner, repo = parse_repo_url(repo_url)
    if not owner or not repo:
        print("❌ Invalid GitHub URL!")
        return
    
    # Load credentials
    username, token = load_credentials()
    if not username or not token:
        return
    
    # Create request
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(api_url)
    req.add_header("Authorization", f"token {token}")
    
    try:
        # Fetch data
        print(f"📥 Fetching: {owner}/{repo}")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        # Create report
        report = {
            "name": data["name"],
            "owner": data["owner"]["login"],
            "description": data["description"] or "No description",
            "language": data["language"] or "Not specified",
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "issues": data["open_issues_count"],
            "url": data["html_url"],
            "created": data["created_at"][:10],
            "updated": data["updated_at"][:10]
        }
        
        # Save report
        filename = f"{owner}_{repo}_report.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Saved: {filename}")
        print(f"📋 {report['name']} by {report['owner']}")
        print(f"   ⭐ {report['stars']} stars | 🍴 {report['forks']} forks")
        
    except HTTPError as e:
        if e.code == 401:
            print("❌ Authentication failed! Check token.")
        elif e.code == 403:
            print("❌ API rate limit or access denied!")
        elif e.code == 404:
            print("❌ Repository not found or access denied!")
        else:
            print(f"❌ HTTP Error: {e.code}")
    except URLError:
        print("❌ Network error! Check connection.")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_help():
    """Show available commands"""
    print("Commands:")
    print("  get <url>   - Download repository report")
    print("  help        - Show this help")
    print("  exit        - Exit program")

def main():
    """Main program loop"""
    setup_credentials()
    print("\nType 'help' for commands\n")
    
    while True:
        try:
            cmd = input("> ").strip().split()
            if not cmd:
                continue
                
            if cmd[0] == "get":
                if len(cmd) > 1:
                    get_repo_report(cmd[1])
                else:
                    print("❌ Usage: get <repository_url>")
            elif cmd[0] == "help":
                show_help()
            elif cmd[0] == "exit":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Unknown command! Type 'help' for commands.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
