const MY_SERVER = 'https://library-project-test1.onrender.com/';
// const MY_SERVER = 'http://127.0.0.1:5000/';

// Function to get books (with optional search term)
async function getBooks(searchTerm = '') {
    try {
        const response = await axios.get(MY_SERVER + '/books', {
            params: {
                title: searchTerm, // Pass the search term as a parameter
            },
        });
        const books = response.data;
        const tableBody = document.getElementById('book-table-body');
        tableBody.innerHTML = ''; // Clear the table body

        books.forEach(book => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.copies_available}</td>
                <td>${book.loan_duration_type}</td>
                <td>
                    <button class="btn btn-danger delete-book" data-id="${book.id}">Delete</button>
                    <button class="btn btn-info update-book" data-id="${book.id}">Update</button>
                    <button class="btn btn-info loan-book-button" data-id="${book.id}" data-loan="${book.loan_duration_type}" onclick="loanBook('${book.id}', '${book.loan_duration_type}')">Loan</button>
                    <button class="btn btn-info return-book-button" data-id="${book.id}">Return</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
        // Handle the error and provide user feedback
    }
}

// Function to filter books by name
function filterBooksByTitle(books, searchTerm) {
    return books.filter(book => book.title.toLowerCase().includes(searchTerm.toLowerCase()));
}

// Function to update the book table with filtered data
function updateBookTable(books) {
    const tableBody = document.getElementById('book-table-body');
    tableBody.innerHTML = ''; // Clear the table body
    books.forEach(book => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${book.id}</td>
            <td>${book.title}</td>
            <td>${book.author}</td>
            <td>${book.copies_available}</td>
            <td>${book.loan_duration_type}</td>
            <td>
                <button class="btn btn-danger delete-book" data-id="${book.id}">Delete</button>
                <button class="btn btn-info update-book" data-id="${book.id}">Update</button>
                <button class="btn btn-info loan-book-button" data-id="${book.id}" data-loan="${book.loan_duration_type}" onclick="loanBook('${book.id}', '${book.loan_duration_type}')">Loan</button>
                <button class="btn btn-info return-book-button" data-id="${book.id}" onclick="loanBook('${book.id}', '${book.loan_duration_type}')">Return</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Event listener for the search input
document.getElementById('book-search-input').addEventListener('input', handleSearchInput);

function handleSearchInput() {
    const searchInput = document.getElementById('book-search-input');
    const searchTerm = searchInput.value.trim();
    const filteredBooks = filterBooksByTitle(bookData, searchTerm);
    updateBookTable(filteredBooks); // Update the table with filtered results
}

let bookData = []
async function init() {
    try {
        const response = await axios.get(MY_SERVER + '/books');
        bookData = response.data; // Populate bookData with initial data
        updateBookTable(bookData);
    } catch (error) {
        console.error(error);
        // Handle the error and provide user feedback
    }
}
init();

async function addBook(title, author, copiesAvailable, loanDurationType) {
    const bookData = {
        title: title,
        author: author,
        copies_available: copiesAvailable,
        loan_duration_type: loanDurationType,
    };

    try {
        const response = await axios.post(`${MY_SERVER}/books/add`, bookData, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.data.message === 'Book added successfully') {
            alert('Book added successfully');
            getBooks(); // Refresh the book list
        } else {
            alert('Error adding book: ' + response.data.message);
        }
    } catch (error) {
        console.error('Error adding book:', error);
    }
}

// Event listener for the "Add Book" form submission
document.getElementById('add_book_form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form submission and page reload

    const titleInput = document.getElementById('title');
    const authorInput = document.getElementById('author');
    const copiesAvailableInput = document.getElementById('copies_available');
    const loanDurationTypeInput = document.getElementById('loan_duration_type');

    const title = titleInput.value;
    const author = authorInput.value;
    const copiesAvailable = copiesAvailableInput.value;
    const loanDurationType = loanDurationTypeInput.value;

    if (title && author && copiesAvailable && loanDurationType) {
        addBook(title, author, copiesAvailable, loanDurationType);
        // Optionally, clear the form fields after adding the book
        titleInput.value = '';
        authorInput.value = '';
        copiesAvailableInput.value = '';
        loanDurationTypeInput.value = '';
    } else {
        alert('Please fill in all the fields.');
    }
});


// Event delegation to handle various book actions
document.getElementById('book-table-body').addEventListener('click', (event) => {
    const target = event.target;
    const bookId = target.getAttribute('data-id');
    const bookLoanType = target.getAttribute('data-loan');

    if (target.classList.contains('loan-book-button')) {
        loanBook(bookId, bookLoanType);
    } else if (target.classList.contains('return-book-button')) {
        returnBook(bookId);
    } else if (target.classList.contains('delete-book')) {
        deleteBook(bookId);
    } else if (target.classList.contains('update-book')) {
        const row = target.parentElement.parentElement;
        if (!row.querySelector('.update-form')) {
            const updateForm = document.createElement('div');
            updateForm.className = 'update-form';

            const titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.placeholder = 'New Title';

            const authorInput = document.createElement('input');
            authorInput.type = 'text';
            authorInput.placeholder = 'New Author';

            const copiesAvailableInput = document.createElement('input');
            copiesAvailableInput.type = 'number';
            copiesAvailableInput.placeholder = 'New Available Copies';

            const durationTypeInput = document.createElement('input');
            durationTypeInput.type = 'number';
            durationTypeInput.placeholder = 'New Duration Type';

            const updateButton = document.createElement('button');
            updateButton.textContent = 'Submit';
            updateButton.addEventListener('click', async () => {
                const newTitle = titleInput.value;
                const newAuthor = authorInput.value;
                const newCopiesAvailable = copiesAvailableInput.value;
                const newDurationType = durationTypeInput.value;

                if (newTitle && newAuthor && newCopiesAvailable && newDurationType !== '') {
                    updateBook(bookId, newTitle, newAuthor, newCopiesAvailable, newDurationType);
                }
            });

            updateForm.appendChild(titleInput);
            updateForm.appendChild(authorInput);
            updateForm.appendChild(copiesAvailableInput);
            updateForm.appendChild(durationTypeInput);
            updateForm.appendChild(updateButton);

            row.appendChild(updateForm);
        }
    }
});

// Function to loan a book
const loanBook= async(bookID, loanDurationType)=> {
    console.log(loanDurationType)
    // Prompt the user for the customer_id
    const customerIdLoan = prompt('Enter customer ID:');

    if (!customerIdLoan) {

        // The user cancelled the prompt or provided an empty input
        alert('Invalid customer ID');
        return;
    }

    // Prepare the loan data using the parameters
    const loanData = {
        customer_id: customerIdLoan,
        book_id: bookID,
        loan_duration_type: loanDurationType,
    };
    try {
        const response = await axios.post(`${MY_SERVER}/loans/loan`, JSON.stringify(loanData), {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        console.log(response);
        if (response.data.message === 'Book loaned successfully') {
            alert('Book loaned successfully');
            // Update the display to reflect the new loan
        } else {
            alert('Error creating loan: ' + response.data.message);
        }
    } catch (error) {
        console.error('Error creating loan:', error);
    }
}

// Function to return a book
async function returnBook(bookId) {
    const customerIdReturn = prompt('Enter customer ID:');
    const returnData = {
        book_id: bookId,
        customer_id: customerIdReturn
    };

    try {
        const response = await axios.post(`${MY_SERVER}/loans/return`, JSON.stringify(returnData), {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (response.data.message === 'Book returned successfully') {
            alert('Book returned successfully');
            // Update the display to reflect the return
        } else {
            alert('Error returning book: ' + response.data.message);
        }
    } catch (error) {
        console.error('Error returning book:', error);
    }
}

async function updateBook(bookId, newTitle, newAuthor, newCopiesAvailable, newLoanDurationType) {
    const bookData = {
        id: bookId,
        title: newTitle,
        author: newAuthor,
        copies_available: newCopiesAvailable,
        loan_duration_type: newLoanDurationType,
    };

    try {
        const response = await axios.put(`${MY_SERVER}/books/update/${bookId}`, bookData, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.data.message === 'Book updated successfully') {
            alert('Book updated successfully');
            getBooks(); 
        } else {
            alert('Error updating book: ' + response.data.message);
        }
    } catch (error) {
        console.error('Error updating book:', error);
    }
}

async function deleteBook(bookId) {
    try {
        const response = await axios.delete(`${MY_SERVER}/books/delete/${bookId}`, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        console.log('Book deleted:', response.data);
        getBooks(); // Refresh the book list
    } catch (error) {
        console.error('Error deleting book:', error);
        // Handle the error and provide user feedback
    }
}

// Function for show books button listener
document.getElementById('toggleBooksTable').addEventListener('click', function () {
    const booksTable = document.getElementById('display_books');
    if (booksTable.style.display === 'none' || booksTable.style.display === '') {
        booksTable.style.display = 'block';
    } else {
        booksTable.style.display = 'none';
    }
    getBooks();
});

// Function to search for books by name
document.getElementById('book-search-button').addEventListener('click', () => {
    const searchInput = document.getElementById('book-search-input');
    const searchTerm = searchInput.value.trim();
    getBooks(searchTerm);
});

// Function to update countdown timer
function updateCountdownTimer(loanStartDate, dueDate) {
    const now = new Date();
    const timeRemaining = dueDate - now;

    if (timeRemaining <= 0) {
        return "Overdue.";
    }

    const daysRemaining = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
    const hoursRemaining = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutesRemaining = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));

    return `${daysRemaining}d ${hoursRemaining}h ${minutesRemaining}m`;
}

// Function to update countdown timers for loans
document.querySelectorAll('.update-timer').forEach(timerElement => {
    const loanStartDate = new Date(timerElement.getAttribute('data-id-start-date'));
    const dueDate = new Date(timerElement.getAttribute('data-due-date'));
    timerElement.textContent = updateCountdownTimer(loanStartDate, dueDate);
    setInterval(() => {
        timerElement.textContent = updateCountdownTimer(loanStartDate, dueDate);
    }, 60000); // Update every minute (adjust as needed)
});

// Initial loading of books
getBooks();
