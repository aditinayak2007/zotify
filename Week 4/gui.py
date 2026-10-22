"""
Interactive Deadlock Simulation System - Graphical User Interface
Module Owner: Anas (UI & Visualization)
Integrated by: Aditi Nayak (Team Leader & Integration)
Team: Aditi Nayak, Anas, Nireeksha, Yaseem
Course: Operating Systems PBL (Week 4)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

class DeadlockSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Deadlock Simulation System - OS PBL Week 4")
        self.root.geometry("1280x820")
        self.root.minsize(1024, 720)

        # Apply a clean modern theme
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Data model
        self.n = 5  # Number of processes
        self.m = 3  # Number of resource types

        self.alloc = []
        self.max_mat = []
        self.need = []
        self.avail = []
        self.request = []
        self.deadlocked_procs = []
        self.system_status = "SAFE"  # SAFE, UNSAFE, DEADLOCKED

        self._init_default_data()
        self._build_ui()
        self._sync_matrices_to_ui()
        self._redraw_rag()
        self.log_message("[SYSTEM INITIALIZED]: Ready for simulation. Loaded standard Silberschatz 5x3 benchmark.")

    def _init_default_data(self):
        """Initializes with Silberschatz 5 processes, 3 resource types benchmark."""
        self.n = 5
        self.m = 3
        self.alloc = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]
        self.max_mat = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ]
        self.avail = [3, 3, 2]
        self.request = [[0] * self.m for _ in range(self.n)]
        self._recalculate_need()
        self.deadlocked_procs = []
        self.system_status = "SAFE"

    def _recalculate_need(self):
        self.need = []
        for i in range(self.n):
            row = []
            for j in range(self.m):
                row.append(max(0, self.max_mat[i][j] - self.alloc[i][j]))
            self.need.append(row)

    # ---------------- UI BUILDER ----------------
    def _build_ui(self):
        # 1. Header Banner
        header_frame = tk.Frame(self.root, bg="#1e293b", pady=10, padx=15)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(header_frame, text="Interactive Deadlock Simulation System",
                             font=("Helvetica", 16, "bold"), fg="#f8fafc", bg="#1e293b")
        title_lbl.pack(side=tk.LEFT)

        team_lbl = tk.Label(header_frame,
                            text="Team: Aditi Nayak (Leader) | Anas (UI) | Nireeksha (Banker's) | Yaseem (Deadlock & RAG)",
                            font=("Helvetica", 9), fg="#94a3b8", bg="#1e293b")
        team_lbl.pack(side=tk.LEFT, padx=20)

        self.status_badge = tk.Label(header_frame, text=" [ SYSTEM STATE: SAFE ] ",
                                     font=("Helvetica", 11, "bold"), bg="#10b981", fg="white",
                                     padx=12, pady=4, relief=tk.RIDGE)
        self.status_badge.pack(side=tk.RIGHT)

        # 2. Control Toolbar
        toolbar = tk.Frame(self.root, bg="#f1f5f9", pady=6, padx=15, relief=tk.GROOVE, bd=1)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        tk.Label(toolbar, text="Processes (N):", bg="#f1f5f9", font=("Helvetica", 9, "bold")).pack(side=tk.LEFT, padx=4)
        self.n_spin = ttk.Spinbox(toolbar, from_=1, to=10, width=4)
        self.n_spin.set(self.n)
        self.n_spin.pack(side=tk.LEFT, padx=4)

        tk.Label(toolbar, text="Resources (M):", bg="#f1f5f9", font=("Helvetica", 9, "bold")).pack(side=tk.LEFT, padx=4)
        self.m_spin = ttk.Spinbox(toolbar, from_=1, to=10, width=4)
        self.m_spin.set(self.m)
        self.m_spin.pack(side=tk.LEFT, padx=4)

        apply_dim_btn = ttk.Button(toolbar, text="Resize Matrices", command=self._on_resize_matrices)
        apply_dim_btn.pack(side=tk.LEFT, padx=8)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Label(toolbar, text="Load Preset:", bg="#f1f5f9", font=("Helvetica", 9, "bold")).pack(side=tk.LEFT, padx=4)
        self.preset_combo = ttk.Combobox(toolbar, values=[
            "Preset 1: Silberschatz Safe State (5x3)",
            "Preset 2: Circular Wait Deadlock (3x3)",
            "Preset 3: Multi-Process Deadlock (4x3)",
            "Preset 4: Unsafe State but not Deadlocked"
        ], state="readonly", width=38)
        self.preset_combo.current(0)
        self.preset_combo.pack(side=tk.LEFT, padx=4)

        load_preset_btn = ttk.Button(toolbar, text="Load", command=self._on_load_preset)
        load_preset_btn.pack(side=tk.LEFT, padx=4)

        reset_btn = ttk.Button(toolbar, text="↺ Reset", command=self._on_reset)
        reset_btn.pack(side=tk.RIGHT, padx=5)

        # 3. Main Workspace Split (Left: Matrices & Operations, Right: RAG & Log)
        main_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#cbd5e1", sashwidth=4)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Left Container
        left_container = tk.Frame(main_pane, bg="#ffffff")
        main_pane.add(left_container, minsize=520, width=580)

        # Notebook for Matrices
        self.notebook = ttk.Notebook(left_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.tab_alloc = ttk.Frame(self.notebook)
        self.tab_max = ttk.Frame(self.notebook)
        self.tab_need = ttk.Frame(self.notebook)
        self.tab_avail = ttk.Frame(self.notebook)
        self.tab_request = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_alloc, text="Allocation Matrix")
        self.notebook.add(self.tab_max, text="Max Matrix")
        self.notebook.add(self.tab_need, text="Need Matrix")
        self.notebook.add(self.tab_avail, text="Available Vector")
        self.notebook.add(self.tab_request, text="Pending Requests")

        # Create entry grids
        self.entries_alloc = []
        self.entries_max = []
        self.labels_need = []
        self.entries_avail = []
        self.entries_request = []

        self._build_matrix_tab(self.tab_alloc, "Allocation Matrix (Alloc[i][j])", "alloc")
        self._build_matrix_tab(self.tab_max, "Maximum Requirement Matrix (Max[i][j])", "max")
        self._build_matrix_tab(self.tab_need, "Need Matrix (Need = Max - Alloc)", "need")
        self._build_avail_tab(self.tab_avail)
        self._build_matrix_tab(self.tab_request, "Outstanding Request Matrix (Req[i][j])", "request")

        # Action Buttons Panel
        action_box = tk.LabelFrame(left_container, text=" Simulation Operations ",
                                   font=("Helvetica", 10, "bold"), bg="#ffffff", padx=10, pady=8)
        action_box.pack(fill=tk.X, side=tk.BOTTOM, padx=6, pady=6)

        # Row 1 of actions
        btn_row1 = tk.Frame(action_box, bg="#ffffff")
        btn_row1.pack(fill=tk.X, pady=4)

        banker_btn = tk.Button(btn_row1, text="🔍 Check Banker's Safety", bg="#3b82f6", fg="white",
                               font=("Helvetica", 9, "bold"), relief=tk.RAISED, padx=8, pady=5,
                               command=self._on_check_bankers_safety)
        banker_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        req_btn = tk.Button(btn_row1, text="📥 Request Resources", bg="#0284c7", fg="white",
                            font=("Helvetica", 9, "bold"), relief=tk.RAISED, padx=8, pady=5,
                            command=self._on_open_request_dialog)
        req_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        # Row 2 of actions
        btn_row2 = tk.Frame(action_box, bg="#ffffff")
        btn_row2.pack(fill=tk.X, pady=4)

        detect_btn = tk.Button(btn_row2, text="⚠️ Detect Deadlock", bg="#d97706", fg="white",
                               font=("Helvetica", 9, "bold"), relief=tk.RAISED, padx=8, pady=5,
                               command=self._on_detect_deadlock)
        detect_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        recover_btn = tk.Button(btn_row2, text="🛠️ Recover from Deadlock", bg="#ef4444", fg="white",
                                font=("Helvetica", 9, "bold"), relief=tk.RAISED, padx=8, pady=5,
                                command=self._on_recover_dialog)
        recover_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        # Right Container (RAG Visualization & Execution Log)
        right_container = tk.Frame(main_pane, bg="#ffffff")
        main_pane.add(right_container, minsize=420)

        # RAG Visualization Canvas Box
        rag_box = tk.LabelFrame(right_container, text=" Resource Allocation Graph (RAG) Visualization ",
                                font=("Helvetica", 10, "bold"), bg="#ffffff", padx=6, pady=6)
        rag_box.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Graph legend
        legend_frame = tk.Frame(rag_box, bg="#ffffff")
        legend_frame.pack(fill=tk.X, side=tk.TOP, pady=2)
        tk.Label(legend_frame, text="● Process (Blue)   ■ Resource (Green)   ➜ Allocation (Solid)   ⇢ Request (Dashed)   ● Deadlock (Red)",
                 font=("Helvetica", 8), fg="#475569", bg="#ffffff").pack(side=tk.LEFT)

        self.canvas = tk.Canvas(rag_box, bg="#f8fafc", highlightthickness=1, highlightbackground="#cbd5e1")
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=4)

        # Execution Log Box
        log_box = tk.LabelFrame(right_container, text=" Step-by-Step Diagnostic Trace & Algorithm Log ",
                                font=("Helvetica", 10, "bold"), bg="#ffffff", padx=6, pady=4)
        log_box.pack(fill=tk.BOTH, expand=False, side=tk.BOTTOM, padx=4, pady=4, ipady=2)

        self.log_text = tk.Text(log_box, height=8, font=("Consolas", 9), bg="#0f172a", fg="#e2e8f0",
                                wrap=tk.WORD, relief=tk.SUNKEN)
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        log_scroll = ttk.Scrollbar(log_box, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=log_scroll.set)

    # ---------------- MATRIX BUILDERS ----------------
    def _build_matrix_tab(self, parent, title, m_type):
        for widget in parent.winfo_children():
            widget.destroy()

        top_bar = tk.Frame(parent, pady=4, padx=6)
        top_bar.pack(fill=tk.X)
        tk.Label(top_bar, text=title, font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        if m_type in ("alloc", "max", "request"):
            save_btn = ttk.Button(top_bar, text="Save Changes", command=self._read_ui_matrices)
            save_btn.pack(side=tk.RIGHT)

        grid_frame = tk.Frame(parent, padx=10, pady=8)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        # Column headers (R0, R1, ...)
        tk.Label(grid_frame, text="Process", font=("Helvetica", 9, "bold"), width=8).grid(row=0, column=0, padx=4, pady=4)
        for j in range(self.m):
            tk.Label(grid_frame, text=f"R{j}", font=("Helvetica", 9, "bold"), width=6).grid(row=0, column=j+1, padx=4, pady=4)

        entries = []
        for i in range(self.n):
            row_entries = []
            tk.Label(grid_frame, text=f"P{i}", font=("Helvetica", 9, "bold")).grid(row=i+1, column=0, padx=4, pady=2)
            for j in range(self.m):
                if m_type == "need":
                    val_lbl = tk.Label(grid_frame, text="0", font=("Helvetica", 9), width=6, relief=tk.RIDGE, bg="#f1f5f9")
                    val_lbl.grid(row=i+1, column=j+1, padx=3, pady=2)
                    row_entries.append(val_lbl)
                else:
                    ent = ttk.Entry(grid_frame, width=6, justify="center")
                    ent.grid(row=i+1, column=j+1, padx=3, pady=2)
                    row_entries.append(ent)
            entries.append(row_entries)

        if m_type == "alloc":
            self.entries_alloc = entries
        elif m_type == "max":
            self.entries_max = entries
        elif m_type == "need":
            self.labels_need = entries
        elif m_type == "request":
            self.entries_request = entries

    def _build_avail_tab(self, parent):
        for widget in parent.winfo_children():
            widget.destroy()

        top_bar = tk.Frame(parent, pady=4, padx=6)
        top_bar.pack(fill=tk.X)
        tk.Label(top_bar, text="Available Resource Vector", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
        save_btn = ttk.Button(top_bar, text="Save Changes", command=self._read_ui_matrices)
        save_btn.pack(side=tk.RIGHT)

        grid_frame = tk.Frame(parent, padx=10, pady=10)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        for j in range(self.m):
            tk.Label(grid_frame, text=f"R{j}", font=("Helvetica", 9, "bold"), width=6).grid(row=0, column=j, padx=6, pady=4)

        self.entries_avail = []
        for j in range(self.m):
            ent = ttk.Entry(grid_frame, width=6, justify="center")
            ent.grid(row=1, column=j, padx=6, pady=4)
            self.entries_avail.append(ent)

    # ---------------- DATA SYNCHRONIZATION ----------------
    def _sync_matrices_to_ui(self):
        """Pushes internal data models to UI entries."""
        for i in range(self.n):
            for j in range(self.m):
                if i < len(self.entries_alloc) and j < len(self.entries_alloc[i]):
                    self.entries_alloc[i][j].delete(0, tk.END)
                    self.entries_alloc[i][j].insert(0, str(self.alloc[i][j]))
                if i < len(self.entries_max) and j < len(self.entries_max[i]):
                    self.entries_max[i][j].delete(0, tk.END)
                    self.entries_max[i][j].insert(0, str(self.max_mat[i][j]))
                if i < len(self.labels_need) and j < len(self.labels_need[i]):
                    self.labels_need[i][j].config(text=str(self.need[i][j]))
                if i < len(self.entries_request) and j < len(self.entries_request[i]):
                    self.entries_request[i][j].delete(0, tk.END)
                    self.entries_request[i][j].insert(0, str(self.request[i][j]))

        for j in range(self.m):
            if j < len(self.entries_avail):
                self.entries_avail[j].delete(0, tk.END)
                self.entries_avail[j].insert(0, str(self.avail[j]))

    def _read_ui_matrices(self):
        """Reads entries from UI and updates internal state with validation."""
        try:
            new_alloc = []
            for i in range(self.n):
                row = []
                for j in range(self.m):
                    v = int(self.entries_alloc[i][j].get().strip())
                    if v < 0:
                        raise ValueError(f"Negative allocation at P{i}, R{j}")
                    row.append(v)
                new_alloc.append(row)

            new_max = []
            for i in range(self.n):
                row = []
                for j in range(self.m):
                    v = int(self.entries_max[i][j].get().strip())
                    if v < 0:
                        raise ValueError(f"Negative max requirement at P{i}, R{j}")
                    if v < new_alloc[i][j]:
                        raise ValueError(f"Max[{i}][{j}] ({v}) is less than Allocation ({new_alloc[i][j]})")
                    row.append(v)
                new_max.append(row)

            new_avail = []
            for j in range(self.m):
                v = int(self.entries_avail[j].get().strip())
                if v < 0:
                    raise ValueError(f"Negative available at R{j}")
                new_avail.append(v)

            new_req = []
            for i in range(self.n):
                row = []
                for j in range(self.m):
                    v = int(self.entries_request[i][j].get().strip())
                    if v < 0:
                        raise ValueError(f"Negative request at P{i}, R{j}")
                    row.append(v)
                new_req.append(row)

            self.alloc = new_alloc
            self.max_mat = new_max
            self.avail = new_avail
            self.request = new_req
            self._recalculate_need()
            self._sync_matrices_to_ui()
            self._redraw_rag()
            self.log_message("[UPDATE]: Matrices validated and successfully updated.")
            return True
        except ValueError as err:
            messagebox.showerror("Validation Error", f"Invalid matrix input:\n{err}")
            return False

    def log_message(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def _set_status_badge(self, status, text):
        self.system_status = status
        if status == "SAFE":
            self.status_badge.config(text=f" [ {text} ] ", bg="#10b981")
        elif status == "UNSAFE":
            self.status_badge.config(text=f" [ {text} ] ", bg="#f59e0b")
        elif status == "DEADLOCKED":
            self.status_badge.config(text=f" [ {text} ] ", bg="#ef4444")

    # ---------------- ALGORITHMS ----------------
    def _run_bankers_algorithm(self):
        """Executes Banker's safety algorithm and returns (is_safe, sequence, trace_logs)."""
        work = list(self.avail)
        finished = [False] * self.n
        seq = []
        trace = []

        trace.append(f"Starting Banker's Safety Algorithm: Initial Work Vector = {work}")

        found = True
        while len(seq) < self.n and found:
            found = False
            for i in range(self.n):
                if not finished[i]:
                    can_run = True
                    for j in range(self.m):
                        if self.need[i][j] > work[j]:
                            can_run = False
                            break
                    if can_run:
                        trace.append(f"  -> Process P{i} can complete (Need: {self.need[i]} <= Work: {work})")
                        for j in range(self.m):
                            work[j] += self.alloc[i][j]
                        finished[i] = True
                        seq.append(i)
                        trace.append(f"     P{i} released resources. New Work = {work}")
                        found = True

        is_safe = (len(seq) == self.n)
        return is_safe, seq, trace

    def _on_check_bankers_safety(self):
        if not self._read_ui_matrices():
            return

        is_safe, seq, trace = self._run_bankers_algorithm()
        self.log_message("\n=== BANKER'S ALGORITHM SAFETY CHECK ===")
        for line in trace:
            self.log_message(line)

        if is_safe:
            seq_str = " -> ".join([f"P{p}" for p in seq])
            self._set_status_badge("SAFE", f"SYSTEM STATE: SAFE | Sequence: {seq_str}")
            self.log_message(f">>> [RESULT]: System is in a SAFE STATE.")
            self.log_message(f">>> Safe Execution Sequence: {seq_str}\n")
            messagebox.showinfo("Banker's Algorithm: SAFE", f"The system is in a SAFE STATE!\n\nSafe Sequence:\n{seq_str}")
        else:
            self._set_status_badge("UNSAFE", "SYSTEM STATE: UNSAFE (Potential Deadlock)")
            self.log_message(">>> [ALERT]: System is in an UNSAFE STATE! No safe sequence exists.\n")
            messagebox.showwarning("Banker's Algorithm: UNSAFE", "The system is in an UNSAFE STATE!\nNo safe sequence could be found.")

        self.deadlocked_procs = []
        self._redraw_rag()

    def _on_detect_deadlock(self):
        """Executes the Multi-Resource Deadlock Detection Algorithm."""
        if not self._read_ui_matrices():
            return

        work = list(self.avail)
        finish = [False] * self.n

        # If Alloc[i] == 0 for all j, finish[i] = True
        for i in range(self.n):
            if all(self.alloc[i][j] == 0 for j in range(self.m)):
                finish[i] = True

        self.log_message("\n=== DEADLOCK DETECTION ALGORITHM ===")
        self.log_message(f"Initial Work Vector = {work}")

        found = True
        while found:
            found = False
            for i in range(self.n):
                if not finish[i]:
                    if all(self.request[i][j] <= work[j] for j in range(self.m)):
                        for j in range(self.m):
                            work[j] += self.alloc[i][j]
                        finish[i] = True
                        found = True
                        self.log_message(f"  -> Process P{i} can satisfy request {self.request[i]} with Work. Frees allocation. New Work: {work}")

        deadlocked = [i for i in range(self.n) if not finish[i]]
        self.deadlocked_procs = deadlocked

        if deadlocked:
            dl_str = ", ".join([f"P{p}" for p in deadlocked])
            self._set_status_badge("DEADLOCKED", f"DEADLOCK DETECTED! Involving: {dl_str}")
            self.log_message(f">>> [ALERT]: Deadlock detected! Number of deadlocked processes: {len(deadlocked)}")
            self.log_message(f">>> Deadlocked processes: {dl_str}\n")
            self._redraw_rag()
            messagebox.showerror("Deadlock Detection: DEADLOCK!",
                                 f"DEADLOCK DETECTED!\n\nThe following processes are deadlocked:\n{dl_str}\n\nInitiate Deadlock Recovery to resolve.")
        else:
            self._set_status_badge("SAFE", "NO DEADLOCK DETECTED")
            self.log_message(">>> [OK]: No deadlock detected in the system. All processes can complete.\n")
            self._redraw_rag()
            messagebox.showinfo("Deadlock Detection: OK", "No deadlock detected! All processes can proceed to completion.")

    # ---------------- REQUEST DIALOG ----------------
    def _on_open_request_dialog(self):
        if not self._read_ui_matrices():
            return

        dlg = tk.Toplevel(self.root)
        dlg.title("Submit Resource Request (Banker's Avoidance)")
        dlg.geometry("420x300")
        dlg.transient(self.root)
        dlg.grab_set()

        tk.Label(dlg, text="Request Resources for Process", font=("Helvetica", 11, "bold")).pack(pady=8)

        p_frame = tk.Frame(dlg)
        p_frame.pack(pady=5)
        tk.Label(p_frame, text="Select Process:", font=("Helvetica", 9, "bold")).pack(side=tk.LEFT, padx=5)
        proc_combo = ttk.Combobox(p_frame, values=[f"P{i}" for i in range(self.n)], state="readonly", width=8)
        proc_combo.current(0)
        proc_combo.pack(side=tk.LEFT, padx=5)

        req_frame = tk.LabelFrame(dlg, text=" Request Vector ", padx=10, pady=10)
        req_frame.pack(pady=10, padx=15, fill=tk.X)

        req_entries = []
        for j in range(self.m):
            sub = tk.Frame(req_frame)
            sub.pack(side=tk.LEFT, expand=True, padx=4)
            tk.Label(sub, text=f"R{j}").pack()
            ent = ttk.Entry(sub, width=6, justify="center")
            ent.insert(0, "0")
            ent.pack()
            req_entries.append(ent)

        def submit():
            try:
                p_idx = int(proc_combo.get().replace("P", ""))
                req_vec = [int(ent.get().strip()) for ent in req_entries]
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
                return

            # Banker's rule 1: Request <= Need
            for j in range(self.m):
                if req_vec[j] > self.need[p_idx][j]:
                    messagebox.showerror("Denied", f"Process P{p_idx} requested {req_vec[j]} of R{j}, which exceeds remaining Need ({self.need[p_idx][j]}).")
                    return

            # Banker's rule 2: Request <= Available
            for j in range(self.m):
                if req_vec[j] > self.avail[j]:
                    messagebox.showwarning("Must Wait", f"Process P{p_idx} requested {req_vec[j]} of R{j}, but only {self.avail[j]} are currently Available. Process must wait.")
                    return

            # Pretend allocation
            for j in range(self.m):
                self.avail[j] -= req_vec[j]
                self.alloc[p_idx][j] += req_vec[j]
                self.need[p_idx][j] -= req_vec[j]

            # Check safety
            is_safe, seq, trace = self._run_bankers_algorithm()
            if is_safe:
                seq_str = " -> ".join([f"P{p}" for p in seq])
                self.log_message(f"\n[REQUEST GRANTED]: P{p_idx} requested {req_vec}. System remains SAFE.")
                self.log_message(f"Safe sequence: {seq_str}")
                self._sync_matrices_to_ui()
                self._set_status_badge("SAFE", f"REQUEST GRANTED | Safe Seq: {seq_str}")
                self._redraw_rag()
                messagebox.showinfo("Request Granted", f"Request for P{p_idx} GRANTED!\n\nThe resulting state is SAFE.\nSafe Sequence: {seq_str}")
                dlg.destroy()
            else:
                # Rollback
                for j in range(self.m):
                    self.avail[j] += req_vec[j]
                    self.alloc[p_idx][j] -= req_vec[j]
                    self.need[p_idx][j] += req_vec[j]
                self.log_message(f"\n[REQUEST REJECTED]: P{p_idx} requested {req_vec}. Allocation leaves system in UNSAFE state. Rolled back.")
                self._set_status_badge("UNSAFE", "REQUEST REJECTED (Would Cause Unsafe State)")
                messagebox.showwarning("Request Denied", f"Request for P{p_idx} DENIED!\n\nGranting this request would leave the system in an UNSAFE state.\nState rolled back.")

        btn_box = tk.Frame(dlg)
        btn_box.pack(pady=10)
        ttk.Button(btn_box, text="Submit Request", command=submit).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_box, text="Cancel", command=dlg.destroy).pack(side=tk.LEFT, padx=6)

    # ---------------- RECOVERY DIALOG ----------------
    def _on_recover_dialog(self):
        if not self._read_ui_matrices():
            return

        # Check for deadlock first
        work = list(self.avail)
        finish = [False] * self.n
        for i in range(self.n):
            if all(self.alloc[i][j] == 0 for j in range(self.m)):
                finish[i] = True
        found = True
        while found:
            found = False
            for i in range(self.n):
                if not finish[i]:
                    if all(self.request[i][j] <= work[j] for j in range(self.m)):
                        for j in range(self.m):
                            work[j] += self.alloc[i][j]
                        finish[i] = True
                        found = True
        deadlocked = [i for i in range(self.n) if not finish[i]]

        if not deadlocked:
            messagebox.showinfo("No Recovery Needed", "The system is currently NOT in deadlock.\nNo recovery action is required.")
            return

        dlg = tk.Toplevel(self.root)
        dlg.title("Deadlock Recovery")
        dlg.geometry("450x320")
        dlg.transient(self.root)
        dlg.grab_set()

        tk.Label(dlg, text="Deadlock Recovery Strategies", font=("Helvetica", 11, "bold")).pack(pady=8)
        tk.Label(dlg, text=f"Currently deadlocked processes: {', '.join([f'P{p}' for p in deadlocked])}",
                 font=("Helvetica", 9, "bold"), fg="#ef4444").pack(pady=4)

        opt_frame = tk.LabelFrame(dlg, text=" Select Recovery Method ", padx=10, pady=10)
        opt_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        var_mode = tk.IntVar(value=1)
        r1 = ttk.Radiobutton(opt_frame, text="Auto Greedy Abort (Terminates process holding most resources)", variable=var_mode, value=1)
        r1.pack(anchor=tk.W, pady=3)

        r2 = ttk.Radiobutton(opt_frame, text="Manual Abort: Select specific victim process", variable=var_mode, value=2)
        r2.pack(anchor=tk.W, pady=3)

        v_frame = tk.Frame(opt_frame)
        v_frame.pack(anchor=tk.W, padx=25, pady=2)
        tk.Label(v_frame, text="Victim Process:").pack(side=tk.LEFT)
        victim_combo = ttk.Combobox(v_frame, values=[f"P{p}" for p in deadlocked], state="readonly", width=8)
        victim_combo.current(0)
        victim_combo.pack(side=tk.LEFT, padx=6)

        def execute_recovery():
            mode = var_mode.get()
            if mode == 1:
                # Greedy: find process holding most resources
                best_victim = -1
                max_held = -1
                for p in deadlocked:
                    held = sum(self.alloc[p])
                    if held > max_held:
                        max_held = held
                        best_victim = p
                victim = best_victim
            else:
                victim = int(victim_combo.get().replace("P", ""))

            # Abort victim process: reclaim resources
            freed_summary = []
            for j in range(self.m):
                freed = self.alloc[victim][j]
                if freed > 0:
                    self.avail[j] += freed
                    freed_summary.append(f"R{j}: +{freed}")
                self.alloc[victim][j] = 0
                self.request[victim][j] = 0
                self.max_mat[victim][j] = 0
                self.need[victim][j] = 0

            self.log_message(f"\n[RECOVERY]: Aborted Process P{victim}.")
            self.log_message(f"Reclaimed resources: {', '.join(freed_summary) if freed_summary else 'None'}")
            self.log_message(f"New Available Vector: {self.avail}")

            self._sync_matrices_to_ui()
            dlg.destroy()

            # Re-run deadlock detection
            self._on_detect_deadlock()

        btn_bar = tk.Frame(dlg)
        btn_bar.pack(pady=10)
        ttk.Button(btn_bar, text="Execute Recovery", command=execute_recovery).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_bar, text="Cancel", command=dlg.destroy).pack(side=tk.LEFT, padx=6)

    # ---------------- PRESETS & RESIZE ----------------
    def _on_load_preset(self):
        idx = self.preset_combo.current()
        if idx == 0:
            # Preset 1: Silberschatz Safe State
            self._init_default_data()
            self.log_message("[PRESET LOADED]: Preset 1 - Silberschatz Safe State Benchmark (5x3).")
        elif idx == 1:
            # Preset 2: Circular Wait Deadlock
            self.n = 3
            self.m = 3
            self.alloc = [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ]
            self.max_mat = [
                [1, 1, 0],
                [0, 1, 1],
                [1, 0, 1]
            ]
            self.avail = [0, 0, 0]
            self.request = [
                [0, 1, 0],  # P0 requests R1
                [0, 0, 1],  # P1 requests R2
                [1, 0, 0]   # P2 requests R0
            ]
            self._recalculate_need()
            self.deadlocked_procs = [0, 1, 2]
            self.system_status = "DEADLOCKED"
            self.log_message("[PRESET LOADED]: Preset 2 - Active Circular Wait Deadlock (P0->P1->P2).")
        elif idx == 2:
            # Preset 3: Multi-Process Deadlock
            self.n = 4
            self.m = 3
            self.alloc = [
                [2, 0, 0],
                [0, 1, 1],
                [0, 1, 0],
                [1, 0, 1]
            ]
            self.max_mat = [
                [2, 1, 0],
                [1, 1, 1],
                [0, 2, 0],
                [1, 1, 1]
            ]
            self.avail = [0, 0, 0]
            self.request = [
                [0, 1, 0],
                [1, 0, 0],
                [0, 0, 1],
                [0, 1, 0]
            ]
            self._recalculate_need()
            self.deadlocked_procs = [0, 1, 2, 3]
            self.system_status = "DEADLOCKED"
            self.log_message("[PRESET LOADED]: Preset 3 - Multi-Process Deadlock (4x3).")
        elif idx == 3:
            # Preset 4: Unsafe State but not deadlocked (no pending requests)
            self.n = 3
            self.m = 1
            self.alloc = [[1], [1], [0]]
            self.max_mat = [[2], [2], [2]]
            self.avail = [0]
            self.request = [[0], [0], [0]]
            self._recalculate_need()
            self.deadlocked_procs = []
            self.system_status = "UNSAFE"
            self.log_message("[PRESET LOADED]: Preset 4 - Unsafe State with No Active Deadlock (Distinction Test).")

        self.n_spin.set(self.n)
        self.m_spin.set(self.m)
        self._rebuild_all_matrix_tabs()
        self._sync_matrices_to_ui()
        self._redraw_rag()
        if self.system_status == "DEADLOCKED":
            self._set_status_badge("DEADLOCKED", "DEADLOCK DETECTED (Preset)")
        elif self.system_status == "UNSAFE":
            self._set_status_badge("UNSAFE", "UNSAFE STATE (Preset)")
        else:
            self._set_status_badge("SAFE", "SYSTEM STATE: SAFE")

    def _on_resize_matrices(self):
        try:
            new_n = int(self.n_spin.get())
            new_m = int(self.m_spin.get())
            if not (1 <= new_n <= 10 and 1 <= new_m <= 10):
                raise ValueError("N and M must be between 1 and 10.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid dimensions: {e}")
            return

        new_alloc = [[0] * new_m for _ in range(new_n)]
        new_max = [[0] * new_m for _ in range(new_n)]
        new_req = [[0] * new_m for _ in range(new_n)]
        new_avail = [0] * new_m

        for i in range(min(self.n, new_n)):
            for j in range(min(self.m, new_m)):
                new_alloc[i][j] = self.alloc[i][j]
                new_max[i][j] = self.max_mat[i][j]
                new_req[i][j] = self.request[i][j]

        for j in range(min(self.m, new_m)):
            new_avail[j] = self.avail[j]

        self.n = new_n
        self.m = new_m
        self.alloc = new_alloc
        self.max_mat = new_max
        self.avail = new_avail
        self.request = new_req
        self._recalculate_need()
        self.deadlocked_procs = []

        self._rebuild_all_matrix_tabs()
        self._sync_matrices_to_ui()
        self._redraw_rag()
        self.log_message(f"[RESIZED]: System dimensions set to {self.n} Processes x {self.m} Resources.")

    def _rebuild_all_matrix_tabs(self):
        self._build_matrix_tab(self.tab_alloc, "Allocation Matrix (Alloc[i][j])", "alloc")
        self._build_matrix_tab(self.tab_max, "Maximum Requirement Matrix (Max[i][j])", "max")
        self._build_matrix_tab(self.tab_need, "Need Matrix (Need = Max - Alloc)", "need")
        self._build_avail_tab(self.tab_avail)
        self._build_matrix_tab(self.tab_request, "Outstanding Request Matrix (Req[i][j])", "request")

    def _on_reset(self):
        self._init_default_data()
        self.n_spin.set(self.n)
        self.m_spin.set(self.m)
        self._rebuild_all_matrix_tabs()
        self._sync_matrices_to_ui()
        self._redraw_rag()
        self._set_status_badge("SAFE", "SYSTEM STATE: SAFE")
        self.log_message("[RESET]: Simulation reset to initial benchmark state.")

    # ---------------- RESOURCE ALLOCATION GRAPH (RAG) DRAWING ----------------
    def _redraw_rag(self):
        """Draws the Resource Allocation Graph on the Tkinter canvas."""
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w < 50 or h < 50:
            w, h = 540, 420

        # Calculate circular layout coordinates for processes and resources
        cx, cy = w / 2, h / 2
        r_procs = min(w, h) * 0.36
        r_res = min(w, h) * 0.20

        # Positions for processes
        proc_coords = {}
        for i in range(self.n):
            angle = 2 * math.pi * i / self.n - (math.pi / 2)
            px = cx + r_procs * math.cos(angle)
            py = cy + r_procs * math.sin(angle)
            proc_coords[i] = (px, py)

        # Positions for resources
        res_coords = {}
        for j in range(self.m):
            angle = 2 * math.pi * j / self.m - (math.pi / 2)
            rx = cx + r_res * math.cos(angle)
            ry = cy + r_res * math.sin(angle)
            res_coords[j] = (rx, ry)

        # 1. Draw Allocation Edges: R_j -> P_i (Solid line with arrow)
        for i in range(self.n):
            for j in range(self.m):
                count = self.alloc[i][j]
                if count > 0:
                    rx, ry = res_coords[j]
                    px, py = proc_coords[i]
                    is_dl_edge = (i in self.deadlocked_procs)
                    edge_color = "#dc2626" if is_dl_edge else "#2563eb"
                    width = 2 if is_dl_edge else 1.5

                    # Draw line from resource edge to process edge
                    self.canvas.create_line(rx, ry, px, py, arrow=tk.LAST, arrowshape=(10, 12, 4),
                                            fill=edge_color, width=width)
                    # Label
                    mid_x = (rx * 0.4 + px * 0.6)
                    mid_y = (ry * 0.4 + py * 0.6)
                    self.canvas.create_rectangle(mid_x - 7, mid_y - 7, mid_x + 7, mid_y + 7,
                                                fill="#ffffff", outline=edge_color)
                    self.canvas.create_text(mid_x, mid_y, text=str(count), font=("Helvetica", 8, "bold"), fill=edge_color)

        # 2. Draw Request Edges: P_i -> R_j (Dashed line with arrow)
        for i in range(self.n):
            for j in range(self.m):
                count = self.request[i][j]
                if count > 0:
                    px, py = proc_coords[i]
                    rx, ry = res_coords[j]
                    is_dl_edge = (i in self.deadlocked_procs)
                    edge_color = "#dc2626" if is_dl_edge else "#d97706"
                    width = 2.5 if is_dl_edge else 1.5

                    self.canvas.create_line(px, py, rx, ry, arrow=tk.LAST, arrowshape=(10, 12, 4),
                                            dash=(4, 3), fill=edge_color, width=width)
                    mid_x = (px * 0.6 + rx * 0.4)
                    mid_y = (py * 0.6 + ry * 0.4)
                    self.canvas.create_rectangle(mid_x - 7, mid_y - 7, mid_x + 7, mid_y + 7,
                                                fill="#ffffff", outline=edge_color)
                    self.canvas.create_text(mid_x, mid_y, text=str(count), font=("Helvetica", 8, "bold"), fill=edge_color)

        # 3. Draw Process Nodes (Circles)
        radius = 20
        for i in range(self.n):
            px, py = proc_coords[i]
            is_dl = (i in self.deadlocked_procs)
            fill_color = "#fee2e2" if is_dl else "#e0f2fe"
            border_color = "#dc2626" if is_dl else "#0284c7"
            border_width = 3 if is_dl else 2

            self.canvas.create_oval(px - radius, py - radius, px + radius, py + radius,
                                   fill=fill_color, outline=border_color, width=border_width)
            self.canvas.create_text(px, py, text=f"P{i}", font=("Helvetica", 10, "bold"),
                                   fill=border_color)

        # 4. Draw Resource Nodes (Rectangles)
        box_w, box_h = 24, 24
        for j in range(self.m):
            rx, ry = res_coords[j]
            self.canvas.create_rectangle(rx - box_w, ry - box_h, rx + box_w, ry + box_h,
                                        fill="#dcfce7", outline="#16a34a", width=2)
            self.canvas.create_text(rx, ry - 7, text=f"R{j}", font=("Helvetica", 9, "bold"), fill="#15803d")
            # Show available count below
            self.canvas.create_text(rx, ry + 8, text=f"Av:{self.avail[j]}", font=("Helvetica", 7), fill="#166534")


def main():
    root = tk.Tk()
    app = DeadlockSimulatorGUI(root)
    # Re-draw RAG on canvas resize
    app.canvas.bind("<Configure>", lambda event: app._redraw_rag())
    root.mainloop()


if __name__ == "__main__":
    main()
