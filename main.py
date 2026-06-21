#!/usr/bin/env python3
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from core import GitScanner, SecretScanner, CommitGenerator

console = Console()

def print_banner():
    banner = Text("⚡ COMMIT-SENSE ⚡\nAI & Security Git Hook", style="bold cyan", justify="center")
    console.print(Panel(banner, border_style="bright_magenta"))

def run():
    print_banner()
    
    console.print("[yellow]🔍 Analyzing Git Staging Area...[/yellow]")
    diff_text = GitScanner.get_staged_diff()
    
    if not diff_text:
        console.print("[dim]No staged changes found. Use 'git add' first.[/dim]")
        sys.exit(0)

    # 1. Security Scan
    findings = SecretScanner.scan(diff_text)
    if findings:
        console.print("\n[bold red]🚨 ACTION ABORTED: Security Risk Detected![/bold red]")
        console.print("[red]The following secrets were found in your staged files:[/red]\n")
        for secret_type, line in findings:
            console.print(f"  - [bold yellow]{secret_type}[/bold yellow]: {line}")
        console.print("\n[red]Please remove these secrets from your code before committing.[/red]")
        sys.exit(1)
        
    console.print("[green]✔ Clean: No secrets detected.[/green]\n")

    # 2. AI Commit Generation
    console.print("[cyan]🤖 Generating Smart Commit Message...[/cyan]")
    commit_msg = CommitGenerator.generate_from_diff(diff_text)
    
    console.print(f"\n[bold green]Suggested Commit:[/bold green] {commit_msg}")
    
    # In a real environment, we would use subprocess to actually commit here if the user approves.
    # For now, we output it.
    console.print("\n[dim]To use this message, run:[/dim]")
    console.print(f"[bold cyan]git commit -m \"{commit_msg}\"[/bold cyan]\n")

if __name__ == "__main__":
    run()
