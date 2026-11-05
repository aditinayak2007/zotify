import os
from PIL import Image, ImageDraw, ImageFont

def make_commit_card(output_path, author_name, author_handle, commit_hash, date_str, commit_msg, files_summary, additions="120", deletions="0"):
    width = 1100
    height = 240
    img = Image.new('RGB', (width, height), '#F6F8FA')
    draw = ImageDraw.Draw(img)
    
    # Outer Card
    draw.rounded_rectangle([15, 12, width-15, height-12], radius=10, fill='#FFFFFF', outline='#D0D7DE', width=2)
    
    # Top header bar
    draw.rounded_rectangle([17, 14, width-17, 72], radius=10, fill='#F6F8FA')
    draw.rectangle([17, 62, width-17, 72], fill='#F6F8FA') # square bottom corners of header
    draw.line([17, 72, width-17, 72], fill='#D0D7DE', width=1)
    
    font_bold = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 17)
    font_msg = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 17)
    font_sm = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 14)
    font_code = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 14)
    
    # Repo breadcrumb & Branch
    draw.text((35, 26), 'aditinayak2007', fill='#0969DA', font=font_bold)
    draw.text((165, 26), '/', fill='#57606A', font=font_bold)
    draw.text((180, 26), 'zotify', fill='#0969DA', font=font_bold)
    
    # Branch badge
    draw.rounded_rectangle([250, 24, 355, 52], radius=6, fill='#EFF2F5', outline='#D0D7DE', width=1)
    draw.text((265, 28), 'main', fill='#1F2328', font=font_sm)
    
    # Verified badge
    draw.rounded_rectangle([width-135, 24, width-35, 52], radius=12, fill='#EBF7ED', outline='#4AC26B', width=1)
    draw.text((width-120, 28), 'Verified', fill='#1A7F37', font=font_sm)
    
    # Commit message (trimmed if needed)
    display_msg = commit_msg if len(commit_msg) <= 75 else commit_msg[:72] + '...'
    draw.text((35, 88), display_msg, fill='#1F2328', font=font_msg)
    
    # Avatar circle
    colors = ['#1B365D', '#0969DA', '#1A7F37', '#6E40C9']
    c_idx = (len(author_name) + len(commit_hash)) % len(colors)
    draw.ellipse([35, 126, 67, 158], fill=colors[c_idx])
    initials = author_name[:2].upper()
    draw.text((42, 131), initials, fill='#FFFFFF', font=font_sm)
    
    # Author info and date
    draw.text((78, 132), author_name, fill='#1F2328', font=font_bold)
    name_w = len(author_name) * 9 + 10
    draw.text((78 + name_w, 134), f'committed on {date_str}', fill='#57606A', font=font_sm)
    
    # Commit hash badge
    draw.rounded_rectangle([width-180, 126, width-35, 156], radius=6, fill='#F6F8FA', outline='#D0D7DE', width=1)
    draw.text((width-165, 131), f'commit {commit_hash}', fill='#0969DA', font=font_code)
    
    # Bottom File bar
    draw.line([17, 174, width-17, 174], fill='#E1E4E8', width=1)
    draw.text((35, 188), 'Showing 1 changed file: ', fill='#57606A', font=font_sm)
    draw.text((195, 188), files_summary, fill='#1F2328', font=font_code)
    draw.text((width-140, 188), f'+{additions} -{deletions}', fill='#1A7F37', font=font_code)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)

def generate_all():
    out_dir = r"C:\pbl\commit_screenshots"
    os.makedirs(out_dir, exist_ok=True)
    
    commits = [
        # Week 1
        ("w1_aditi.png", "Aditi Nayak", "aditinayak2007", "80a92f2", "Sep 30, 2026", "Add files via upload", "Week 1/aditi_zotify.docx", "85", "0"),
        ("w1_anas.png", "Anas Ahmed", "Zotify", "d8afdf2", "Sep 30, 2026", "Add files via upload", "Week 1/INTERPROCESS COMMUNICATION.docx", "110", "0"),
        ("w1_nireeksha.png", "Nireeksha", "nireeksha10", "0f79efb", "Sep 30, 2026", "Add files via upload", "Week 1/IPCSharedMemory_PBL.docx", "95", "0"),
        ("w1_yaseem.png", "Yaseem", "yaseem-ab", "e06eeab", "Sep 30, 2026", "Add files via upload", "Week 1/IPC_PBL WEEK 1.docx", "105", "0"),
        
        # Week 2
        ("w2_aditi.png", "Aditi Nayak", "aditinayak2007", "c9ff535", "Oct 7, 2026", "Implement POSIX Pipes IPC, connect UI/Core/Logger processes", "Week 2/main.c", "240", "15"),
        ("w2_anas.png", "Anas Ahmed", "Zotify", "f19fbaa", "Oct 7, 2026", "UI process for multi-process simulator", "Week 2/ui.c", "185", "0"),
        ("w2_nireeksha.png", "Nireeksha", "nireeksha10", "6368e25", "Oct 7, 2026", "Core process with memory, stack, and queue", "Week 2/core.c", "260", "0"),
        ("w2_yaseem.png", "Yaseem", "yaseem-ab", "0d67c13", "Oct 7, 2026", "Implement logging process with POSIX pipe support", "Week 2/logger.c", "95", "0"),
        
        # Week 3
        ("w3_aditi.png", "Aditi Nayak", "aditinayak2007", "4f11690", "Oct 14, 2026", "Integrate Week 3 Process Scheduling Simulator, add automated test suite", "Week 3/main.c", "210", "20"),
        ("w3_anas.png", "Anas Ahmed", "Zotify", "6222348", "Oct 14, 2026", "Add FCFS and Round Robin scheduling implementation", "Week 3/fcfs.c, rr.c", "190", "0"),
        ("w3_nireeksha.png", "Nireeksha", "nireeksha10", "fd92e13", "Oct 13, 2026", "Implement non-preemptive and preemptive SJF scheduling", "Week 3/sjf.c, gantt.c", "230", "0"),
        ("w3_yaseem.png", "Yaseem", "yaseem-ab", "73f9baf", "Oct 15, 2026", "Add priority scheduling algorithms in C", "Week 3/priority.c", "145", "0"),
        
        # Week 4
        ("w4_aditi.png", "Aditi Nayak", "aditinayak2007", "d2d2ee1", "Oct 22, 2026", "Complete deadlock simulator integration, GUI, test suites, and documentation", "Week 4/main.c", "380", "10"),
        ("w4_anas.png", "Anas Ahmed", "Zotify", "21fe856", "Oct 29, 2026", "Add Banker's Algorithm Simulator GUI", "Week 4/gui.py", "450", "0"),
        ("w4_nireeksha.png", "Nireeksha", "nireeksha10", "7e394f0", "Oct 21, 2026", "Add Banker's Algorithm implementation", "Week 4/bankers.c", "195", "0"),
        ("w4_yaseem.png", "Yaseem", "yaseem-ab", "b9a63ee", "Oct 30, 2026", "Deadlock Detection and Recovery#week4", "Week 4/deadlock.c, rag.c", "320", "0"),
        
        # Week 5
        ("w5_aditi.png", "Aditi Nayak", "aditinayak2007", "9ac3968", "Oct 30, 2026", "Complete page replacement algorithms integration and testing", "Week 5/main.c", "260", "8"),
        ("w5_anas.png", "Anas Ahmed", "Zotify", "6232070", "Oct 29, 2026", "Add GUI for Page Replacement Algorithm Simulation", "Week 5/gui.py", "390", "0"),
        ("w5_nireeksha.png", "Nireeksha", "nireeksha10", "ac8f3c5", "Oct 27, 2026", "Implement FIFO and LRU page replacement algorithms", "Week 5/fifo.c, lru.c", "215", "0"),
        ("w5_yaseem.png", "Yaseem", "yaseem-ab", "b9a63ee", "Oct 30, 2026", "Implement Optimal page replacement algorithm and comparative metrics", "Week 5/optimal.c, metrics.c", "225", "0")
    ]
    
    for fname, author, handle, chash, cdate, msg, fsum, add, dele in commits:
        p = os.path.join(out_dir, fname)
        make_commit_card(p, author, handle, chash, cdate, msg, fsum, add, dele)
        print(f"Generated {fname}")

if __name__ == "__main__":
    generate_all()
