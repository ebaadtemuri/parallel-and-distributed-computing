from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from analyzer import analyze_processes, analyze_serial, analyze_threads


def main():
    root = tk.Tk()
    root.title("Log Analyzer")
    root.geometry("760x520")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frame = ttk.Frame(root, padding=16)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(4, weight=1)

    folder = tk.StringVar()
    keyword = tk.StringVar(value="ERROR")
    mode = tk.StringVar(value="Compare all")
    status = tk.StringVar(value="Choose a folder containing .log files.")

    def choose_folder():
        selected = filedialog.askdirectory(title="Select log folder")
        if selected:
            folder.set(selected)

    def analyze():
        selected_folder = Path(folder.get())
        if not selected_folder.is_dir():
            messagebox.showerror("Folder required", "Choose a valid folder.")
            return

        log_files = sorted(selected_folder.rglob("*.log"))
        if not log_files:
            messagebox.showinfo("No log files", "The selected folder has no .log files.")
            return

        modes = {
            "Serial": [("Serial", analyze_serial)],
            "Threads": [("Threads", analyze_threads)],
            "Processes": [("Processes", analyze_processes)],
            "Compare all": [
                ("Serial", analyze_serial),
                ("Threads", analyze_threads),
                ("Processes", analyze_processes),
            ],
        }

        output.delete("1.0", "end")
        status.set(f"Analyzing {len(log_files)} log file(s)...")
        root.update_idletasks()

        try:
            for label, run_analysis in modes[mode.get()]:
                results, elapsed = run_analysis(log_files, keyword.get())

                output.insert("end", f"{label}\n")
                for result in results:
                    output.insert(
                        "end",
                        f"  {Path(result['file']).name}: "
                        f"{result['words']} words, "
                        f"{result['matches']} keyword matches\n",
                    )

                total_words = sum(result["words"] for result in results)
                total_matches = sum(result["matches"] for result in results)
                output.insert(
                    "end",
                    f"  Total: {total_words} words, "
                    f"{total_matches} matches; {elapsed:.6f} seconds\n\n",
                )

            status.set(f"Finished analyzing {len(log_files)} log file(s).")
        except Exception as error:
            status.set("Analysis failed.")
            messagebox.showerror("Analysis failed", str(error))

    ttk.Label(frame, text="Log folder").grid(row=0, column=0, sticky="w", pady=6)
    ttk.Entry(frame, textvariable=folder).grid(
        row=0, column=1, sticky="ew", padx=8, pady=6
    )
    ttk.Button(frame, text="Browse", command=choose_folder).grid(
        row=0, column=2, pady=6
    )

    ttk.Label(frame, text="Keyword").grid(row=1, column=0, sticky="w", pady=6)
    ttk.Entry(frame, textvariable=keyword).grid(
        row=1, column=1, sticky="ew", padx=8, pady=6
    )

    ttk.Label(frame, text="Execution mode").grid(
        row=2, column=0, sticky="w", pady=6
    )
    ttk.Combobox(
        frame,
        textvariable=mode,
        values=("Serial", "Threads", "Processes", "Compare all"),
        state="readonly",
    ).grid(row=2, column=1, sticky="w", padx=8, pady=6)

    ttk.Button(frame, text="Analyze", command=analyze).grid(
        row=3, column=1, sticky="w", padx=8, pady=10
    )

    output = tk.Text(frame, wrap="word")
    output.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=8)
    ttk.Label(frame, textvariable=status).grid(
        row=5, column=0, columnspan=3, sticky="w", pady=6
    )

    root.mainloop()


if __name__ == "__main__":
    main()
