# import json
# import os

# LIBRARY_FILE = "library.txt"

# # Load the library from file
# def load_library():
#     if os.path.exists(LIBRARY_FILE):
#         with open(LIBRARY_FILE, "r") as file:
#             return json.load(file)
#     return []

# # Save the library to file
# def save_library(library):
#     with open(LIBRARY_FILE, "w") as file:
#         json.dump(library, file)

# # Add a book
# def add_book(library):
#     title = input("Enter the book title: ").strip()
#     author = input("Enter the author: ").strip()
#     year = int(input("Enter the publication year: ").strip())
#     genre = input("Enter the genre: ").strip()
#     read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

#     library.append({
#         "title": title,
#         "author": author,
#         "year": year,
#         "genre": genre,
#         "read": read_status
#     })
#     print("Book added successfully!")

# # Remove a book
# def remove_book(library):
#     title = input("Enter the title of the book to remove: ").strip()
#     for book in library:
#         if book["title"].lower() == title.lower():
#             library.remove(book)
#             print("Book removed successfully!")
#             return
#     print("Book not found.")

# # Search for a book
# def search_book(library):
#     print("Search by:\n1. Title\n2. Author")
#     choice = input("Enter your choice: ").strip()
#     keyword = input("Enter the search term: ").strip().lower()

#     matches = [book for book in library if keyword in book["title"].lower() or keyword in book["author"].lower()]
    
#     if matches:
#         for i, book in enumerate(matches, 1):
#             status = "Read" if book["read"] else "Unread"
#             print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
#     else:
#         print("No matching books found.")

# # Display all books
# def display_books(library):
#     if not library:
#         print("Your library is empty.")
#         return
    
#     for i, book in enumerate(library, 1):
#         status = "Read" if book["read"] else "Unread"
#         print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

# # Display statistics
# def display_statistics(library):
#     total_books = len(library)
#     if total_books == 0:
#         print("No books in the library.")
#         return

#     read_books = sum(1 for book in library if book["read"])
#     percentage_read = (read_books / total_books) * 100

#     print(f"Total books: {total_books}")
#     print(f"Percentage read: {percentage_read:.2f}%")

# # Main menu
# def main():
#     library = load_library()

#     while True:
#         print("\nWelcome to your Personal Library Manager!")
#         print("1. Add a book")
#         print("2. Remove a book")
#         print("3. Search for a book")
#         print("4. Display all books")
#         print("5. Display statistics")
#         print("6. Exit")
        
#         choice = input("Enter your choice: ").strip()

#         if choice == "1":
#             add_book(library)
#         elif choice == "2":
#             remove_book(library) 
#         elif choice == "3":
#             search_book(library)
#         elif choice == "4":
#             display_books(library)
#         elif choice == "5":
#             display_statistics(library)
#         elif choice == "6":
#             save_library(library)
#             print("Library saved to file. Goodbye!")
#             break
#         else:
#             print("Invalid choice, please try again.")

# if __name__ == "__main__":
#     main()


import streamlit as st
import json
import os

LIBRARY_FILE = "library.json"

# Load library data
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library data
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
library = load_library()

# Streamlit UI
st.title("📔🔖 Personal Library Manager")

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Statistics"])

# Add a book
if menu == "Add a Book":
    st.subheader("📖 Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        if title and author and year and genre:
            library.append({
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read": read_status
            })
            save_library(library)
            st.success("Book added successfully! ✅")
        else:
            st.error("Please fill all fields!")

# Remove a book
elif menu == "Remove a Book":
    st.subheader("🗑️ Remove a Book")
    book_titles = [book["title"] for book in library]
    
    if book_titles:
        book_to_remove = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f"'{book_to_remove}' removed successfully! ✅")
    else:
        st.warning("No books available to remove.")

# Search for a book
elif menu == "Search for a Book":
    st.subheader("🔎 Search for a Book")
    search_query = st.text_input("Enter book title or author")
    
    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            for book in results:
                st.write(f"📘 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching books found.")

# Display all books
elif menu == "Display All Books":
    st.subheader("📚 Your Library")
    
    if library:
        for book in library:
            st.write(f"📘 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.warning("No books in the library.")

# Display statistics
elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    
    if total_books > 0:
        st.write(f"📚 **Total books:** {total_books}")
        st.write(f"✅ **Books read:** {read_books} ({(read_books/total_books)*100:.2f}%)")
    else:
        st.warning("No books in the library.")


