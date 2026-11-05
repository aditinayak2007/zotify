import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_row(row, heights=None, is_header=False, bg_color=None):
    if is_header:
        for cell in row.cells:
            set_cell_background(cell, bg_color or "E2E8F0")
            set_cell_margins(cell, top=140, bottom=140, left=150, right=150)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(10.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(27, 54, 93)
    else:
        for cell in row.cells:
            if bg_color:
                set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(45, 55, 72)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(27, 54, 93)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(44, 82, 130)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(43, 108, 176)
    return p

def add_body_p(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(30, 41, 59)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_question_box(doc, question_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    r_q = p.add_run("Question: ")
    r_q.font.name = 'Calibri'
    r_q.font.size = Pt(10.5)
    r_q.font.bold = True
    r_q.font.color.rgb = RGBColor(27, 54, 93)
    
    r_txt = p.add_run(question_text)
    r_txt.font.name = 'Calibri'
    r_txt.font.size = Pt(10.5)
    r_txt.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_screenshot_box(doc, member_name):
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(8)
    p_name.paragraph_format.space_after = Pt(2)
    p_name.paragraph_format.keep_with_next = True
    r_name = p_name.add_run(member_name)
    r_name.font.name = 'Calibri'
    r_name.font.size = Pt(11)
    r_name.font.bold = True
    r_name.font.color.rgb = RGBColor(44, 82, 130)
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=200, bottom=200, left=200, right=200)
    
    # Border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
        f'<w:bottom w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
        f'<w:left w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
        f'<w:right w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    cp = cell.paragraphs[0]
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c_run = cp.add_run("[Insert screenshot of execution here]")
    c_run.font.name = 'Calibri'
    c_run.font.size = Pt(10)
    c_run.font.italic = True
    c_run.font.color.rgb = RGBColor(100, 116, 139)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def add_code_section(doc, submitted_by, filename, code_content):
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(10)
    p_sub.paragraph_format.space_after = Pt(3)
    p_sub.paragraph_format.keep_with_next = True
    
    r_sub = p_sub.add_run(f"Submitted by: {submitted_by} ({filename})")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(10.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(27, 54, 93)
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="12" w:space="0" w:color="2C5282"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    # Add code text
    lines = code_content.strip().split('\n')
    # If the file is very large, include the most representative 120 lines to keep document crisp and responsive
    if len(lines) > 250:
        lines = lines[:230] + [f"\n// ... [Remainder of {filename} ({len(lines)} total lines) truncated for report conciseness. Full source available in project repository] ..."]
    
    formatted_code = '\n'.join(lines)
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(0)
    cp.paragraph_format.line_spacing = 1.05
    c_run = cp.add_run(formatted_code)
    c_run.font.name = 'Consolas'
    c_run.font.size = Pt(8.5)
    c_run.font.color.rgb = RGBColor(30, 41, 59)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(6)

def read_file_safe(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    return "// File not found."

def build_document():
    doc = docx.Document()
    
    # Set page layout to Letter/A4 with 1-inch margins
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11.0)
        
    base_dir = r"C:\Users\Aditi Nayak\.gemini\antigravity\scratch\zotify"
    
    # ==========================================
    # 1. COVER PAGE
    # ==========================================
    p_cov_sp1 = doc.add_paragraph()
    p_cov_sp1.paragraph_format.space_before = Pt(24)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Report on Project Based Learning (PBL)")
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(27, 54, 93)
    
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_after = Pt(14)
    r_date = p_date.add_run("Nov 5, 2026")
    r_date.font.name = 'Calibri'
    r_date.font.size = Pt(11)
    r_date.font.color.rgb = RGBColor(100, 116, 139)
    
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(18)
    r_inst = p_inst.add_run("St. Aloysius (Deemed to be University), School of Engineering, Mangaluru")
    r_inst.font.name = 'Calibri'
    r_inst.font.size = Pt(12)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(45, 55, 72)
    
    # Logo Placeholder Box
    logo_table = doc.add_table(rows=1, cols=1)
    logo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    l_cell = logo_table.cell(0, 0)
    l_cell.width = Inches(3.2)
    set_cell_background(l_cell, "F1F5F9")
    set_cell_margins(l_cell, top=260, bottom=260, left=180, right=180)
    tcPr = l_cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
        f'<w:bottom w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
        f'<w:left w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
        f'<w:right w:val="dashed" w:sz="6" w:space="0" w:color="94A3B8"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    lp = l_cell.paragraphs[0]
    lp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    lr = lp.add_run("[College logo: insert here]")
    lr.font.name = 'Calibri'
    lr.font.size = Pt(10.5)
    lr.font.italic = True
    lr.font.color.rgb = RGBColor(100, 116, 139)
    
    p_course_sp = doc.add_paragraph()
    p_course_sp.paragraph_format.space_before = Pt(20)
    p_course_sp.paragraph_format.space_after = Pt(2)
    
    p_c1 = doc.add_paragraph()
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c1.paragraph_format.space_after = Pt(3)
    rc1 = p_c1.add_run("Course: Operating Systems (OSCO). Course code: [OSCO course code]")
    rc1.font.name = 'Calibri'
    rc1.font.size = Pt(11)
    rc1.font.color.rgb = RGBColor(51, 65, 85)
    
    p_c2 = doc.add_paragraph()
    p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c2.paragraph_format.space_after = Pt(14)
    rc2 = p_c2.add_run("Course: Data Structures & Algorithms (DSA). Course code: [DSA course code]")
    rc2.font.name = 'Calibri'
    rc2.font.size = Pt(11)
    rc2.font.color.rgb = RGBColor(51, 65, 85)
    
    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_after = Pt(18)
    r_proj = p_proj.add_run("Project title: OS Simulators: IPC, CPU Scheduling, Deadlock and Page Replacement")
    r_proj.font.name = 'Calibri'
    r_proj.font.size = Pt(12)
    r_proj.font.bold = True
    r_proj.font.color.rgb = RGBColor(27, 54, 93)
    
    # Submitted by Table
    p_sub_lbl = doc.add_paragraph()
    p_sub_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub_lbl.paragraph_format.space_after = Pt(4)
    r_sub_lbl = p_sub_lbl.add_run("Submitted by:")
    r_sub_lbl.font.name = 'Calibri'
    r_sub_lbl.font.size = Pt(11)
    r_sub_lbl.font.bold = True
    r_sub_lbl.font.color.rgb = RGBColor(45, 55, 72)
    
    sub_table = doc.add_table(rows=5, cols=2)
    sub_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sub_table, color="CBD5E1")
    
    sub_headers = ["Registration No.", "Name"]
    sub_data = [
        ["25192102", "Aditi Nayak (Leader)"],
        ["[Reg No]", "Anas Ahmed"],
        ["[Reg No]", "Nireeksha"],
        ["[Reg No]", "Yaseem"]
    ]
    
    col_widths = [Inches(2.2), Inches(3.0)]
    for j, h in enumerate(sub_headers):
        sub_table.cell(0, j).text = h
        sub_table.cell(0, j).width = col_widths[j]
    format_row(sub_table.rows[0], is_header=True, bg_color="E2E8F0")
    
    for i, row_data in enumerate(sub_data):
        row = sub_table.rows[i+1]
        for j, val in enumerate(row_data):
            row.cells[j].text = val
            row.cells[j].width = col_widths[j]
        format_row(row, bg_color="FFFFFF" if i%2==0 else "F8FAFC")
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        
    p_sup = doc.add_paragraph()
    p_sup.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sup.paragraph_format.space_before = Pt(28)
    r_sup = p_sup.add_run("Under the supervision of: [Faculty name, designation]")
    r_sup.font.name = 'Calibri'
    r_sup.font.size = Pt(11)
    r_sup.font.italic = True
    r_sup.font.color.rgb = RGBColor(71, 85, 105)
    
    doc.add_page_break()
    
    # ==========================================
    # 2. INDEX PAGE
    # ==========================================
    add_heading_1(doc, "Index")
    
    idx_table = doc.add_table(rows=6, cols=4)
    idx_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(idx_table, color="CBD5E1")
    
    idx_headers = ["Week", "Title", "Date", "Remarks"]
    idx_data = [
        ["Week 1", "IPC techniques", "[dd/mm/yyyy]", "Completed"],
        ["Week 2", "Multiple processes Simulator", "[dd/mm/yyyy]", "Completed"],
        ["Week 3", "Processes scheduling (FCFS, SJF, Round Robin)", "[dd/mm/yyyy]", "Completed"],
        ["Week 4", "Deadlock avoidance (Banker's algorithm)", "[dd/mm/yyyy]", "Completed"],
        ["Week 5", "Page replacement simulator (FIFO, LRU, Optimal)", "[dd/mm/yyyy]", "Completed"]
    ]
    
    idx_widths = [Inches(1.0), Inches(3.2), Inches(1.1), Inches(1.2)]
    for j, h in enumerate(idx_headers):
        idx_table.cell(0, j).text = h
        idx_table.cell(0, j).width = idx_widths[j]
    format_row(idx_table.rows[0], is_header=True, bg_color="E2E8F0")
    
    for i, row_data in enumerate(idx_data):
        row = idx_table.rows[i+1]
        for j, val in enumerate(row_data):
            row.cells[j].text = val
            row.cells[j].width = idx_widths[j]
        format_row(row, bg_color="FFFFFF" if i%2==0 else "F8FAFC")
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    doc.add_page_break()
    
    # ==========================================
    # 3. WEEK 1: IPC TECHNIQUES
    # ==========================================
    add_heading_1(doc, "Week 1: IPC techniques")
    add_body_p(doc, "[dd/mm/yyyy]", bold_prefix="Date: ")
    add_question_box(doc, "Implement two inter-process communication (IPC) techniques, a pipe and shared memory, and show how two processes exchange data using each of them.")
    
    add_heading_2(doc, "Team Members")
    add_screenshot_box(doc, "Aditi Nayak")
    add_screenshot_box(doc, "Anas Ahmed")
    add_screenshot_box(doc, "Nireeksha")
    add_screenshot_box(doc, "Yaseem")
    
    add_heading_2(doc, "How the Work Was Divided")
    add_body_p(doc, "In Week 1, our team explored and implemented foundational Inter-Process Communication (IPC) mechanisms in modern Operating Systems. In an operating system, processes execute with private and isolated virtual memory address spaces to maintain system safety. To exchange data, synchronize concurrent activities, or coordinate distributed computational workflows, processes must leverage IPC mechanisms managed by the kernel. Our team divided the responsibilities across four distinct IPC techniques: Pipes, Sockets, Shared Memory, and Message Queues.")
    
    w1_div_table = doc.add_table(rows=5, cols=3)
    w1_div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(w1_div_table, color="CBD5E1")
    
    w1_headers = ["Member", "Responsibility", "IPC Technique"]
    w1_data = [
        ["Aditi Nayak (Leader)", "Anonymous and Named Pipes IPC implementation & stream analysis", "Pipes"],
        ["Anas Ahmed", "Client-Server Socket communication & port endpoint exchange", "Sockets"],
        ["Nireeksha", "POSIX Shared Memory (shm_open, mmap) & synchronization", "Shared Memory"],
        ["Yaseem", "POSIX Message Queues and asynchronous signal handling", "Message Queues / Signals"]
    ]
    w1_col_widths = [Inches(1.8), Inches(3.2), Inches(1.5)]
    for j, h in enumerate(w1_headers):
        w1_div_table.cell(0, j).text = h
        w1_div_table.cell(0, j).width = w1_col_widths[j]
    format_row(w1_div_table.rows[0], is_header=True, bg_color="E2E8F0")
    for i, row_data in enumerate(w1_data):
        row = w1_div_table.rows[i+1]
        for j, val in enumerate(row_data):
            row.cells[j].text = val
            row.cells[j].width = w1_col_widths[j]
        format_row(row, bg_color="FFFFFF" if i%2==0 else "F8FAFC")
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    add_heading_2(doc, "Technical Overview of Implemented Techniques")
    add_heading_3(doc, "1. Pipes (Anonymous & Named Pipes)")
    add_body_p(doc, "A pipe is an IPC mechanism that provides a unidirectional byte stream connecting two processes. In an anonymous pipe created via the pipe() system call, two file descriptors are allocated: fd[0] for reading and fd[1] for writing. Data written by the parent process is buffered by the kernel and sequentially retrieved by the child process in FIFO order. Named pipes (FIFOs) extend this model across unrelated processes via a designated file system node created with mkfifo().")
    
    add_heading_3(doc, "2. Shared Memory")
    add_body_p(doc, "Shared Memory is the fastest IPC technique because the operating system maps an identical physical memory segment into the virtual address spaces of multiple processes. Once mapped using shm_open() and mmap(), processes read and write directly to memory without kernel copy overhead. To prevent race conditions, POSIX semaphores (sem_wait and sem_post) coordinate concurrent accesses.")
    
    add_heading_3(doc, "3. Sockets")
    add_body_p(doc, "Sockets provide bidirectional network and local (UNIX domain) endpoints. A server process creates a socket, binds it to an address/port, listens for incoming connections, and accepts client sessions. Sockets allow processes to communicate across different machines or locally on the same host.")
    
    add_heading_3(doc, "4. Message Queues")
    add_body_p(doc, "Message queues store discrete, structured messages in a kernel-managed queue. Processes send messages with assigned priority levels using mq_send() and receive them with mq_receive(). This enables asynchronous, decoupled communication without requiring both processes to be active simultaneously.")
    
    add_heading_2(doc, "Code")
    
    # Week 1 Code samples
    pipe_sample = """// Week 1: Pipes IPC Implementation (pipe_ipc.c)
// Submitted by: Aditi Nayak (25192102)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    int fd[2]; // fd[0]: read end, fd[1]: write end
    pid_t pid;
    char write_msg[] = "Hello from Parent via Pipe!";
    char read_msg[100];

    // Create anonymous pipe
    if (pipe(fd) == -1) {
        perror("Pipe creation failed");
        return 1;
    }

    pid = fork();
    if (pid < 0) {
        perror("Fork failed");
        return 1;
    }

    if (pid > 0) { // Parent process: Sender
        close(fd[0]); // Close unused read end
        printf("[Parent] Writing message to pipe: '%s'\\n", write_msg);
        write(fd[1], write_msg, strlen(write_msg) + 1);
        close(fd[1]); // Close write end to signal EOF
        wait(NULL);   // Wait for child to complete
    } else { // Child process: Receiver
        close(fd[1]); // Close unused write end
        read(fd[0], read_msg, sizeof(read_msg));
        printf("[Child] Read message from pipe: '%s'\\n", read_msg);
        close(fd[0]);
        exit(0);
    }
    return 0;
}"""
    add_code_section(doc, "Aditi Nayak", "pipe_ipc.c", pipe_sample)
    
    shm_sample = """// Week 1: Shared Memory IPC Implementation (shm_ipc.c)
// Submitted by: Nireeksha
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/wait.h>

#define SHM_NAME "/pbl_shared_mem"
#define SHM_SIZE 1024

int main() {
    pid_t pid;
    int shm_fd;
    char *ptr;

    // Create shared memory object
    shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    ftruncate(shm_fd, SHM_SIZE);
    ptr = (char *)mmap(0, SHM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);

    pid = fork();
    if (pid > 0) { // Parent writes
        const char *msg = "Shared Memory Data Segment: OSCO PBL Week 1";
        sprintf(ptr, "%s", msg);
        printf("[Parent] Written to Shared Memory: '%s'\\n", msg);
        wait(NULL);
        shm_unlink(SHM_NAME); // Clean up
    } else if (pid == 0) { // Child reads
        sleep(1); // Allow parent to write
        printf("[Child] Read from Shared Memory: '%s'\\n", ptr);
        exit(0);
    }
    return 0;
}"""
    add_code_section(doc, "Nireeksha", "shm_ipc.c", shm_sample)
    
    socket_sample = """// Week 1: Socket IPC Implementation (socket_ipc.c)
// Submitted by: Anas Ahmed
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 8080

void run_server() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1, addrlen = sizeof(address);
    char buffer[1024] = {0};

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 3);
    printf("[Server] Listening on port %d...\\n", PORT);
    new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
    read(new_socket, buffer, 1024);
    printf("[Server] Received: '%s'\\n", buffer);
    send(new_socket, "ACK from Server", 15, 0);
    close(new_socket);
    close(server_fd);
}"""
    add_code_section(doc, "Anas Ahmed", "socket_ipc.c", socket_sample)
    
    mq_sample = """// Week 1: POSIX Message Queue Implementation (msgqueue_ipc.c)
// Submitted by: Yaseem
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <mqueue.h>
#include <unistd.h>

#define QUEUE_NAME "/pbl_msg_queue"
#define MAX_SIZE 128

int main() {
    mqd_t mq;
    struct mq_attr attr;
    char buffer[MAX_SIZE];

    attr.mq_flags = 0;
    attr.mq_maxmsg = 10;
    attr.mq_msgsize = MAX_SIZE;
    attr.mq_curmsgs = 0;

    mq = mq_open(QUEUE_NAME, O_CREAT | O_RDWR, 0644, &attr);
    if (fork() > 0) { // Sender
        const char *msg = "Message Queue Payload";
        mq_send(mq, msg, strlen(msg) + 1, 1);
        printf("[Sender] Sent message: '%s'\\n", msg);
        sleep(1);
        mq_close(mq);
        mq_unlink(QUEUE_NAME);
    } else { // Receiver
        sleep(1);
        mq_receive(mq, buffer, MAX_SIZE, NULL);
        printf("[Receiver] Retrieved message: '%s'\\n", buffer);
        mq_close(mq);
        exit(0);
    }
    return 0;
}"""
    add_code_section(doc, "Yaseem", "msgqueue_ipc.c", mq_sample)
    
    doc.add_page_break()
    
    # ==========================================
    # 4. WEEK 2: MULTIPLE PROCESSES SIMULATOR
    # ==========================================
    add_heading_1(doc, "Week 2: Multiple processes Simulator")
    add_body_p(doc, "[dd/mm/yyyy]", bold_prefix="Date: ")
    add_question_box(doc, "Build a simple CPU simulator (accumulator, memory, stack and instruction queue) as three separate processes, a UI process, a Core process and a Logger process, that exchange data using IPC techniques.")
    
    add_heading_2(doc, "How the Work Was Divided")
    w2_div_table = doc.add_table(rows=5, cols=4)
    w2_div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(w2_div_table, color="CBD5E1")
    
    w2_headers = ["Part", "Owner", "File", "IPC technique"]
    w2_data = [
        ["UI Process", "Anas Ahmed", "ui.c", "POSIX Pipes"],
        ["CPU Core Process", "Nireeksha", "core.c", "POSIX Pipes"],
        ["Logger Process", "Yaseem", "logger.c", "POSIX Pipes"],
        ["Integration & IPC Setup", "Aditi Nayak (Leader)", "main.c, pipe_ipc.h", "Named / Anonymous Pipes"]
    ]
    w2_col_widths = [Inches(1.8), Inches(1.5), Inches(1.7), Inches(1.5)]
    for j, h in enumerate(w2_headers):
        w2_div_table.cell(0, j).text = h
        w2_div_table.cell(0, j).width = w2_col_widths[j]
    format_row(w2_div_table.rows[0], is_header=True, bg_color="E2E8F0")
    for i, row_data in enumerate(w2_data):
        row = w2_div_table.rows[i+1]
        for j, val in enumerate(row_data):
            row.cells[j].text = val
            row.cells[j].width = w2_col_widths[j]
        format_row(row, bg_color="FFFFFF" if i%2==0 else "F8FAFC")
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        row.cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row.cells[3].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    add_heading_2(doc, "System Architecture & Inter-Process Communication Flow")
    add_body_p(doc, "The Multi-Process CPU Simulator models a complete computing system structured into three cooperating operating system processes: UI Process, CPU Core Process, and Logging Process. Inter-process communication is achieved using unidirectional POSIX Pipes configured by Aditi Nayak in pipe_ipc.h.")
    add_body_p(doc, "1. UI Process (ui.c): Accepts assembly instructions from user input or script files (LOAD, STORE, ADD, SUB, PUSH, POP, JMP, HALT), parses opcode tokens and operands, and writes serialized CPUCommand structures into the command pipe (ui_to_core_pipe).")
    add_body_p(doc, "2. CPU Core Process (core.c): Reads CPUCommand packets from the pipe, buffers them in an instruction queue, and executes each instruction against its virtual hardware components: Accumulator register (ACC), 1024-word RAM, and operand Stack. For every operation performed, the Core crafts a structured LogMessage packet containing timestamp, current PC, ACC value, and status description, and transmits it via the core_to_logger_pipe.")
    add_body_p(doc, "3. Logger Process (logger.c): Reads LogMessage packets from the logging pipe, formats log records, prints real-time events to the terminal console, and writes persistent audit records to yaseem.log.")
    add_body_p(doc, "4. Main Orchestrator (main.c): Spawns the processes via fork(), redirects pipe descriptors, handles graceful shutdown upon receiving HALT, and reaps child processes using waitpid().")
    
    add_heading_2(doc, "Code")
    add_code_section(doc, "Aditi Nayak", "pipe_ipc.h", read_file_safe(os.path.join(base_dir, "Week 2", "pipe_ipc.h")))
    add_code_section(doc, "Anas Ahmed", "ui.c", read_file_safe(os.path.join(base_dir, "Week 2", "ui.c")))
    add_code_section(doc, "Nireeksha", "core.c", read_file_safe(os.path.join(base_dir, "Week 2", "core.c")))
    add_code_section(doc, "Yaseem", "logger.c", read_file_safe(os.path.join(base_dir, "Week 2", "logger.c")))
    add_code_section(doc, "Aditi Nayak", "main.c", read_file_safe(os.path.join(base_dir, "Week 2", "main.c")))
    
    doc.add_page_break()
    
    # ==========================================
    # 5. WEEK 3: PROCESS SCHEDULING
    # ==========================================
    add_heading_1(doc, "Week 3: Processes scheduling (FCFS, SJF, Round Robin)")
    add_body_p(doc, "[dd/mm/yyyy]", bold_prefix="Date: ")
    add_question_box(doc, "Implement CPU scheduling simulators for FCFS, non-preemptive SJF and Round Robin. For each algorithm, calculate the waiting time and turnaround time of every process and the average waiting time. (Our simulator also includes SRTF and Priority scheduling, and a Compare All option.)")
    
    add_heading_2(doc, "How the Work Was Divided")
    w3_div_table = doc.add_table(rows=5, cols=2)
    w3_div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(w3_div_table, color="CBD5E1")
    
    w3_headers = ["Member", "Responsibility"]
    w3_data = [
        ["Anas Ahmed", "Input handling, FCFS and Round Robin scheduling algorithms"],
        ["Nireeksha", "Shortest Job First (SJF & SRTF) and Gantt Chart timeline visualization"],
        ["Yaseem", "Priority scheduling (Preemptive & Non-preemptive) and Performance comparison metrics"],
        ["Aditi Nayak (Leader)", "Overall system architecture, integration, validation, and interactive CLI driver"]
    ]
    w3_col_widths = [Inches(2.2), Inches(4.3)]
    for j, h in enumerate(w3_headers):
        w3_div_table.cell(0, j).text = h
        w3_div_table.cell(0, j).width = w3_col_widths[j]
    format_row(w3_div_table.rows[0], is_header=True, bg_color="E2E8F0")
    for i, row_data in enumerate(w3_data):
        row = w3_div_table.rows[i+1]
        for j, val in enumerate(row_data):
            row.cells[j].text = val
            row.cells[j].width = w3_col_widths[j]
        format_row(row, bg_color="FFFFFF" if i%2==0 else "F8FAFC")
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        
    add_heading_2(doc, "Scheduling Principles, Performance Metrics & Gantt Chart")
    add_body_p(doc, "CPU scheduling determines which ready process is allocated CPU execution time when multiple processes compete for CPU resources. Our system models six scheduling algorithms across both preemptive and non-preemptive paradigms:")
    add_body_p(doc, "1. First-Come, First-Served (FCFS): Non-preemptive scheduling where the process arriving first is dispatched first. Simple but vulnerable to the convoy effect.")
    add_body_p(doc, "2. Shortest Job First (SJF): Non-preemptive selection of the process with the lowest burst time among arrived processes. Minimizes average waiting time.")
    add_body_p(doc, "3. Shortest Remaining Time First (SRTF): Preemptive variant of SJF where newly arriving processes with shorter remaining burst preempt running processes.")
    add_body_p(doc, "4. Round Robin (RR): Preemptive time-sliced scheduling where each process receives up to a time quantum before yielding to the ready queue.")
    add_body_p(doc, "5. Priority Scheduling: Schedules processes according to assigned numerical priority, supported in both non-preemptive and preemptive modes.")
    add_body_p(doc, "Calculations & Metrics: Turnaround Time (TAT = Completion Time - Arrival Time), Waiting Time (WT = Turnaround Time - Burst Time), and Gantt Chart visual timeline representing exact CPU allocation intervals.")
    
    add_heading_2(doc, "Code")
    add_code_section(doc, "Aditi Nayak", "process.h", read_file_safe(os.path.join(base_dir, "Week 3", "process.h")))
    add_code_section(doc, "Anas Ahmed", "input.c", read_file_safe(os.path.join(base_dir, "Week 3", "input.c")))
    add_code_section(doc, "Anas Ahmed", "fcfs.c", read_file_safe(os.path.join(base_dir, "Week 3", "fcfs.c")))
    add_code_section(doc, "Nireeksha", "sjf.c", read_file_safe(os.path.join(base_dir, "Week 3", "sjf.c")))
    add_code_section(doc, "Yaseem", "priority.c", read_file_safe(os.path.join(base_dir, "Week 3", "priority.c")))
    add_code_section(doc, "Anas Ahmed", "rr.c", read_file_safe(os.path.join(base_dir, "Week 3", "rr.c")))
    add_code_section(doc, "Nireeksha", "gantt.c", read_file_safe(os.path.join(base_dir, "Week 3", "gantt.c")))
    add_code_section(doc, "Aditi Nayak", "main.c", read_file_safe(os.path.join(base_dir, "Week 3", "main.c")))
    
    doc.add_page_break()
    
    # ==========================================
    # 6. WEEK 4: DEADLOCK AVOIDANCE
    # ==========================================
    add_heading_1(doc, "Week 4: Deadlock avoidance (Banker's algorithm)")
    add_body_p(doc, "[dd/mm/yyyy]", bold_prefix="Date: ")
    add_question_box(doc, "Implement the Banker's algorithm to check whether a system is in a safe state, and print the safe sequence of processes if one exists.")
    
    add_heading_2(doc, "How the Work Was Divided")
    w4_div_table = doc.add_table(rows=5, cols=2)
    w4_div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(w4_div_table, color="CBD5E1")
    
    w4_headers = ["Member", "Responsibility"]
    w4_data = [
        ["Nireeksha", "Banker's Algorithm, Need Matrix calculation, safe/unsafe state check, and safe sequence determination"],
        ["Yaseem", "Deadlock detection, Resource Allocation Graph (RAG) cycle detection, and Deadlock recovery algorithms"],
        ["Anas Ahmed", "Interactive GUI interface (Tkinter) and Visual Resource Allocation Graph display"],
        ["Aditi Nayak (Leader)", "Backend-to-GUI integration, unified CLI simulator, testing, and debugging"]
    ]
    w4_col_widths = [Inches(2.2), Inches(4.3)]
    for j, h in enumerate(w4_headers):
        w4_div_table.cell(0, j).text = h
        w4_div_table.cell(0, j).width = w4_col_widths[j]
    format_row(w4_div_table.rows[0], is_header=True, bg_color="E2E8F0")
    for i, row_data in enumerate(w4_data):
        row = w4_div_table.rows[i+1]
        for j, val in enumerate(row_data):
            row.cells[j].text = val
            row.cells[j].width = w4_col_widths[j]
        format_row(row, bg_color="FFFFFF" if i%2==0 else "F8FAFC")
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        
    add_heading_2(doc, "Deadlock Avoidance, Detection, and Recovery Architecture")
    add_body_p(doc, "A deadlock is a condition in concurrent programming where a set of processes are blocked because each process is holding resources and waiting for other resources acquired by other processes. The four Coffman conditions for deadlock are: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait.")
    add_body_p(doc, "1. Banker's Algorithm (Avoidance): Maintains Available vector, Allocation matrix, and Max matrix. Calculates the Need matrix: Need[i][j] = Max[i][j] - Allocation[i][j]. When a resource request arrives, it simulates allocation and validates if a safe sequence exists using Work and Finish vectors.")
    add_body_p(doc, "2. Deadlock Detection: Analyzes active process allocations and pending requests. Detects circular wait conditions when processes cannot be satisfied with available resources.")
    add_body_p(doc, "3. Resource Allocation Graph (RAG): Constructs a directed bipartite graph connecting Process nodes and Resource nodes. Request edges (P -> R) and Assignment edges (R -> P) are analyzed for cycle detection using depth-first search.")
    add_body_p(doc, "4. Deadlock Recovery: Resolves deadlocks through process termination (aborting deadlocked processes in order of minimum impact) and resource preemption.")
    add_body_p(doc, "5. GUI & Integration: Anas developed the Tkinter visual frontend, and Aditi integrated the complete backend C engine, IPC bridge, argument parsing, and automated test runners.")
    
    add_heading_2(doc, "Code")
    add_code_section(doc, "Aditi Nayak", "bankers.h", read_file_safe(os.path.join(base_dir, "Week 4", "bankers.h")))
    add_code_section(doc, "Nireeksha", "bankers.c", read_file_safe(os.path.join(base_dir, "Week 4", "bankers.c")))
    add_code_section(doc, "Yaseem", "deadlock.c", read_file_safe(os.path.join(base_dir, "Week 4", "deadlock.c")))
    add_code_section(doc, "Yaseem", "rag.c", read_file_safe(os.path.join(base_dir, "Week 4", "rag.c")))
    add_code_section(doc, "Yaseem", "recovery.c", read_file_safe(os.path.join(base_dir, "Week 4", "recovery.c")))
    add_code_section(doc, "Aditi Nayak", "main.c", read_file_safe(os.path.join(base_dir, "Week 4", "main.c")))
    add_code_section(doc, "Anas Ahmed", "gui.py", read_file_safe(os.path.join(base_dir, "Week 4", "gui.py")))
    
    doc.add_page_break()
    
    # ==========================================
    # 7. WEEK 5: PAGE REPLACEMENT SIMULATOR
    # ==========================================
    add_heading_1(doc, "Week 5: Page replacement simulator (FIFO, LRU, Optimal)")
    add_body_p(doc, "[dd/mm/yyyy]", bold_prefix="Date: ")
    add_question_box(doc, "Implement page replacement algorithm simulators for FIFO, LRU, and Optimal page replacement. For each algorithm, display frame contents after every reference and compute page hits, faults, and ratios, with a Compare All option.")
    
    add_heading_2(doc, "How the Work Was Divided")
    w5_div_table = doc.add_table(rows=5, cols=2)
    w5_div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(w5_div_table, color="CBD5E1")
    
    w5_headers = ["Member", "Responsibility"]
    w5_data = [
        ["Nireeksha", "FIFO (First-In, First-Out) and LRU (Least Recently Used) page replacement algorithms"],
        ["Yaseem", "Optimal Page Replacement algorithm, metrics calculations (Hit ratio, Fault ratio), and algorithm comparative analysis"],
        ["Anas Ahmed", "Interactive GUI frontend (Tkinter) with dynamic memory frame grid visualization and step-by-step trace"],
        ["Aditi Nayak (Leader)", "Project integration, C engine orchestrator, comprehensive CLI test harness, validation, and documentation"]
    ]
    w5_col_widths = [Inches(2.2), Inches(4.3)]
    for j, h in enumerate(w5_headers):
        w5_div_table.cell(0, j).text = h
        w5_div_table.cell(0, j).width = w5_col_widths[j]
    format_row(w5_div_table.rows[0], is_header=True, bg_color="E2E8F0")
    for i, row_data in enumerate(w5_data):
        row = w5_div_table.rows[i+1]
        for j, val in enumerate(row_data):
            row.cells[j].text = val
            row.cells[j].width = w5_col_widths[j]
        format_row(row, bg_color="FFFFFF" if i%2==0 else "F8FAFC")
        row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        
    add_heading_2(doc, "Virtual Memory Demand Paging & Page Replacement Algorithms")
    add_body_p(doc, "In modern virtual memory architectures, logical address spaces are mapped to physical RAM via page tables. Under demand paging, pages are loaded into physical frames only upon execution reference. If a requested page is not in RAM, a page fault occurs, requiring the OS to bring the page from disk into a physical frame. If all frames are occupied, a page replacement algorithm chooses an existing page to replace:")
    add_body_p(doc, "1. FIFO (First-In, First-Out): Replaces the page that was loaded earliest into memory. While simple to implement using a FIFO queue, it can suffer from Belady's Anomaly where allocating more physical frames paradoxically results in more page faults.")
    add_body_p(doc, "2. LRU (Least Recently Used): Replaces the page that has not been referenced for the longest period of time. By taking advantage of temporal locality, LRU provides high hit ratios and never experiences Belady's Anomaly.")
    add_body_p(doc, "3. Optimal Page Replacement (OPT): Replaces the page that will not be accessed for the longest time in the future. Because it requires perfect future knowledge, it is an ideal theoretical benchmark to measure other algorithms.")
    add_body_p(doc, "Metrics & Calculations: Hit Ratio = (Hits / Total References) * 100%, Fault Ratio = (Faults / Total References) * 100%. Frame contents are traced and displayed step-by-step after every page reference.")
    
    add_heading_2(doc, "Code")
    add_code_section(doc, "Aditi Nayak", "page_replacement.h", read_file_safe(os.path.join(base_dir, "Week 5", "page_replacement.h")))
    add_code_section(doc, "Nireeksha", "fifo.c", read_file_safe(os.path.join(base_dir, "Week 5", "fifo.c")))
    add_code_section(doc, "Nireeksha", "lru.c", read_file_safe(os.path.join(base_dir, "Week 5", "lru.c")))
    add_code_section(doc, "Yaseem", "optimal.c", read_file_safe(os.path.join(base_dir, "Week 5", "optimal.c")))
    add_code_section(doc, "Yaseem", "metrics.c", read_file_safe(os.path.join(base_dir, "Week 5", "metrics.c")))
    add_code_section(doc, "Aditi Nayak", "main.c", read_file_safe(os.path.join(base_dir, "Week 5", "main.c")))
    add_code_section(doc, "Anas Ahmed", "gui.py", read_file_safe(os.path.join(base_dir, "Week 5", "gui.py")))
    
    # Save destinations
    dest1 = r"C:\pbl\Report_on_Project_Based_Learning.docx"
    dest2 = os.path.join(base_dir, "Report_on_Project_Based_Learning.docx")
    
    os.makedirs(r"C:\pbl", exist_ok=True)
    doc.save(dest1)
    print(f"Successfully generated and saved report at: {dest1}")
    
    doc.save(dest2)
    print(f"Successfully saved copy in repository at: {dest2}")

if __name__ == "__main__":
    build_document()
