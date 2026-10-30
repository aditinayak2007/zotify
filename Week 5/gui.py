"""
Page Replacement Algorithm Simulator - Graphical User Interface
Module Owner: Anas (GUI & User Interface)
Integrated by: Aditi Nayak (Team Leader & Complete Integration)
Team Members: Aditi Nayak (Leader), Anas Ahmed, Nireeksha, Yaseem
Course: Operating Systems PBL (Week 5)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math


def simulate_page_replacement(pages, capacity, algorithm):
    """
    Simulates FIFO, LRU, or Optimal page replacement.
    Returns: (history, hits, faults, hit_ratio, fault_ratio)
      history is a list of tuples: (step_num, page, frames_copy, is_hit)
    """
    frames = []
    history = []
    hits = 0
    faults = 0
    last_used = {}      # For LRU: page -> last accessed index
    fifo_pointer = 0    # For FIFO: circular replacement pointer

    total_refs = len(pages)
    if total_refs == 0 or capacity <= 0:
        return [], 0, 0, 0.0, 0.0

    for i, page in enumerate(pages):
        hit = page in frames

        if hit:
            hits += 1
            last_used[page] = i
        else:
            faults += 1
            if len(frames) < capacity:
                frames.append(page)
            elif algorithm == "FIFO":
                frames[fifo_pointer] = page
                fifo_pointer = (fifo_pointer + 1) % capacity
            elif algorithm == "LRU":
                # Find page with oldest last_used timestamp
                victim = min(frames, key=lambda p: last_used.get(p, -1))
                frames[frames.index(victim)] = page
            elif algorithm == "Optimal":
                # Find page that will not be needed for the longest time in the future
                future = pages[i + 1:]

                def next_use(p):
                    return future.index(p) if p in future else float("inf")

                # If multiple pages never used, max() picks first encountered (deterministic FIFO tie-breaking)
                victim = max(frames, key=next_use)
                frames[frames.index(victim)] = page

            last_used[page] = i

        history.append((i + 1, page, list(frames), hit))

    hit_ratio = (hits / total_refs) * 100.0
    fault_ratio = (faults / total_refs) * 100.0

    return history, hits, faults, hit_ratio, fault_ratio


class PageReplacementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Algorithms Simulator - OS PBL Week 5")
        self.root.geometry("1100x780")
        self.root.minsize(850, 600)
        self.root.configure(bg="#f8fafc")

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self._configure_styles()
        self._build_header()
        self._build_input_panel()
        self._build_summary_panel()
        self._build_results_notebook()

        # Load initial course specification benchmark
        self.load_benchmark()

    def _configure_styles(self):
        self.style.configure("Treeview", rowheight=26, font=("Helvetica", 9))
        self.style.configure("Treeview.Heading", font=("Helvetica", 9, "bold"), background="#e2e8f0")
        self.style.configure("TButton", font=("Helvetica", 9, "bold"), padding=6)
        self.style.configure("Accent.TButton", font=("Helvetica", 9, "bold"), padding=6, background="#2563eb", foreground="white")

    def _build_header(self):
        header = tk.Frame(self.root, bg="#0f172a", padx=20, pady=14)
        header.pack(fill="x")

        title_lbl = tk.Label(
            header,
            text="PAGE REPLACEMENT ALGORITHM SIMULATOR",
            font=("Helvetica", 16, "bold"),
            fg="#f8fafc",
            bg="#0f172a"
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            header,
            text="Team Leader: Aditi Nayak | Anas (GUI) • Nireeksha (FIFO & LRU) • Yaseem (Optimal & Comparison)",
            font=("Helvetica", 9),
            fg="#94a3b8",
            bg="#0f172a"
        )
        sub_lbl.pack(anchor="w", pady=(3, 0))

    def _build_input_panel(self):
        panel = tk.LabelFrame(
            self.root,
            text=" Simulation Configuration & Inputs ",
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            padx=16,
            pady=10
        )
        panel.pack(fill="x", padx=16, pady=10)

        # Row 0: Page reference string input
        tk.Label(panel, text="Page-Reference String:", bg="#ffffff", font=("Helvetica", 9, "bold")).grid(
            row=0, column=0, sticky="w", padx=4, pady=6
        )
        self.page_entry = ttk.Entry(panel, width=50, font=("Consolas", 10))
        self.page_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=8, pady=6)

        # Preset loader buttons
        btn_preset1 = ttk.Button(panel, text="Load Course Benchmark", command=self.load_benchmark)
        btn_preset1.grid(row=0, column=3, padx=4, pady=6)

        btn_preset2 = ttk.Button(panel, text="Load Belady's Anomaly", command=self.load_belady)
        btn_preset2.grid(row=0, column=4, padx=4, pady=6)

        # Row 1: Number of frames & Algorithm selection
        tk.Label(panel, text="Number of Frames:", bg="#ffffff", font=("Helvetica", 9, "bold")).grid(
            row=1, column=0, sticky="w", padx=4, pady=6
        )
        self.frame_entry = ttk.Entry(panel, width=12, font=("Consolas", 10))
        self.frame_entry.grid(row=1, column=1, sticky="w", padx=8, pady=6)

        tk.Label(panel, text="Algorithm:", bg="#ffffff", font=("Helvetica", 9, "bold")).grid(
            row=1, column=2, sticky="e", padx=4, pady=6
        )
        self.algo_combo = ttk.Combobox(
            panel,
            values=["Compare All", "FIFO", "LRU", "Optimal"],
            state="readonly",
            width=18,
            font=("Helvetica", 9)
        )
        self.algo_combo.grid(row=1, column=3, sticky="w", padx=4, pady=6)
        self.algo_combo.set("Compare All")

        # Row 2: Action Buttons
        btn_bar = tk.Frame(panel, bg="#ffffff")
        btn_bar.grid(row=2, column=0, columnspan=5, sticky="w", pady=(8, 4), padx=4)

        btn_run = tk.Button(
            btn_bar,
            text="▶ Run Simulation",
            bg="#2563eb",
            fg="white",
            font=("Helvetica", 9, "bold"),
            padx=12,
            pady=4,
            relief=tk.RAISED,
            command=self.run_simulation
        )
        btn_run.pack(side="left", padx=(0, 8))

        btn_compare = tk.Button(
            btn_bar,
            text="⚖ Compare All Algorithms",
            bg="#059669",
            fg="white",
            font=("Helvetica", 9, "bold"),
            padx=12,
            pady=4,
            relief=tk.RAISED,
            command=self.run_compare_all
        )
        btn_compare.pack(side="left", padx=8)

        btn_clear = tk.Button(
            btn_bar,
            text="↺ Clear / Reset",
            bg="#64748b",
            fg="white",
            font=("Helvetica", 9, "bold"),
            padx=12,
            pady=4,
            relief=tk.RAISED,
            command=self.clear_all
        )
        btn_clear.pack(side="left", padx=8)

        panel.columnconfigure(1, weight=1)

    def _build_summary_panel(self):
        self.summary_frame = tk.LabelFrame(
            self.root,
            text=" Performance Evaluation Summary ",
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            padx=16,
            pady=8
        )
        self.summary_frame.pack(fill="x", padx=16, pady=(0, 8))

        self.summary_cards_frame = tk.Frame(self.summary_frame, bg="#ffffff")
        self.summary_cards_frame.pack(fill="x")

        # Create Metric Cards
        self.card_refs = self._create_card(self.summary_cards_frame, "Total References", "0", "#1e293b")
        self.card_hits = self._create_card(self.summary_cards_frame, "Total Hits", "0", "#15803d")
        self.card_faults = self._create_card(self.summary_cards_frame, "Total Faults", "0", "#b91c1c")
        self.card_hit_ratio = self._create_card(self.summary_cards_frame, "Hit Ratio", "0.00%", "#0284c7")
        self.card_fault_ratio = self._create_card(self.summary_cards_frame, "Fault Ratio", "0.00%", "#ea580c")

        # Best algorithm banner
        self.best_label = tk.Label(
            self.summary_frame,
            text="Select an algorithm and click 'Run Simulation' or 'Compare All'.",
            font=("Helvetica", 9, "bold"),
            bg="#f1f5f9",
            fg="#334155",
            padx=10,
            pady=5,
            relief=tk.RIDGE
        )
        self.best_label.pack(fill="x", pady=(8, 0))

    def _create_card(self, parent, title, init_val, fg_color):
        card = tk.Frame(parent, bg="#f8fafc", relief=tk.GROOVE, bd=1, padx=12, pady=6)
        card.pack(side="left", expand=True, fill="both", padx=4)

        t_lbl = tk.Label(card, text=title, font=("Helvetica", 8, "bold"), fg="#64748b", bg="#f8fafc")
        t_lbl.pack()

        v_lbl = tk.Label(card, text=init_val, font=("Helvetica", 13, "bold"), fg=fg_color, bg="#f8fafc")
        v_lbl.pack(pady=(2, 0))

        return v_lbl

    def _build_results_notebook(self):
        container = tk.Frame(self.root, bg="#f8fafc", padx=16, pady=4)
        container.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: Step-by-Step Simulation Table
        tab_steps = ttk.Frame(self.notebook)
        self.notebook.add(tab_steps, text="  Step-by-Step Frame Contents  ")

        cols = ("algorithm", "step", "page", "frames", "status")
        self.result_tree = ttk.Treeview(tab_steps, columns=cols, show="headings")

        self.result_tree.heading("algorithm", text="Algorithm")
        self.result_tree.heading("step", text="Step #")
        self.result_tree.heading("page", text="Page")
        self.result_tree.heading("frames", text="Frame Contents (Allocated Slots)")
        self.result_tree.heading("status", text="Hit / Fault Status")

        self.result_tree.column("algorithm", width=120, anchor="center")
        self.result_tree.column("step", width=70, anchor="center")
        self.result_tree.column("page", width=80, anchor="center")
        self.result_tree.column("frames", width=340, anchor="center")
        self.result_tree.column("status", width=130, anchor="center")

        self.result_tree.tag_configure("hit", foreground="#15803d", font=("Helvetica", 9, "bold"))
        self.result_tree.tag_configure("fault", foreground="#b91c1c", font=("Helvetica", 9, "bold"))

        scroll_y = ttk.Scrollbar(tab_steps, orient="vertical", command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scroll_y.set)
        self.result_tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        # Tab 2: Comparison Analysis Table
        tab_comp = ttk.Frame(self.notebook)
        self.notebook.add(tab_comp, text="  Algorithms Comparison Matrix  ")

        comp_cols = ("algo", "refs", "hits", "faults", "hit_ratio", "fault_ratio", "rank")
        self.comp_tree = ttk.Treeview(tab_comp, columns=comp_cols, show="headings")

        self.comp_tree.heading("algo", text="Algorithm Name")
        self.comp_tree.heading("refs", text="Total References")
        self.comp_tree.heading("hits", text="Page Hits")
        self.comp_tree.heading("faults", text="Page Faults")
        self.comp_tree.heading("hit_ratio", text="Hit Ratio (%)")
        self.comp_tree.heading("fault_ratio", text="Fault Ratio (%)")
        self.comp_tree.heading("rank", text="Performance Outcome")

        self.comp_tree.column("algo", width=140, anchor="center")
        self.comp_tree.column("refs", width=110, anchor="center")
        self.comp_tree.column("hits", width=90, anchor="center")
        self.comp_tree.column("faults", width=100, anchor="center")
        self.comp_tree.column("hit_ratio", width=110, anchor="center")
        self.comp_tree.column("fault_ratio", width=110, anchor="center")
        self.comp_tree.column("rank", width=220, anchor="center")

        self.comp_tree.tag_configure("winner", foreground="#15803d", font=("Helvetica", 9, "bold"))
        self.comp_tree.tag_configure("normal", foreground="#334155")

        scroll_c = ttk.Scrollbar(tab_comp, orient="vertical", command=self.comp_tree.yview)
        self.comp_tree.configure(yscrollcommand=scroll_c.set)
        self.comp_tree.pack(side="left", fill="both", expand=True)
        scroll_c.pack(side="right", fill="y")

    # ---------------- PRESETS ----------------
    def load_benchmark(self):
        """Loads course standard benchmark: 7 0 1 2 0 3 0 4 2 3 with 3 frames."""
        self.page_entry.delete(0, tk.END)
        self.page_entry.insert(0, "7 0 1 2 0 3 0 4 2 3")
        self.frame_entry.delete(0, tk.END)
        self.frame_entry.insert(0, "3")
        self.algo_combo.set("Compare All")

    def load_belady(self):
        """Loads Belady's Anomaly test: 1 2 3 4 1 2 5 1 2 3 4 5 with 3 frames."""
        self.page_entry.delete(0, tk.END)
        self.page_entry.insert(0, "1 2 3 4 1 2 5 1 2 3 4 5")
        self.frame_entry.delete(0, tk.END)
        self.frame_entry.insert(0, "3")
        self.algo_combo.set("Compare All")

    # ---------------- VALIDATION ----------------
    def _validate_inputs(self):
        raw_pages = self.page_entry.get().replace(",", " ").strip().split()

        if not raw_pages:
            raise ValueError("Please enter a page-reference string (e.g. 7 0 1 2 0 3 0 4 2 3).")

        pages = []
        for token in raw_pages:
            try:
                val = int(token)
                if val < 0:
                    raise ValueError(f"Page number '{val}' cannot be negative.")
                pages.append(val)
            except ValueError:
                raise ValueError(f"Invalid page reference token '{token}'. Only non-negative integers are allowed.")

        raw_frames = self.frame_entry.get().strip()
        if not raw_frames:
            raise ValueError("Please specify the number of page frames.")

        try:
            capacity = int(raw_frames)
            if capacity < 1:
                raise ValueError("Number of frames must be an integer greater than or equal to 1.")
        except ValueError:
            raise ValueError(f"Invalid frame capacity '{raw_frames}'. Must be an integer >= 1.")

        return pages, capacity

    # ---------------- EXECUTION ----------------
    def run_compare_all(self):
        self.algo_combo.set("Compare All")
        self.run_simulation()

    def run_simulation(self):
        try:
            pages, capacity = self._validate_inputs()
        except ValueError as err:
            messagebox.showerror("Input Validation Error", str(err))
            return

        selected_algo = self.algo_combo.get()
        algorithms = ["FIFO", "LRU", "Optimal"] if selected_algo == "Compare All" else [selected_algo]

        self.result_tree.delete(*self.result_tree.get_children())
        self.comp_tree.delete(*self.comp_tree.get_children())

        results = []

        for algo in algorithms:
            history, hits, faults, hit_ratio, fault_ratio = simulate_page_replacement(pages, capacity, algo)
            results.append({
                "algorithm": algo,
                "history": history,
                "hits": hits,
                "faults": faults,
                "hit_ratio": hit_ratio,
                "fault_ratio": fault_ratio,
                "total_refs": len(pages)
            })

            # Populate step-by-step table
            for step_num, page, frames_list, is_hit in history:
                slots = [str(f) for f in frames_list] + ["-"] * (capacity - len(frames_list))
                frames_display = "[ " + "  ".join(slots) + " ]"
                status_text = "PAGE HIT" if is_hit else "PAGE FAULT"
                tag = "hit" if is_hit else "fault"

                self.result_tree.insert(
                    "",
                    "end",
                    values=(algo, step_num, page, frames_display, status_text),
                    tags=(tag,)
                )

        # Update Summary Cards (for single selection or top summary)
        if len(results) == 1:
            res = results[0]
            self.card_refs.config(text=str(res["total_refs"]))
            self.card_hits.config(text=str(res["hits"]))
            self.card_faults.config(text=str(res["faults"]))
            self.card_hit_ratio.config(text=f"{res['hit_ratio']:.2f}%")
            self.card_fault_ratio.config(text=f"{res['fault_ratio']:.2f}%")
            self.best_label.config(
                text=f"Algorithm: {res['algorithm']} | Hits: {res['hits']} | Faults: {res['faults']} | "
                     f"Hit Ratio: {res['hit_ratio']:.2f}% | Fault Ratio: {res['fault_ratio']:.2f}%",
                fg="#1e293b"
            )
            self.notebook.select(0)
        else:
            # Compare All mode: find best algorithm with minimum page faults
            min_faults = min(r["faults"] for r in results)
            winners = [r["algorithm"] for r in results if r["faults"] == min_faults]

            self.card_refs.config(text=str(len(pages)))
            self.card_hits.config(text=f"Opt:{results[2]['hits']}")
            self.card_faults.config(text=f"Min:{min_faults}")
            self.card_hit_ratio.config(text=f"Max:{max(r['hit_ratio'] for r in results):.1f}%")
            self.card_fault_ratio.config(text=f"Min:{min(r['fault_ratio'] for r in results):.1f}%")

            winner_str = ", ".join(winners)
            self.best_label.config(
                text=f"★ BEST PERFORMING ALGORITHM: {winner_str} (Minimum Faults: {min_faults}, "
                     f"Fault Ratio: {(min_faults / len(pages)) * 100:.2f}%)",
                fg="#15803d"
            )

            # Populate Comparison Table
            for r in results:
                is_win = r["algorithm"] in winners
                rank_str = "★ Best Algorithm (Lowest Faults)" if is_win else "Evaluated"
                tag = "winner" if is_win else "normal"

                self.comp_tree.insert(
                    "",
                    "end",
                    values=(
                        r["algorithm"],
                        r["total_refs"],
                        r["hits"],
                        r["faults"],
                        f"{r['hit_ratio']:.2f}%",
                        f"{r['fault_ratio']:.2f}%",
                        rank_str
                    ),
                    tags=(tag,)
                )

            # Switch to comparison tab if multiple algorithms compared
            self.notebook.select(1)

    def clear_all(self):
        self.page_entry.delete(0, tk.END)
        self.frame_entry.delete(0, tk.END)
        self.algo_combo.set("Compare All")
        self.result_tree.delete(*self.result_tree.get_children())
        self.comp_tree.delete(*self.comp_tree.get_children())

        self.card_refs.config(text="0")
        self.card_hits.config(text="0")
        self.card_faults.config(text="0")
        self.card_hit_ratio.config(text="0.00%")
        self.card_fault_ratio.config(text="0.00%")
        self.best_label.config(
            text="Inputs cleared. Enter values or load a benchmark to begin.",
            fg="#64748b"
        )


def main():
    root = tk.Tk()
    app = PageReplacementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
