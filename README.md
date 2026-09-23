Akash Admin Panel Image Upload Automation

Documentation (Python + Playwright + Microsoft Edge)

# Objective

Automate Image Links upload, filename extraction and CDN URL generation.

# Prerequisites

Windows, Python 3.13+, Microsoft Edge, Playwright.

# Folder Structure

Files: login.py, uploader.py, state.json, output.txt and KV image folder.

# Login Process

Run login.py once, login manually, save session to state.json.

# Workflow

Read images, upload, save, find latest filename, generate CDN URL, write output.txt.

# Pagination Handling

Determine last page dynamically using total record count. No hardcoded page numbers.

# Filename Extraction

Read filename from data-values attribute in Image Links table.

# URL Generation

Prefix filename with <http://cdnhost.akashbd.net/assets/uploads/pack_cate/>

# Output

Generated URLs are saved to output.txt.

# Benefits

Eliminates manual upload tracking and URL creation.

**End-to-End Flow:  
**Images in KV -> uploader.py -> Upload -> Save -> Extract Filename -> Build URL -> output.txt
