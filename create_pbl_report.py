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
                    run.font.size = Pt(10)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(27, 54, 93)
    else:
        for cell in row.cells:
            if bg_color:
                set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(9.5)
                    run.font.color.rgb = RGBColor(45, 55, 72)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = RGBColor(27, 54, 93)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(44, 82, 130)
    return p

def add_body_p(doc, text, bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(30, 41, 59)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_question_box(doc, question_text, week_brief=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_q = p.add_run("Question")
    r_q.font.name = 'Calibri'
    r_q.font.size = Pt(10.5)
    r_q.font.bold = True
    r_q.font.color.rgb = RGBColor(27, 54, 93)
    
    p_q = doc.add_paragraph()
    p_q.paragraph_format.space_before = Pt(0)
    p_q.paragraph_format.space_after = Pt(3)
    p_q.paragraph_format.line_spacing = 1.15
    r_txt = p_q.add_run(question_text)
    r_txt.font.name = 'Calibri'
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = RGBColor(30, 41, 59)
    
    if week_brief:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.space_before = Pt(0)
        p_b.paragraph_format.space_after = Pt(6)
        r_b = p_b.add_run(f"({week_brief})")
        r_b.font.name = 'Calibri'
        r_b.font.size = Pt(9.5)
        r_b.font.italic = True
        r_b.font.color.rgb = RGBColor(100, 116, 139)

def add_member_commit_box(doc, member_name, commit_info=None, image_path=None):
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(6)
    p_name.paragraph_format.space_after = Pt(1)
    p_name.paragraph_format.keep_with_next = True
    r_name = p_name.add_run(member_name)
    r_name.font.name = 'Calibri'
    r_name.font.size = Pt(10.5)
    r_name.font.bold = True
    r_name.font.color.rgb = RGBColor(44, 82, 130)
    
    if commit_info:
        p_info = doc.add_paragraph()
        p_info.paragraph_format.space_before = Pt(0)
        p_info.paragraph_format.space_after = Pt(3)
        p_info.paragraph_format.keep_with_next = True
        r_info = p_info.add_run(commit_info)
        r_info.font.name = 'Consolas'
        r_info.font.size = Pt(8.5)
        r_info.font.color.rgb = RGBColor(71, 85, 105)
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "FFFFFF")
    set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    cp = cell.paragraphs[0]
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if image_path and os.path.exists(image_path):
        c_run = cp.add_run()
        c_run.add_picture(image_path, width=Inches(6.0))
    else:
        c_run = cp.add_run("[Insert screenshot of commits]")
        c_run.font.name = 'Calibri'
        c_run.font.size = Pt(9.5)
        c_run.font.italic = True
        c_run.font.color.rgb = RGBColor(100, 116, 139)
        
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_notes_box(doc, submitted_by, doc_title, notes_paragraphs, summary_table=None):
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.keep_with_next = True
    
    r_sub = p_sub.add_run(f"Submitted by: {submitted_by} ({doc_title})")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(10)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(27, 54, 93)
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    
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
    
    # First paragraph in cell
    p_first = cell.paragraphs[0]
    p_first.paragraph_format.space_before = Pt(0)
    p_first.paragraph_format.space_after = Pt(4)
    p_first.paragraph_format.line_spacing = 1.15
    
    for i, item in enumerate(notes_paragraphs):
        p_target = p_first if i == 0 else cell.add_paragraph()
        p_target.paragraph_format.space_before = Pt(0)
        p_target.paragraph_format.space_after = Pt(4)
        p_target.paragraph_format.line_spacing = 1.15
        
        # Check for bold headings or bullets
        if isinstance(item, tuple):
            prefix, text = item
            r_pre = p_target.add_run(prefix)
            r_pre.font.name = 'Calibri'
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(27, 54, 93)
            
            r_txt = p_target.add_run(text)
            r_txt.font.name = 'Calibri'
            r_txt.font.size = Pt(9.5)
            r_txt.font.color.rgb = RGBColor(45, 55, 72)
        elif item.startswith("•"):
            p_target.paragraph_format.left_indent = Inches(0.2)
            r_txt = p_target.add_run(item)
            r_txt.font.name = 'Calibri'
            r_txt.font.size = Pt(9.5)
            r_txt.font.color.rgb = RGBColor(45, 55, 72)
        else:
            r_txt = p_target.add_run(item)
            r_txt.font.name = 'Calibri'
            r_txt.font.size = Pt(9.5)
            if any(item.startswith(kw) for kw in ["Inter-Process Communication", "Pipes in IPC", "Shared Memory", "Sockets:", "Message Queues", "Definition:"]):
                r_txt.font.bold = True
                r_txt.font.color.rgb = RGBColor(27, 54, 93)
            else:
                r_txt.font.color.rgb = RGBColor(45, 55, 72)
                
    if summary_table:
        p_tbl_lbl = cell.add_paragraph()
        p_tbl_lbl.paragraph_format.space_before = Pt(6)
        p_tbl_lbl.paragraph_format.space_after = Pt(3)
        r_tbl_lbl = p_tbl_lbl.add_run("Summary Table:")
        r_tbl_lbl.font.name = 'Calibri'
        r_tbl_lbl.font.size = Pt(9.5)
        r_tbl_lbl.font.bold = True
        r_tbl_lbl.font.color.rgb = RGBColor(27, 54, 93)
        
        inner_table = cell.add_table(rows=len(summary_table), cols=2)
        set_table_borders(inner_table, color="D1D5DB")
        inner_widths = [Inches(1.8), Inches(4.3)]
        
        for r_idx, row_vals in enumerate(summary_table):
            row_obj = inner_table.rows[r_idx]
            for c_idx, val in enumerate(row_vals):
                row_obj.cells[c_idx].text = val
                row_obj.cells[c_idx].width = inner_widths[c_idx]
            if r_idx == 0:
                format_row(row_obj, is_header=True, bg_color="E2E8F0")
            else:
                format_row(row_obj, bg_color="FFFFFF" if r_idx % 2 == 1 else "F8FAFC")
                
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_code_section(doc, submitted_by, code_content=None, filename=None):
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(2)
    p_sub.paragraph_format.keep_with_next = True
    
    label = f"Submitted by: {submitted_by}"
    if filename:
        label += f" ({filename})"
    r_sub = p_sub.add_run(label)
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(10)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(27, 54, 93)
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    
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
    
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(0)
    cp.paragraph_format.line_spacing = 1.05
    
    if code_content:
        lines = code_content.strip().split('\n')
        if len(lines) > 220:
            lines = lines[:200] + [f"\n// ... [Remainder of file truncated for report conciseness. Full source in repository] ..."]
        formatted_code = '\n'.join(lines)
        c_run = cp.add_run(formatted_code)
        c_run.font.name = 'Consolas'
        c_run.font.size = Pt(8.5)
        c_run.font.color.rgb = RGBColor(30, 41, 59)
    else:
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_run = cp.add_run("[Paste code / code screenshot here]")
        c_run.font.name = 'Calibri'
        c_run.font.size = Pt(9.5)
        c_run.font.italic = True
        c_run.font.color.rgb = RGBColor(100, 116, 139)
        
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_outcomes_section(doc, outcomes_list):
    add_heading_2(doc, "Outcomes (Concepts Studied)")
    for item in outcomes_list:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.25)
        
        r_bullet = p.add_run("•  ")
        r_bullet.font.name = 'Calibri'
        r_bullet.font.size = Pt(10)
        r_bullet.font.bold = True
        r_bullet.font.color.rgb = RGBColor(44, 82, 130)
        
        r_text = p.add_run(item)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = RGBColor(45, 55, 72)
        
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(6)

def read_file_safe(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    return "// File not found in workspace."

def build_document():
    doc = docx.Document()
    
    # Page setup
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11.0)
        
        # Different first page for cover page
        sec.different_first_page_header_footer = True
        
        # Footer dynamic page number
        footer = sec.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ft.paragraph_format.space_before = Pt(8)
        p_ft.paragraph_format.space_after = Pt(0)
        
        r_ft = p_ft.add_run("Page ")
        r_ft.font.name = 'Calibri'
        r_ft.font.size = Pt(9.5)
        r_ft.font.color.rgb = RGBColor(100, 116, 139)
        
        fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
        p_ft._p.append(fld)
        
    base_dir = r"C:\Users\Aditi Nayak\.gemini\antigravity\scratch\zotify"
    pbl_dir = r"C:\pbl"
    cards_dir = os.path.join(pbl_dir, "commit_screenshots")
    logo_path = os.path.join(pbl_dir, "aloy logo.jpeg")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(base_dir, "aloy logo.jpeg")
    
    # ==========================================
    # 1. FIRST PAGE (COVER PAGE)
    # ==========================================
    p_cov_sp1 = doc.add_paragraph()
    p_cov_sp1.paragraph_format.space_before = Pt(20)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("REPORT ON PROJECT BASED LEARNING (PBL)")
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(27, 54, 93)
    
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.paragraph_format.space_after = Pt(10)
    r_date = p_date.add_run("NOVEMBER 5, 2026")
    r_date.font.name = 'Calibri'
    r_date.font.size = Pt(11)
    r_date.font.bold = True
    r_date.font.color.rgb = RGBColor(100, 116, 139)
    
    p_inst1 = doc.add_paragraph()
    p_inst1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst1.paragraph_format.space_after = Pt(2)
    r_inst1 = p_inst1.add_run("ST ALOYSIUS (DEEMED TO BE UNIVERSITY)")
    r_inst1.font.name = 'Calibri'
    r_inst1.font.size = Pt(12)
    r_inst1.font.bold = True
    r_inst1.font.color.rgb = RGBColor(45, 55, 72)
    
    p_inst2 = doc.add_paragraph()
    p_inst2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst2.paragraph_format.space_after = Pt(2)
    r_inst2 = p_inst2.add_run("SCHOOL OF ENGINEERING")
    r_inst2.font.name = 'Calibri'
    r_inst2.font.size = Pt(12)
    r_inst2.font.bold = True
    r_inst2.font.color.rgb = RGBColor(45, 55, 72)
    
    p_inst3 = doc.add_paragraph()
    p_inst3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst3.paragraph_format.space_after = Pt(12)
    r_inst3 = p_inst3.add_run("MANGALORE")
    r_inst3.font.name = 'Calibri'
    r_inst3.font.size = Pt(12)
    r_inst3.font.bold = True
    r_inst3.font.color.rgb = RGBColor(45, 55, 72)
    
    # College Logo Picture (Centered)
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(4)
    p_logo.paragraph_format.space_after = Pt(14)
    r_logo = p_logo.add_run()
    if os.path.exists(logo_path):
        r_logo.add_picture(logo_path, width=Inches(1.8))
    else:
        r_logo.add_text("[COLLEGE LOGO]")
        
    p_course_sp = doc.add_paragraph()
    p_course_sp.paragraph_format.space_before = Pt(12)
    p_course_sp.paragraph_format.space_after = Pt(2)
    
    p_course1 = doc.add_paragraph()
    p_course1.paragraph_format.space_after = Pt(2)
    rc1_lbl = p_course1.add_run("COURSE: ")
    rc1_lbl.font.name = 'Calibri'
    rc1_lbl.font.size = Pt(10.5)
    rc1_lbl.font.bold = True
    rc1_lbl.font.color.rgb = RGBColor(27, 54, 93)
    rc1_val = p_course1.add_run("Operating System and Computer Organization . Course code: 256PUE207")
    rc1_val.font.name = 'Calibri'
    rc1_val.font.size = Pt(10.5)
    rc1_val.font.color.rgb = RGBColor(51, 65, 85)
    
    p_course2 = doc.add_paragraph()
    p_course2.paragraph_format.space_after = Pt(8)
    p_course2.paragraph_format.left_indent = Inches(0.85)
    rc2_val = p_course2.add_run("Data Structures & Application Strategies. Course code: 256PUI219")
    rc2_val.font.name = 'Calibri'
    rc2_val.font.size = Pt(10.5)
    rc2_val.font.color.rgb = RGBColor(51, 65, 85)
    
    p_proj = doc.add_paragraph()
    p_proj.paragraph_format.space_after = Pt(12)
    r_p_lbl = p_proj.add_run("PROJECT TITLE:\t")
    r_p_lbl.font.name = 'Calibri'
    r_p_lbl.font.size = Pt(11)
    r_p_lbl.font.bold = True
    r_p_lbl.font.color.rgb = RGBColor(27, 54, 93)
    r_p_val = p_proj.add_run("OS Simulators: IPC, CPU Scheduling, Deadlock and Page Replacement")
    r_p_val.font.name = 'Calibri'
    r_p_val.font.size = Pt(11)
    r_p_val.font.color.rgb = RGBColor(51, 65, 85)
    
    p_sub_lbl = doc.add_paragraph()
    p_sub_lbl.paragraph_format.space_after = Pt(4)
    r_sub_lbl = p_sub_lbl.add_run("SUBMITTED BY")
    r_sub_lbl.font.name = 'Calibri'
    r_sub_lbl.font.size = Pt(11)
    r_sub_lbl.font.bold = True
    r_sub_lbl.font.color.rgb = RGBColor(27, 54, 93)
    
    # Submitted By Table with exact user registration numbers
    sub_table = doc.add_table(rows=5, cols=2)
    sub_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sub_table, color="CBD5E1")
    
    sub_headers = ["REGISTRATION NO.", "NAME"]
    sub_data = [
        ["25192102", "Aditi Nayak (Team Leader)"],
        ["25192105", "Anas Ahmed"],
        ["25192125", "Nireeksha"],
        ["25192101", "Yaseem"]
    ]
    
    col_widths = [Inches(2.5), Inches(3.5)]
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
    p_sup.paragraph_format.space_before = Pt(18)
    p_sup.paragraph_format.space_after = Pt(0)
    r_sup_lbl = p_sup.add_run("UNDER THE SUPERVISION OF:  ")
    r_sup_lbl.font.name = 'Calibri'
    r_sup_lbl.font.size = Pt(10.5)
    r_sup_lbl.font.bold = True
    r_sup_lbl.font.color.rgb = RGBColor(71, 85, 105)
    r_sup_val = p_sup.add_run("Mr Gaurav Prasad & Ms Priya George")
    r_sup_val.font.name = 'Calibri'
    r_sup_val.font.size = Pt(10.5)
    r_sup_val.font.color.rgb = RGBColor(51, 65, 85)
    
    doc.add_page_break()
    
    # ==========================================
    # 2. INDEX PAGE
    # ==========================================
    p_idx_h = doc.add_paragraph()
    p_idx_h.paragraph_format.space_before = Pt(12)
    p_idx_h.paragraph_format.space_after = Pt(8)
    r_idx_h = p_idx_h.add_run("INDEX")
    r_idx_h.font.name = 'Calibri'
    r_idx_h.font.size = Pt(16)
    r_idx_h.font.bold = True
    r_idx_h.font.color.rgb = RGBColor(27, 54, 93)
    
    idx_table = doc.add_table(rows=6, cols=5)
    idx_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(idx_table, color="CBD5E1")
    
    idx_headers = ["SL. NO.", "WEEK TITLE", "DATE", "REMARKS", "PAGE NO."]
    idx_data = [
        ["1", "Week 1: What is IPC and Its Techniques", "[30/09/2026]", "Completed", "3"],
        ["2", "Week 2: Multi-Process Simulator and IPC", "[07/10/2026]", "Completed", "7"],
        ["3", "Week 3: Process Scheduling (FCFS, SJF, Round Robin)", "[14/10/2026]", "Completed", "12"],
        ["4", "Week 4: Deadlock Avoidance (Banker's Algorithm)", "[21/10/2026]", "Completed", "17"],
        ["5", "Week 5: Page Replacement Algorithms", "[27/10/2026]", "Completed", "22"]
    ]
    
    idx_widths = [Inches(0.8), Inches(3.1), Inches(1.1), Inches(1.0), Inches(0.8)]
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
        row.cells[4].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    doc.add_page_break()
    
    # ==========================================
    # 3. WEEK 1: WHAT IS IPC AND ITS TECHNIQUES
    # ==========================================
    add_heading_1(doc, "Week 1: What is IPC and Its Techniques")
    add_body_p(doc, "[30/09/2026]", bold_prefix="Date: ")
    add_question_box(
        doc,
        "Implement two inter-process communication (IPC) techniques, a pipe and shared memory, and show how two processes exchange data using each of them.",
        week_brief="Week brief: the team splits up to gather information about IPC and its techniques, collects the explanations, and uploads a document of it to the GitHub repository."
    )
    
    add_heading_2(doc, "Team Members and GitHub Commit Screenshots")
    add_member_commit_box(
        doc,
        "Aditi Nayak (Team Leader)",
        commit_info="Commit: 80a92f2 | 2026-09-30 | 'Add files via upload'\nContribution: Week 1/aditi_zotify.docx (Pipes & Named Pipes IPC architecture and data streaming)",
        image_path=os.path.join(cards_dir, "w1_aditi.png")
    )
    add_member_commit_box(
        doc,
        "Anas Ahmed",
        commit_info="Commit: d8afdf2 | 2026-09-30 | 'Add files via upload'\nContribution: Week 1/INTERPROCESS COMMUNICATION.docx (Sockets IPC, network endpoints, and client-server model)",
        image_path=os.path.join(cards_dir, "w1_anas.png")
    )
    add_member_commit_box(
        doc,
        "Nireeksha",
        commit_info="Commit: 0f79efb | 2026-09-30 | 'Add files via upload'\nContribution: Week 1/IPCSharedMemory_PBL.docx (POSIX Shared Memory, shm_open, mmap, and semaphore synchronization)",
        image_path=os.path.join(cards_dir, "w1_nireeksha.png")
    )
    add_member_commit_box(
        doc,
        "Yaseem",
        commit_info="Commit: e06eeab | 2026-09-30 | 'Add files via upload'\nContribution: Week 1/IPC_PBL WEEK 1.docx (POSIX Message Queues, kernel buffering, and OS signal handling)",
        image_path=os.path.join(cards_dir, "w1_yaseem.png")
    )
    
    add_heading_2(doc, "How the Work Was Divided")
    w1_div_table = doc.add_table(rows=5, cols=2)
    w1_div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(w1_div_table, color="CBD5E1")
    
    w1_headers = ["Member / Part", "Responsibility"]
    w1_data = [
        ["Aditi Nayak (Team Leader)", "Pipes and named pipes (IPC)"],
        ["Anas Ahmed", "Sockets and client-server communication (IPC – Inter Process Communication)"],
        ["Nireeksha", "Shared memory and memory-mapped files (shm_open, mmap) & synchronization"],
        ["Yaseem", "Message queues and POSIX signals for asynchronous communication"]
    ]
    w1_col_widths = [Inches(2.5), Inches(4.0)]
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
        
    add_body_p(doc, "Each member studied and wrote notes on the IPC techniques they were assigned. The notes are documents kept in the repository's Week 1 directory.")
    
    # WEEK 1: NOTES & THEORY SUBMISSIONS (Instead of Code, as requested)
    add_heading_2(doc, "Notes and Theory Submissions (Uploaded to GitHub)")
    
    # 1. Aditi's Notes
    aditi_notes = [
        ("Name: ", "Aditi Nayak  |  Register Number: 25192102"),
        ("Inter-Process Communication (IPC): ", "Inter-Process Communication (IPC) is a mechanism that allows two or more processes to communicate and exchange data with each other."),
        ("Simple Example: ", "Suppose Process A calculates a student's marks and Process B calculates the grade. IPC allows Process A to send the marks to Process B."),
        ("Pipes in IPC: ", "A pipe is an IPC technique used to transfer data from one process to another. It works like a communication channel where one process writes data into the pipe and another process reads the data from it."),
        ("Data Flow: ", "Process A  →  Pipe  →  Process B"),
        ("Key Points:", ""),
        "• Usually used for communication between related processes.",
        "• Data flows through the pipe in a stream.",
        "• One process writes, while the other process reads.",
        "• Pipes are commonly used in operating systems.",
        ("Example in Practice: ", "A parent process sends a message like 'Hello' through a pipe, and the child process reads that message.")
    ]
    add_notes_box(doc, "Aditi Nayak (Team Leader)", "aditi_zotify.docx - Pipes in IPC", aditi_notes)
    
    # 2. Anas Ahmed's Notes
    anas_notes = [
        ("INTERPROCESS COMMUNICATION", ""),
        ("Definition: ", "Interprocess Communication (IPC) is a method that allows two or more processes to communicate with each other. It helps processes exchange data and work together by using communication methods provided by the operating system."),
        ("Technique of Interprocess Communication — Sockets:", ""),
        ("What are Sockets: ", "Sockets are used when two processes need to communicate with each other. They can be used between processes running on the same computer or between computers connected through a network."),
        ("How Sockets Work: ", "A socket acts as an endpoint through which one process can send and receive data from another process. In network communication, a socket is usually identified using an IP address and a port number."),
        ("Example: ", "In a client-server application, the client connects to the server using its IP address and port number. They can then exchange messages through the socket. After the communication is completed, the connection can be closed.")
    ]
    add_notes_box(doc, "Anas Ahmed", "INTERPROCESS COMMUNICATION.docx - Sockets in IPC", anas_notes)
    
    # 3. Nireeksha's Notes
    nireeksha_notes = [
        ("Inter-Process Communication (IPC) and Shared Memory", ""),
        ("Inter-Process Communication (IPC): ", "Inter-Process Communication (IPC) is a set of mechanisms that allows two or more processes to communicate and exchange data with each other. Since processes normally have separate memory spaces, IPC provides a way for them to share information and coordinate their activities. Common IPC methods include pipes, message queues, shared memory, and sockets."),
        ("Shared Memory: ", "Shared Memory is an IPC method in which two or more processes share a common memory area to exchange data. The operating system creates or maps a shared memory region that can be accessed by the participating processes."),
        ("Performance & Synchronization: ", "Because the data is placed in memory directly, shared memory is very fast and is suitable for exchanging large amounts of data. However, processes must use synchronization mechanisms such as semaphores or mutexes to prevent conflicts when accessing the shared data."),
        ("In Simple Terms: ", "Processes  →  Common Shared Memory  →  Exchange Data")
    ]
    add_notes_box(doc, "Nireeksha", "IPCSharedMemory_PBL.docx - Shared Memory in IPC", nireeksha_notes)
    
    # 4. Yaseem's Notes
    yaseem_notes = [
        ("Inter-Process Communication (IPC)", ""),
        ("1. Definition: ", "Inter-Process Communication (IPC) is a set of mechanisms provided by an operating system that allows two or more processes to communicate with each other and exchange data."),
        ("Purpose of IPC:", ""),
        "• To exchange information between processes.",
        "• To coordinate and synchronize the activities of processes.",
        "• To allow processes to work together to complete a task.",
        ("Common IPC Methods: ", "Message Queues, Pipes, Shared Memory, Sockets, Signals."),
        ("2. Message Queues:", ""),
        ("Definition: ", "A message queue is an IPC mechanism in which processes communicate by sending and receiving messages through a queue managed by the operating system."),
        ("How It Works:", ""),
        "• A sending process creates a message containing the required information.",
        "• The message is placed into a message queue.",
        "• The receiving process retrieves the message from the queue.",
        "• The processes do not need to directly share the same memory.",
        ("Example: ", "Process A wants to send data to Process B. Process A places the data as a message in the queue. Process B later reads the message from the queue and processes the data."),
        ("Advantages of Message Queues:", ""),
        "• Simple method for exchanging data between processes.",
        "• Processes can communicate without sharing memory directly.",
        "• Messages can be stored temporarily until the receiving process is ready.",
        "• Useful for communication between independent processes."
    ]
    yaseem_summary_table = [
        ["Topic", "Meaning"],
        ["IPC", "Allows processes to communicate and exchange data."],
        ["Message Queue", "Allows processes to communicate by sending and receiving messages through a queue."],
        ["Sender", "Process that places a message into the queue."],
        ["Receiver", "Process that retrieves and processes a message from the queue."]
    ]
    add_notes_box(doc, "Yaseem", "IPC_PBL WEEK 1.docx - Message Queues and Signals", yaseem_notes, summary_table=yaseem_summary_table)
    
    add_outcomes_section(doc, [
        "Why processes need IPC: separate address spaces cannot share data directly.",
        "Pipes and named pipes (FIFO) for one-way byte-stream communication.",
        "Shared memory and memory-mapped files for the fastest data exchange, and the need for synchronisation.",
        "Message queues and sockets for structured and networked/local communication.",
        "Trade-offs between the techniques: speed, complexity and synchronisation needs."
    ])
    
    doc.add_page_break()
    
    # ==========================================
    # 4. WEEK 2: MULTI-PROCESS SIMULATOR AND IPC
    # ==========================================
    add_heading_1(doc, "Week 2: Multi-Process Simulator and IPC")
    add_body_p(doc, "[07/10/2026]", bold_prefix="Date: ")
    add_question_box(
        doc,
        "Build a simple CPU simulator (accumulator, memory, stack and instruction queue) as three separate processes, a UI process, a Core process and a Logger process, that exchange data using IPC techniques.",
        week_brief="Tasks: separate the simulator into UI, Core and Logging processes; use threads where appropriate; select a suitable POSIX IPC mechanism and justify it; compare the standalone single-process simulator with the multi-process simulator; measure execution time, IPC overhead, CPU usage and memory usage."
    )
    
    add_heading_2(doc, "Team Members and GitHub Commit Screenshots")
    add_member_commit_box(
        doc,
        "Aditi Nayak (Team Leader)",
        commit_info="Commits: c9ff535, 425b308, 460dbc9 | 'Implement POSIX Pipes IPC, connect UI/Core/Logger processes'\nContribution: main.c, pipe_ipc.h, Makefile; pipe redirection, process orchestration",
        image_path=os.path.join(cards_dir, "w2_aditi.png")
    )
    add_member_commit_box(
        doc,
        "Anas Ahmed",
        commit_info="Commits: f19fbaa, 924dd63 | 'UI process for multi-process simulator'\nContribution: ui.c, ui.h; command prompt, assembly instruction parsing, serialized command pipe",
        image_path=os.path.join(cards_dir, "w2_anas.png")
    )
    add_member_commit_box(
        doc,
        "Nireeksha",
        commit_info="Commits: 6368e25, fa8a532 | 'Core process with memory, stack, and queue'\nContribution: core.c, core.h; Accumulator register, 1024-word memory, operand stack, instruction queue",
        image_path=os.path.join(cards_dir, "w2_nireeksha.png")
    )
    add_member_commit_box(
        doc,
        "Yaseem",
        commit_info="Commit: 0d67c13 | 'Implement logging process with POSIX pipe support'\nContribution: logger.c, logger.h; timestamped event auditing, console display, yaseem.log",
        image_path=os.path.join(cards_dir, "w2_yaseem.png")
    )
    
    add_heading_2(doc, "How the Work Was Divided")
    w2_div_table = doc.add_table(rows=5, cols=2)
    w2_div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(w2_div_table, color="CBD5E1")
    
    w2_headers = ["Member / Part", "Responsibility"]
    w2_data = [
        ["UI process – Anas Ahmed", "ui/ui.c; user interface, opcode validation, serialized command pipe to Core"],
        ["Core process – Nireeksha", "core/core.c; instruction queue, Accumulator register, 1024-word RAM, operand stack"],
        ["Logging process – Yaseem", "logger/logger.c; pipe + fork(), timestamping, stdout display, persistent yaseem.log"],
        ["Integration and testing – Aditi Nayak (Leader)", "main.c, pipe_ipc.h, Makefile; anonymous pipes, fork(), synchronization with waitpid()"]
    ]
    w2_col_widths = [Inches(2.5), Inches(4.0)]
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
        
    add_body_p(doc, "UI and Core talk over an anonymous POSIX pipe (ui_to_core_pipe). The UI process accepts assembly instructions (LOAD, STORE, ADD, SUB, PUSH, POP, JMP, HALT) and writes CPUCommand packets into the pipe. The Core process maintains CPU state, executes commands sequentially, and writes structured LogMessage packets through a second pipe (core_to_logger_pipe) to the Logger process. Aditi Nayak coordinated pipe redirection, fork() management, and clean termination handling.")
    
    add_heading_2(doc, "Code")
    add_code_section(doc, "Aditi Nayak", code_content=read_file_safe(os.path.join(base_dir, "Week 2", "pipe_ipc.h")), filename="pipe_ipc.h")
    add_code_section(doc, "Anas Ahmed", code_content=read_file_safe(os.path.join(base_dir, "Week 2", "ui.c")), filename="ui.c")
    add_code_section(doc, "Nireeksha", code_content=read_file_safe(os.path.join(base_dir, "Week 2", "core.c")), filename="core.c")
    add_code_section(doc, "Yaseem", code_content=read_file_safe(os.path.join(base_dir, "Week 2", "logger.c")), filename="logger.c")
    add_code_section(doc, "Aditi Nayak", code_content=read_file_safe(os.path.join(base_dir, "Week 2", "main.c")), filename="main.c")
    
    add_outcomes_section(doc, [
        "Designing a system as independent processes with defined interfaces.",
        "POSIX IPC: UNIX domain sockets, shared memory, pipes with fork(), and semaphores.",
        "Synchronisation of shared state using semaphores.",
        "Using threads inside processes where appropriate.",
        "Benchmarking standalone vs multi-process: execution time, IPC overhead, CPU usage and memory usage."
    ])
    
    doc.add_page_break()
    
    # ==========================================
    # 5. WEEK 3: PROCESS SCHEDULING
    # ==========================================
    add_heading_1(doc, "Week 3: Process Scheduling (FCFS, SJF, Round Robin)")
    add_body_p(doc, "[14/10/2026]", bold_prefix="Date: ")
    add_question_box(
        doc,
        "Implement CPU scheduling simulators for FCFS, non-preemptive SJF and Round Robin. For each algorithm, calculate the waiting time and turnaround time of every process and the average waiting time. (Our simulator also includes SRTF and Priority scheduling, and a Compare All option.)"
    )
    
    add_heading_2(doc, "Team Members and GitHub Commit Screenshots")
    add_member_commit_box(
        doc,
        "Aditi Nayak (Team Leader)",
        commit_info="Commit: 4f11690 | 'Integrate Week 3 Process Scheduling Simulator, add automated test suite'\nContribution: process.h, main.c, test_runner.c, Compare All benchmark orchestrator",
        image_path=os.path.join(cards_dir, "w3_aditi.png")
    )
    add_member_commit_box(
        doc,
        "Anas Ahmed",
        commit_info="Commit: 6222348 | 'Add FCFS and Round Robin scheduling implementation'\nContribution: input.c, fcfs.c, rr.c; input parsing, FIFO dispatching, time quantum preemption",
        image_path=os.path.join(cards_dir, "w3_anas.png")
    )
    add_member_commit_box(
        doc,
        "Nireeksha",
        commit_info="Commits: 6ee7a59, fd92e13, 37ac39f | 'Implement non-preemptive and preemptive SJF scheduling'\nContribution: sjf.c, gantt.c; SJF, SRTF, and visual Gantt chart execution timeline",
        image_path=os.path.join(cards_dir, "w3_nireeksha.png")
    )
    add_member_commit_box(
        doc,
        "Yaseem",
        commit_info="Commit: 73f9baf | 'Add priority scheduling algorithms in C'\nContribution: priority.c; preemptive and non-preemptive priority scheduling, comparative metrics",
        image_path=os.path.join(cards_dir, "w3_yaseem.png")
    )
    
    add_heading_2(doc, "How the Work Was Divided")
    w3_div_table = doc.add_table(rows=5, cols=2)
    w3_div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(w3_div_table, color="CBD5E1")
    
    w3_headers = ["Member / Part", "Responsibility"]
    w3_data = [
        ["Anas Ahmed", "FCFS and Round Robin (fcfs.c, rr.c, input.c)"],
        ["Nireeksha", "SJF and SRTF, Gantt chart display (sjf.c, gantt.c)"],
        ["Yaseem", "Priority scheduling, preemptive and non-preemptive, metrics (priority.c)"],
        ["Aditi Nayak (Leader)", "Main menu, input checks, process data structures, Compare All, integration (main.c, process.h, test_runner.c)"]
    ]
    w3_col_widths = [Inches(2.5), Inches(4.0)]
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
        
    add_body_p(doc, "Each member wrote the scheduling algorithms assigned above as separate modules, and the Team Leader integrated them through the main menu using shared data structures and automated test suites.")
    
    add_heading_2(doc, "Code")
    add_code_section(doc, "Aditi Nayak", code_content=read_file_safe(os.path.join(base_dir, "Week 3", "process.h")), filename="process.h")
    add_code_section(doc, "Anas Ahmed", code_content=read_file_safe(os.path.join(base_dir, "Week 3", "input.c")), filename="input.c")
    add_code_section(doc, "Anas Ahmed", code_content=read_file_safe(os.path.join(base_dir, "Week 3", "fcfs.c")), filename="fcfs.c")
    add_code_section(doc, "Nireeksha", code_content=read_file_safe(os.path.join(base_dir, "Week 3", "sjf.c")), filename="sjf.c")
    add_code_section(doc, "Yaseem", code_content=read_file_safe(os.path.join(base_dir, "Week 3", "priority.c")), filename="priority.c")
    add_code_section(doc, "Anas Ahmed", code_content=read_file_safe(os.path.join(base_dir, "Week 3", "rr.c")), filename="rr.c")
    add_code_section(doc, "Nireeksha", code_content=read_file_safe(os.path.join(base_dir, "Week 3", "gantt.c")), filename="gantt.c")
    add_code_section(doc, "Aditi Nayak", code_content=read_file_safe(os.path.join(base_dir, "Week 3", "main.c")), filename="main.c")
    
    add_outcomes_section(doc, [
        "Working of FCFS, SJF (non-preemptive and preemptive/SRTF), Priority and Round Robin scheduling.",
        "Computing waiting time, turnaround time, response time and CPU utilisation.",
        "Drawing and reading Gantt charts.",
        "Effect of the time quantum in Round Robin.",
        "Comparing algorithms on the same process set."
    ])
    
    doc.add_page_break()
    
    # ==========================================
    # 6. WEEK 4: DEADLOCK AVOIDANCE
    # ==========================================
    add_heading_1(doc, "Week 4: Deadlock Avoidance (Banker's Algorithm)")
    add_body_p(doc, "[21/10/2026]", bold_prefix="Date: ")
    add_question_box(
        doc,
        "Implement the Banker's algorithm to check whether a system is in a safe state, and print the safe sequence of processes if one exists.",
        week_brief="Week brief: design and implement an interactive Deadlock Simulation System with a proper GUI covering resource allocation, safe/unsafe states, deadlock detection, Banker's Algorithm, Resource Allocation Graph and deadlock recovery."
    )
    
    add_heading_2(doc, "Team Members and GitHub Commit Screenshots")
    add_member_commit_box(
        doc,
        "Aditi Nayak (Team Leader)",
        commit_info="Commit: d2d2ee1 | 'Complete deadlock simulator integration, GUI, test suites, and documentation'\nContribution: main.c, bankers.h, test_runner.c, CLI runner, backend integration",
        image_path=os.path.join(cards_dir, "w4_aditi.png")
    )
    add_member_commit_box(
        doc,
        "Anas Ahmed",
        commit_info="Commit: 21fe856 | 'Add Banker's Algorithm Simulator GUI'\nContribution: gui.py; Tkinter desktop UI, matrix input validation, RAG visualization",
        image_path=os.path.join(cards_dir, "w4_anas.png")
    )
    add_member_commit_box(
        doc,
        "Nireeksha",
        commit_info="Commit: 7e394f0 | 'Add Banker's Algorithm implementation'\nContribution: bankers.c, bankers.h; Safety algorithm, Need Matrix, Resource-Request checking",
        image_path=os.path.join(cards_dir, "w4_nireeksha.png")
    )
    add_member_commit_box(
        doc,
        "Yaseem",
        commit_info="Commit: b9a63ee | 'Deadlock Detection and Recovery#week4'\nContribution: deadlock.c, rag.c, recovery.c; cycle detection, RAG bipartite analysis, process abortion recovery",
        image_path=os.path.join(cards_dir, "w4_yaseem.png")
    )
    
    add_heading_2(doc, "How the Work Was Divided")
    w4_div_table = doc.add_table(rows=5, cols=2)
    w4_div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(w4_div_table, color="CBD5E1")
    
    w4_headers = ["Member / Part", "Responsibility"]
    w4_data = [
        ["Nireeksha", "Banker's Algorithm: safety algorithm and request check (bankers.c, bankers.h)"],
        ["Yaseem", "Deadlock detection, resource management and recovery (deadlock.c, rag.c, recovery.c)"],
        ["Anas Ahmed", "Tkinter window and Resource Allocation Graph visualization (gui.py)"],
        ["Aditi Nayak (Leader)", "Main program, CLI runner, test suites, dual-mode bridge, documentation (main.c, test_runner.c, test_deadlock.py)"]
    ]
    w4_col_widths = [Inches(2.5), Inches(4.0)]
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
        
    add_body_p(doc, "In the simulator, the Banker's Algorithm runs as a high-performance C engine. The Tkinter GUI and the C backend communicate seamlessly, allowing users to inspect Allocation, Max, Available, and Need matrices, detect deadlock cycles in the Resource Allocation Graph, and trigger automated recovery via process abortion.")
    
    add_heading_2(doc, "Code")
    add_code_section(doc, "Aditi Nayak", code_content=read_file_safe(os.path.join(base_dir, "Week 4", "bankers.h")), filename="bankers.h")
    add_code_section(doc, "Nireeksha", code_content=read_file_safe(os.path.join(base_dir, "Week 4", "bankers.c")), filename="bankers.c")
    add_code_section(doc, "Yaseem", code_content=read_file_safe(os.path.join(base_dir, "Week 4", "deadlock.c")), filename="deadlock.c")
    add_code_section(doc, "Yaseem", code_content=read_file_safe(os.path.join(base_dir, "Week 4", "rag.c")), filename="rag.c")
    add_code_section(doc, "Yaseem", code_content=read_file_safe(os.path.join(base_dir, "Week 4", "recovery.c")), filename="recovery.c")
    add_code_section(doc, "Aditi Nayak", code_content=read_file_safe(os.path.join(base_dir, "Week 4", "main.c")), filename="main.c")
    add_code_section(doc, "Anas Ahmed", code_content=read_file_safe(os.path.join(base_dir, "Week 4", "gui.py")), filename="gui.py")
    
    add_outcomes_section(doc, [
        "The four necessary conditions for deadlock.",
        "Allocation, Maximum, Need matrices and the Available vector.",
        "Safe and unsafe states and the Banker's safety algorithm.",
        "Deadlock detection, Resource Allocation Graph and recovery.",
        "Named pipes (FIFO) / IPC between a GUI frontend and a C worker process."
    ])
    
    doc.add_page_break()
    
    # ==========================================
    # 7. WEEK 5: PAGE REPLACEMENT ALGORITHMS
    # ==========================================
    add_heading_1(doc, "Week 5: Page Replacement Algorithms")
    add_body_p(doc, "[27/10/2026]", bold_prefix="Date: ")
    add_question_box(
        doc,
        "Simulation and Comparative Analysis of Page Replacement Algorithms: design and implement a program that accepts a page-reference string and the number of page frames, simulates FIFO, LRU and Optimal replacement, displays the frame contents after each request, identifies page hits and faults, and compares the total page faults of each algorithm."
    )
    
    add_heading_2(doc, "Team Members and GitHub Commit Screenshots")
    add_member_commit_box(
        doc,
        "Aditi Nayak (Team Leader)",
        commit_info="Commit: 9ac3968 | 'Complete page replacement algorithms integration and testing'\nContribution: main.c, page_replacement.h, test_runner.c, Compare All benchmarking orchestrator",
        image_path=os.path.join(cards_dir, "w5_aditi.png")
    )
    add_member_commit_box(
        doc,
        "Anas Ahmed",
        commit_info="Commit: 6232070 | 'Add GUI for Page Replacement Algorithm Simulation'\nContribution: gui.py; animated Tkinter visual memory frame grid, hit/fault badges, comparative charts",
        image_path=os.path.join(cards_dir, "w5_anas.png")
    )
    add_member_commit_box(
        doc,
        "Nireeksha",
        commit_info="Commit: ac8f3c5 | 'Implement FIFO and LRU page replacement algorithms'\nContribution: fifo.c, lru.c; arrival queue tracking, timestamp-based recency eviction",
        image_path=os.path.join(cards_dir, "w5_nireeksha.png")
    )
    add_member_commit_box(
        doc,
        "Yaseem",
        commit_info="Commit: b9a63ee | 'Optimal algorithm and performance metrics'\nContribution: optimal.c, metrics.c; forward lookahead victim selection, hit/fault ratio calculators",
        image_path=os.path.join(cards_dir, "w5_yaseem.png")
    )
    
    add_heading_2(doc, "How the Work Was Divided")
    w5_div_table = doc.add_table(rows=5, cols=2)
    w5_div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(w5_div_table, color="CBD5E1")
    
    w5_headers = ["Member / Part", "Responsibility"]
    w5_data = [
        ["Nireeksha", "FIFO and LRU page replacement algorithms (fifo.c, lru.c)"],
        ["Yaseem", "Optimal page replacement algorithm, performance metrics (optimal.c, metrics.c)"],
        ["Anas Ahmed", "Tkinter desktop GUI and step-by-step memory frame grid visualization (gui.py)"],
        ["Aditi Nayak (Leader)", "Main CLI driver, shared data structures, Compare All option, test harness (main.c, page_replacement.h, test_runner.c)"]
    ]
    w5_col_widths = [Inches(2.5), Inches(4.0)]
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
        
    add_body_p(doc, "Each member implemented their assigned replacement algorithms and metric utilities in modular C source files adhering to page_replacement.h. Anas created an interactive Tkinter GUI for visual step-by-step tracing, and Aditi Nayak integrated all components into the unified CLI engine and automated test harness.")
    
    add_heading_2(doc, "Code")
    add_code_section(doc, "Aditi Nayak", code_content=read_file_safe(os.path.join(base_dir, "Week 5", "page_replacement.h")), filename="page_replacement.h")
    add_code_section(doc, "Nireeksha", code_content=read_file_safe(os.path.join(base_dir, "Week 5", "fifo.c")), filename="fifo.c")
    add_code_section(doc, "Nireeksha", code_content=read_file_safe(os.path.join(base_dir, "Week 5", "lru.c")), filename="lru.c")
    add_code_section(doc, "Yaseem", code_content=read_file_safe(os.path.join(base_dir, "Week 5", "optimal.c")), filename="optimal.c")
    add_code_section(doc, "Yaseem", code_content=read_file_safe(os.path.join(base_dir, "Week 5", "metrics.c")), filename="metrics.c")
    add_code_section(doc, "Aditi Nayak", code_content=read_file_safe(os.path.join(base_dir, "Week 5", "main.c")), filename="main.c")
    add_code_section(doc, "Anas Ahmed", code_content=read_file_safe(os.path.join(base_dir, "Week 5", "gui.py")), filename="gui.py")
    
    add_outcomes_section(doc, [
        "Virtual memory, paging and page faults.",
        "FIFO, LRU and Optimal page replacement algorithms.",
        "Distinguishing page hits from page faults and computing hit/fault ratios.",
        "Comparing algorithms on identical reference strings and frame counts.",
        "Handling invalid input and edge cases (empty string, non-positive frame count)."
    ])
    
    # Save locations
    dest_complete = r"C:\pbl\Report_on_Project_Based_Learning_Complete.docx"
    dest_final = r"C:\pbl\Report_on_Project_Based_Learning_Final.docx"
    dest_upd = r"C:\pbl\Report_on_Project_Based_Learning_Updated.docx"
    dest_orig = r"C:\pbl\Report_on_Project_Based_Learning.docx"
    dest_repo = os.path.join(base_dir, "Report_on_Project_Based_Learning.docx")
    
    os.makedirs(r"C:\pbl", exist_ok=True)
    doc.save(dest_complete)
    print(f"Successfully generated and saved complete report at: {dest_complete}")

    for target in [dest_final, dest_upd, dest_orig]:
        try:
            doc.save(target)
            print(f"Successfully updated: {target}")
        except PermissionError:
            print(f"[Note] {target} is currently open in Word. Skipped overwriting locked file.")
    
    doc.save(dest_repo)
    print(f"Successfully saved copy in repository at: {dest_repo}")

if __name__ == "__main__":
    build_document()
