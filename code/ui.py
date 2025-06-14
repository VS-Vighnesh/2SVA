from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.align import Align
from rich import box
from rich.markdown import Markdown
import os

class TOTPInterface:
    def __init__(self):
        self.console = Console()
    
    def show_header(self):
        """Display the application header"""
        header = Text("🔐 TOTP 2FA Authenticator", style="bold blue")
        panel = Panel(
            Align.center(header),
            box=box.DOUBLE,
            style="blue",
            padding=(1, 2)
        )
        self.console.print(panel)
        self.console.print()
    
    def show_menu(self) -> str:
        """Display main menu and get user choice"""
        menu_table = Table(show_header=False, box=box.SIMPLE)
        menu_table.add_column("Option", style="cyan", width=10)
        menu_table.add_column("Description", style="white")
        
        menu_table.add_row("1", "Register new user")
        menu_table.add_row("2", "Login with 2FA")
        menu_table.add_row("3", "Exit")
        
        panel = Panel(
            menu_table,
            title="[bold green]Main Menu[/bold green]",
            border_style="green"
        )
        self.console.print(panel)
        
        while True:
            choice = Prompt.ask(
                "[bold yellow]Select an option[/bold yellow]",
                choices=["1", "2", "3"],
                default="3"
            )
            return choice
    
    def get_username(self, action: str = "register") -> str:
        """Get username input"""
        return Prompt.ask(f"[bold cyan]Enter username to {action}[/bold cyan]")
    
    def get_totp_code(self) -> str:
        """Get TOTP code from user"""
        return Prompt.ask("[bold yellow]Enter 6-digit TOTP code from your authenticator app[/bold yellow]")
    
    def show_qr_setup(self, username: str, qr_filename: str, provisioning_uri: str):
        """Display QR code setup instructions"""
        self.console.print()
        
        # Setup instructions
        instructions = f"""
## 📱 Setup Instructions for {username}

1. **Open your authenticator app** (Google Authenticator, Authy, etc.)
2. **Scan the QR code** saved as: `{qr_filename}`
3. **Or manually enter this key**: 
4. **Enter the 6-digit code** from your app to verify setup

**Provisioning URI (for manual setup):**
```
{provisioning_uri}
```
        """
        
        panel = Panel(
            Markdown(instructions),
            title="[bold green]📱 Authenticator Setup[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(panel)
        
        # Show QR file info
        if os.path.exists(qr_filename):
            file_info = Panel(
                f"[bold green]✅ QR Code saved as:[/bold green] [cyan]{qr_filename}[/cyan]\n"
                f"[yellow]Open this file to scan with your authenticator app[/yellow]",
                border_style="yellow"
            )
            self.console.print(file_info)
    
    def show_success(self, message: str):
        """Display success message"""
        success_panel = Panel(
            f"[bold green]✅ {message}[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(success_panel)
    
    def show_error(self, message: str):
        """Display error message"""
        error_panel = Panel(
            f"[bold red]❌ {message}[/bold red]",
            border_style="red",
            padding=(1, 2)
        )
        self.console.print(error_panel)
    
    def show_info(self, message: str):
        """Display info message"""
        info_panel = Panel(
            f"[bold blue]ℹ️ {message}[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        self.console.print(info_panel)
    
    def show_warning(self, message: str):
        """Display warning message"""
        warning_panel = Panel(
            f"[bold yellow]⚠️ {message}[/bold yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
        self.console.print(warning_panel)
    
    def confirm_action(self, message: str) -> bool:
        """Get confirmation from user"""
        return Prompt.ask(
            f"[bold yellow]{message}[/bold yellow]",
            choices=["y", "n"],
            default="n"
        ).lower() == "y"
    
    def wait_for_enter(self):
        """Wait for user to press enter"""
        Prompt.ask("[dim]Press Enter to continue...[/dim]", default="")
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_user_list(self, users: list):
        """Display list of registered users"""
        if not users:
            self.show_info("No users registered yet.")
            return
        
        user_table = Table(title="Registered Users")
        user_table.add_column("Username", style="cyan")
        
        for user in users:
            user_table.add_row(user)
        
        self.console.print(user_table)