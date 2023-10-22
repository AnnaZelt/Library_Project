const MY_SERVER = 'http://127.0.0.1:5000';

const getBooks = async () => {
    try {
        const response = await axios.get(MY_SERVER + '/books');
        const books = response.data;
        const tableBody = document.getElementById('book-table-body');

        books.forEach(book => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book['available copies']}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
    }
};

getBooks();
