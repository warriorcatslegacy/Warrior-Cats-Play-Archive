from bs4 import BeautifulSoup
import os

# === CONFIGURATION ===
INPUT_FILE = r"D:\wcp_archives\rawhtml\thunderclan_camp_2021.html"  # ← update this to your actual file
OUTPUT_DIR = r"D:\wcp_archives\output_pages"              # ← output folder
MESSAGES_PER_PAGE = 50                                    # ← messages per split page

# === Ensure Output Directory Exists ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Load HTML ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

head_html = str(soup.head)
message_groups = soup.select(".chatlog__message-group")
total_pages = (len(message_groups) + MESSAGES_PER_PAGE - 1) // MESSAGES_PER_PAGE

# === Page Generation ===
for page_num in range(total_pages):
    start = page_num * MESSAGES_PER_PAGE
    end = start + MESSAGES_PER_PAGE
    page_messages = message_groups[start:end]

    # === Generate Message HTML ===
    body_content = '<div class="chatlog">\n' + '\n'.join(str(m) for m in page_messages) + '\n</div>'

    # === Navigation HTML ===
    nav_html = '<div style="text-align:center; margin: 2em;">\n'

    # First & Prev
    if page_num > 0:
        nav_html += f'<a href="page1.html">« First</a> '
        nav_html += f'<a href="page{page_num}.html">‹ Prev</a> '

    # Jump -3
    if page_num >= 3:
        nav_html += f'<a href="page{page_num - 2}.html">« -3</a> '

    # Current page
    nav_html += f'<strong>Page {page_num + 1} of {total_pages}</strong> '

    # Jump +3
    if page_num + 3 < total_pages:
        nav_html += f'<a href="page{page_num + 4}.html">+3 »</a> '

    # Next & Last
    if page_num < total_pages - 1:
        nav_html += f'<a href="page{page_num + 2}.html">Next ›</a> '
        nav_html += f'<a href="page{total_pages}.html">Last »</a> '

    nav_html += '\n</div>'

    # === Final HTML Output ===
    final_html = (
        '<!DOCTYPE html>\n<html lang="en">\n' +
        head_html +
        '\n<body>\n' +
        body_content +
        '\n' + nav_html +
        '\n</body>\n</html>'
    )

    output_filename = os.path.join(OUTPUT_DIR, f"page{page_num + 1}.html")
    with open(output_filename, "w", encoding="utf-8") as out:
        out.write(final_html)

print(f"✅ Done! Split {len(message_groups)} messages into {total_pages} pages.")
print(f"📂 Output saved to: {OUTPUT_DIR}")
