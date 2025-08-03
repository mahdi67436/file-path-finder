import os
import time
import threading
import platform
import subprocess
from queue import Queue
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
import pyfiglet

console = Console()

def print_mr_hacker():
    ascii_art = pyfiglet.figlet_format("H4X CHEAT")
    console.print(f"[bold red]{ascii_art}[/bold red]")

def open_folder(path):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(f'explorer /select,"{path}"')
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-R", path])
        else:
            subprocess.Popen(["xdg-open", os.path.dirname(path)])
    except Exception as e:
        console.print(f"[red]Could not open folder for: {path}[/red]")

def enqueue_folders(start_folder, queue, exclude_dirs):
    """Recursive enqueue all folders except excluded ones"""
    for root, dirs, files in os.walk(start_folder):
        # Filter excluded dirs in-place to avoid walking into them
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        queue.put(root)

def search_files(queue, results, search_term, search_type, exts, stop_time, progress_task, progress, lock):
    while not queue.empty() and time.time() < stop_time:
        folder = queue.get()
        try:
            files = os.listdir(folder)
        except Exception:
            queue.task_done()
            continue
        
        for file in files:
            if self_stop.is_set() or time.time() > stop_time:
                break
            
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                # Extension filter
                if exts and not any(file.lower().endswith(e.lower()) for e in exts):
                    continue
                
                # Match check
                if search_type == "exact":
                    match = file.lower() == search_term.lower()
                else:
                    match = search_term.lower() in file.lower()
                
                if match:
                    with lock:
                        if full_path not in results:
                            results.append(full_path)
                            console.log(f"[green]Found:[/green] {full_path}")
        progress.advance(progress_task)
        queue.task_done()

def main():
    print_mr_hacker()
    console.print("[bold cyan]=== Advanced File Path Finder ===[/bold cyan]\n")
    
    folder = console.input("[yellow]Enter folder path to search in:[/yellow] ").strip()
    if not os.path.exists(folder):
        console.print("[red]That folder doesn't exist. Exiting.[/red]")
        return
    
    search_term = console.input("[yellow]Enter file name or text to search for:[/yellow] ").strip()
    
    console.print("[yellow]Search type:[/yellow]\n1. Exact match\n2. Contains")
    choice = console.input("[yellow]Choose 1 or 2:[/yellow] ").strip()
    search_type = "exact" if choice == "1" else "contains"
    
    exts_input = console.input("[yellow]Filter by extensions? (comma separated, e.g. .txt,.pdf) or leave empty:[/yellow] ").strip()
    exts = [e.strip() for e in exts_input.split(",")] if exts_input else []
    
    exclude_input = console.input("[yellow]Exclude folders? (comma separated, e.g. node_modules,.git) or leave empty:[/yellow] ").strip()
    exclude_dirs = [d.strip() for d in exclude_input.split(",")] if exclude_input else []
    
    try:
        seconds = int(console.input("[yellow]How many seconds to search? (default 30):[/yellow] ").strip() or "30")
    except:
        seconds = 30
    
    try:
        thread_count = int(console.input("[yellow]Number of threads to use? (default 4):[/yellow] ").strip() or "4")
    except:
        thread_count = 4
    
    results = []
    queue = Queue()
    
    # enqueue folders recursively excluding specified dirs
    enqueue_folders(folder, queue, exclude_dirs)
    total_folders = queue.qsize()
    console.print(f"[blue]Total folders to search: {total_folders}[/blue]")
    
    global self_stop
    self_stop = threading.Event()
    
    stop_time = time.time() + seconds
    
    lock = threading.Lock()
    
    console.print(f"\n[cyan]Starting search for '{search_term}' in {folder} (up to {seconds} seconds)...[/cyan]")
    
    with Progress(SpinnerColumn(),
                  "[progress.description]{task.description}",
                  BarColumn(),
                  "[progress.percentage]{task.percentage:>3.0f}%",
                  TimeRemainingColumn()) as progress:
        
        progress_task = progress.add_task("Searching...", total=total_folders)
        
        threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=search_files,
                                 args=(queue, results, search_term, search_type, exts, stop_time, progress_task, progress, lock))
            t.daemon = True
            t.start()
            threads.append(t)
        
        try:
            while any(t.is_alive() for t in threads) and time.time() < stop_time:
                time.sleep(0.2)
        except KeyboardInterrupt:
            self_stop.set()
            console.print("\n[red]Search stopped by user.[/red]")
    
    # Deduplicate and sort results
    results = sorted(set(results))
    
    console.print("\n[bold magenta]=== Search Results ===[/bold magenta]")
    if results:
        table = Table(show_header=True, header_style="bold green")
        table.add_column("No.", style="dim", width=6)
        table.add_column("File Path", overflow="fold")
        for i, fpath in enumerate(results, 1):
            table.add_row(str(i), fpath)
        console.print(table)
        
        open_choice = console.input("\nOpen file locations? (y/n): ").lower()
        if open_choice == 'y':
            for file in results:
                open_folder(file)
    else:
        console.print("[red]No matching files found.[/red]")
    
    save_choice = console.input("\nSave results to a text file? (y/n): ").lower()
    if save_choice == 'y':
        filename = f"file_search_results_{int(time.time())}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Search results for '{search_term}' in {folder}:\n\n")
            for file in results:
                f.write(file + "\n")
        console.print(f"[green]Results saved to:[/green] {filename}")
        open_folder(os.path.abspath(filename))

if __name__ == "__main__":
    main()
