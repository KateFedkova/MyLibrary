window.onload = (event) => {

    token = localStorage.getItem("token")
    console.log(token)

    form = document.getElementById("add-book-form");
    const url = "http://127.0.0.1:5000/add_book";

     form.addEventListener("submit", (event) => {
        event.preventDefault();
        sendRequestToServer(form, url)

        .then(data => console.log(data))
        .catch(error => console.error(error))
        });

    function sendRequestToServer (form, url) {

       const formData = new FormData(form);
       const data = {};

       for (const[key, value] of formData.entries()) {
            data[key] = value
       }

       return new Promise((resolve, reject) => {
            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body:JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => resolve(data))
            .catch((error) => {
                console.log(error);
                reject(error);
            })
       })

    }


    function Books(eventsFromApi) {
        console.log(eventsFromApi)
        const tableBody = document.getElementById("table-body")

        eventsFromApi.forEach(function (event) {
            event = JSON.parse(event)
            const tr1 = document.createElement("tr")
            console.log(tr1)
            const td1 = document.createElement("td")

            console.log(tr1)
            td1.textContent = event.title
             tr1.appendChild(td1)
            const td2 = document.createElement("td")
            td2.textContent = event.author
            tr1.appendChild(td2)
            tableBody.appendChild(tr1)

    })
    }

    function getBooks() {

        const apiUrl = "http://127.0.0.1:5000/get_books"

        return fetch(apiUrl, {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${token}`}
            })
        .then(data => data.json())
        .catch(error => console.error(error))

}

    getBooks()
    .then(data => Books(data))
}