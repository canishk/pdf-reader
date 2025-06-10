from pypdf import PdfReader

reader = PdfReader("Brand Summary.pdf")

def find_bookmark_page(bookmarks, target_title:str) -> int | None:
    for item in bookmarks:
        if isinstance(item, list):
            result = find_bookmark_page(item, target_title)
            if result:
                return result
        elif target_title.lower() in item.title.lower():
            return reader.get_destination_page_number(item)
    return None

def extract_text_from_page(reader: PdfReader, page_number: int) -> str:
    if 0 <= page_number < len(reader.pages):
        page = reader.pages[page_number]
        return page.extract_text() or ""
    return ""

bookmark_title = "Store Summary"
page_number = find_bookmark_page(reader.outline, bookmark_title)
if page_number is not None:
    print(f"The bookmark '{bookmark_title}' is on page {page_number + 1}.")
    text = extract_text_from_page(reader, page_number)
    print(f"Text from page {page_number + 1}:\n{text}")
else:
    print(f"The bookmark '{bookmark_title}' was not found.")
