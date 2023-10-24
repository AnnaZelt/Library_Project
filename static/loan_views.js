const MY_SERVER = 'http://127.0.0.1:5000';

const getLoans = async () => {
    try {
        const response = await axios.get(MY_SERVER + '/loans'); // Update the endpoint to fetch loans
        const loans = response.data;
        const tableBody = document.getElementById('loan-table-body');

        loans.forEach(loan => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${loan.id}</td>
                <td>${loan.customer_id}</td>
                <td>${loan.book_id}</td>
                <td>${loan.due_date}</td>
                <td>${loan.return_date != null ? loan.return_date : 'Borrowed'}</td>
                <td>${loan.loan_start_date}</td>
            `;
            tableBody.appendChild(row);
        });        
    } catch (error) {
        console.error(error);
    }
};

// Loan a Book
document.getElementById('loanBookButton').addEventListener('click', async () => {
    const customerID = document.getElementById('customerID').value;
    const bookID = document.getElementById('bookID').value;
    const dueDate = document.getElementById('dueDate').value;

    // Send an HTTP POST request to loan a book
    const response = await axios.post('/loans/loan', {
        customer_id: customerID,
        book_id: bookID,
        due_date: dueDate,
    });

    // Handle the response and update the display
    if (response.data.message === 'Loan created successfully') {
        // Update the display to reflect the new loan
    } else {
        // Handle errors
    }
});

// Return a Book
document.getElementById('returnBookButton').addEventListener('click', async () => {
    const loanID = document.getElementById('loanID').value;
    const returnDate = document.getElementById('returnDate').value;

    // Send an HTTP POST request to return a book
    const response = await axios.post('/loans/return', {
        loan_id: loanID,
        return_date: returnDate,
    });

    // Handle the response and update the display
    if (response.data.message === 'Book returned successfully') {
        // Update the display to reflect the return
    } else {
        // Handle errors
    }
});


function toggleTable(tableId) {
    const table = document.getElementById(tableId);
    if (table.style.display === 'none') {
        table.style.display = 'block';
    } else {
        table.style.display = 'none';
    }
}

const toggleLoansTable = document.getElementById('toggleLoansTable');
toggleLoansTable.addEventListener('click', () => {
    toggleTable('display_loans');
});
// Call the function to fetch and display loans when needed
getLoans();
