# Git-provat-repo# GitHub Repository Reporter

A simple Python tool to download repository information from GitHub with secure credential handling.

## Features
- One-time credential setup
- Download public/private repository reports
- No external dependencies (uses only built-in libraries)
- Secure credential storage
- Simple command interface

## Installation
Save the script as `ghreport.py`

## Setup (One-time Only)
1. Create a GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Generate new token with appropriate scopes:
     - `public_repo` for public repositories
     - `repo` for private repositories
   - Copy the generated token

2. Run the script for first-time setup:
   ```bash
   python ghreport.py
   ```

## Commands
| Command | Description |
|---------|-------------|
| `get <URL>` | Download repository report |
| `help` | Show available commands |
| `exit` | Exit the program |

## Usage Examples

### First Run (Credential Setup)
```bash
$ python ghreport.py
🐙 GitHub Repository Reporter
GitHub username: yourusername
GitHub token: ****************
✓ Credentials saved!
> get https://github.com/user/private-repo
📥 Fetching: user/private-repo
✅ Saved: user_private-repo_report.json
```

### Subsequent Runs
```bash
$ python ghreport.py
🐙 GitHub Repository Reporter
> get https://github.com/python/cpython
📥 Fetching: python/cpython
✅ Saved: python_cpython_report.json
```

## Report Contents
The downloaded JSON report includes:
- Repository name
- Owner
- Description
- Primary language
- Stars count
- Forks count
- Open issues
- Repository URL
- Creation date
- Last update

## Security Notes
- Credentials stored in `github_config.json`
- Use Personal Access Tokens instead of passwords
- Add `github_config.json` to `.gitignore`
- Token permissions should be minimal

## Requirements
- Python 3.x (no external packages needed)

## Quick Start
1. Save as `ghreport.py`
2. First run: `python ghreport.py` (sets up credentials)
3. Download reports: `get https://github.com/user/repo`

## Notes
- Works with both public and private repositories
- Limited by GitHub API rate limits (5000 requests/hour)
- Credentials are stored locally in `github_config.json`
- For private repositories, ensure your token has `repo` scope
