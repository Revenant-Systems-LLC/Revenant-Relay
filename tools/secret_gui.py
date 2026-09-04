"""GUI editor for the DPAPI secret vault. No terminal, no shell history.

`secret_tool.py` prompts on stdin, which means typing credentials into a console
window. This does the same job in a masked dialog instead. Nothing is echoed,
nothing reaches PowerShell history, and existing values are never displayed —
each key shows SET or EMPTY only.

Blank fields are left alone. Only keys you actually type into get written, so
you can open this, fill one box, and save without touching anything else.

Run:
    py -3.11 secret_gui.py
"""

from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import secret_tool  # noqa: E402

# Keys Relay reads, grouped for the dialog. Keys already in the vault but not
# listed here still appear, under "Other" — nothing is hidden from the editor.
GROUPS = [
    ("Reddit", [
        "RR_REDDIT_CLIENT_ID",
        "RR_REDDIT_CLIENT_SECRET",
        "RR_REDDIT_USERNAME",
        "RR_REDDIT_PASSWORD",
        "RR_REDDIT_USER_AGENT",
        "RR_REDDIT_REFRESH_TOKEN",
    ]),
    ("Meta (Facebook + Instagram)", [
        "RR_FACEBOOK_PAGE_ID",
        "RR_FACEBOOK_PAGE_TOKEN",
        "RR_INSTAGRAM_USER_ID",
        "RR_INSTAGRAM_TOKEN",
        "RR_INSTAGRAM_MEDIA_BASE_URL",
    ]),
    ("LinkedIn", [
        "RR_LINKEDIN_POST_TARGET",
        "RR_LINKEDIN_COMPANY_PAGE_URL",
    ]),
    ("Bluesky", [
        "RR_BLUESKY_HANDLE",
        "RR_BLUESKY_PASSWORD",
    ]),
    ("Email reports", [
        "RR_EMAIL",
        "RR_EMAIL_PASSWORD",
    ]),
]

# Not secret — showing these back makes it obvious when one is wrong, which is
# how the corrupted Reddit username sat unnoticed for a month.
PLAIN = {
    "RR_REDDIT_USERNAME",
    "RR_REDDIT_USER_AGENT",
    "RR_LINKEDIN_POST_TARGET",
    "RR_LINKEDIN_COMPANY_PAGE_URL",
    "RR_INSTAGRAM_MEDIA_BASE_URL",
    "RR_FACEBOOK_PAGE_ID",
    "RR_INSTAGRAM_USER_ID",
    "RR_BLUESKY_HANDLE",
    "RR_EMAIL",
}


class SecretEditor:
    def __init__(self, root):
        self.root = root
        self.payload, self.text = secret_tool._read()
        self.current = secret_tool._pairs(self.text)
        self.entries: dict[str, tk.Entry] = {}

        root.title("Revenant Relay — credentials")
        root.geometry("640x760")

        header = ttk.Label(
            root,
            text=("Blank fields are left unchanged. Fill only what you want to set.\n"
                  "Existing secret values are never shown — only SET or EMPTY."),
            justify="left",
            padding=(12, 10),
        )
        header.pack(anchor="w")

        canvas = tk.Canvas(root, borderwidth=0, highlightthickness=0)
        scroll = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        body = ttk.Frame(canvas)
        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(12, 0))
        scroll.pack(side="right", fill="y")

        listed = {k for _, keys in GROUPS for k in keys}
        extra = sorted(k for k in self.current if k not in listed)
        groups = GROUPS + ([("Other", extra)] if extra else [])

        for title, keys in groups:
            frame = ttk.LabelFrame(body, text=title, padding=(10, 8))
            frame.pack(fill="x", expand=True, pady=6, padx=(0, 12))
            for key in keys:
                self._row(frame, key)

        buttons = ttk.Frame(root, padding=(12, 10))
        buttons.pack(side="bottom", fill="x")
        ttk.Button(buttons, text="Save", command=self.save).pack(side="right")
        ttk.Button(buttons, text="Cancel", command=root.destroy).pack(side="right", padx=6)

    def _row(self, parent, key):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=2)

        ttk.Label(row, text=key, width=30, anchor="w").pack(side="left")

        value = self.current.get(key)
        if value is None:
            status, colour = "ABSENT", "#b00"
        elif value:
            status, colour = "SET", "#070"
        else:
            status, colour = "EMPTY", "#b60"
        tk.Label(row, text=status, width=8, anchor="w", fg=colour).pack(side="left")

        entry = ttk.Entry(row, show=None if key in PLAIN else "*")
        entry.pack(side="left", fill="x", expand=True)
        # Non-secret values are prefilled so a wrong one is visible at a glance.
        if key in PLAIN and value:
            entry.insert(0, value)
        self.entries[key] = entry

    def save(self):
        changes = {}
        for key, entry in self.entries.items():
            typed = entry.get().strip()
            if not typed:
                continue
            if typed == self.current.get(key):
                continue  # prefilled and untouched
            changes[key] = typed

        if not changes:
            messagebox.showinfo("Nothing to do", "No fields were changed.")
            return

        names = "\n".join(f"  {k}" for k in sorted(changes))
        if not messagebox.askokcancel("Write to vault?", f"Set these keys?\n\n{names}"):
            return

        lines = self.text.splitlines()
        for key, value in changes.items():
            for i, line in enumerate(lines):
                if line.strip().startswith(f"{key}="):
                    lines[i] = f"{key}={value}"
                    break
            else:
                lines.append(f"{key}={value}")

        try:
            # _write backs up first and re-reads to verify; it raises on mismatch.
            secret_tool._write(self.payload, "\n".join(lines) + "\n")
        except SystemExit as e:
            messagebox.showerror("Write failed", str(e))
            return
        except Exception as e:  # noqa: BLE001 - surface anything to the dialog
            messagebox.showerror("Write failed", f"{e.__class__.__name__}: {e}")
            return

        messagebox.showinfo("Saved", f"Wrote {len(changes)} key(s). Backup created.")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    SecretEditor(root)
    root.mainloop()
