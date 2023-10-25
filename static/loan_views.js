const MY_SERVER = 'http://127.0.0.1:5000';

// Function to get loans
async function getLoans() {
    try {
        const response = await axios.get(MY_SERVER + '/loans');
        const loans = response.data;
        const tableBody = document.getElementById('loan-table-body');
        tableBody.innerHTML = ''; // Clear the table body

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
        // Handle the error and provide user feedback
    }
}

// Function to loan a book
async function loanBook(bookID, loanDurationType) {
    // Prompt the user for the customer_id
    const customerID = prompt('Enter customer ID:');

    if (!customerID) {
        // The user cancelled the prompt or provided an empty input
        alert('Invalid customer ID');
        return;
    }

    // Prepare the loan data
    const loanData = {
        customer_id: customerID,
        book_id: bookID,  // This should receive the book_id parameter
        loan_duration_type: loanDurationType,  // This should receive the loan_duration_type parameter
        due_date: dueDate,
    };

    try {
        const response = await axios.post(`${MY_SERVER}/loans/loan`, loanData, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.data.message === 'Book loaned successfully') {
            alert('Book loaned successfully');
            // Update the display to reflect the new loan
            getLoans(); // Refresh the loans list
        } else {
            alert('Error creating loan: ' + response.data.message);
        }
    } catch (error) {
        console.error('Error creating loan:', error);
    }
}

// Function to return a book
async function returnBook() {
    const loanID = document.getElementById('loanID').value;
    const returnDate = document.getElementById('returnDate').value;

    const returnData = {
        loan_id: loanID,
        return_date: returnDate,
    };

    try {
        const response = await axios.post(`${MY_SERVER}/loans/return`, returnData, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.data.message === 'Book returned successfully') {
            alert('Book returned successfully');
            // Update the display to reflect the return
            getLoans(); // Refresh the loans list
        } else {
            alert('Error returning book: ' + response.data.message);
        }
    } catch (error) {
        console.error('Error returning book:', error);
    }
}

// Function to toggle the loans table
function toggleLoanTable() {
    const loanTable = document.getElementById('display_loans');
    if (loanTable.style.display === 'none' || loanTable.style.display === '') {
        loanTable.style.display = 'block';
    } else {
        loanTable.style.display = 'none';
    }
    getLoans();
}

const toggleLoansTable = document.getElementById('toggleLoansTable');
toggleLoansTable.addEventListener('click', toggleLoanTable);
// Function to display late loans
function displayLateLoans(lateLoans) {
    const lateLoansTable = document.getElementById('lateLoansTable');
    lateLoansTable.innerHTML = ''; // Clear the table

    if (lateLoans.length > 0) {
        const table = document.createElement('table');
        const tableHeader = document.createElement('thead');
        const tableBody = document.createElement('tbody');

        // Create table headers
        const headerRow = document.createElement('tr');
        const headers = ['ID', 'Customer ID', 'Book ID', 'Due Date', 'Loan Start Date'];
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });

        tableHeader.appendChild(headerRow);
        table.appendChild(tableHeader);

        // Populate the table with late loans
        lateLoans.forEach(loan => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${loan.id}</td>
                <td>${loan.customer_id}</td>
                <td>${loan.book_id}</td>
                <td>${loan.due_date}</td>
                <td>${loan.loan_start_date}</td>
            `;
            tableBody.appendChild(row);
        });

        table.appendChild(tableBody);
        lateLoansTable.appendChild(table);
    } else {
        // No late loans, display a message
        const noLateLoansMessage = document.createElement('p');
        noLateLoansMessage.textContent = 'No late loans';
        lateLoansTable.appendChild(noLateLoansMessage);
    }
}

// Function to fetch and display late loans
async function showLateLoans() {
    const lateLoansTable = document.getElementById('lateLoansTable');
    lateLoansTable.style.display = 'block';

    try {
        // Fetch late loans from the server
        const response = await axios.get(MY_SERVER + '/loans/late');
        const lateLoans = response.data;
        
        // Display late loans
        displayLateLoans(lateLoans);
    } catch (error) {
        console.error(error);
        // Handle the error and provide user feedback
    }
}

// Event listener for the "Show Late Loans" button
const toggleLateLoansButton = document.getElementById('toggleLateLoansButton');
toggleLateLoansButton.addEventListener('click', showLateLoans);

// Call the function to fetch and display loans when needed
getLoans();
