window.onload = (event) => {

    token = localStorage.getItem("token")
    console.log(token)

    form = document.getElementById("add-book-form");
    const url = "http://127.0.0.1:5000/add_book";

    const reviewUrl = "http://127.0.0.1:5000/add_review"
    const reviewForm = document.getElementById("add-review")

     reviewForm.addEventListener("submit", (event) => {
        event.preventDefault();
        sendRequestToServer(reviewForm, reviewUrl)

        .then(data => console.log(data))
        .catch(error => console.error(error))
        });

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
            const td1 = document.createElement("td")
            td1.textContent = event.title
            tr1.appendChild(td1)
            const td2 = document.createElement("td")
            td2.textContent = event.author
            tr1.appendChild(td2)
            tableBody.appendChild(tr1)

    })
    }

    function Reviews(eventsFromApi) {
        console.log(eventsFromApi)
        const divBody = document.getElementById("all-posts")

        eventsFromApi.forEach(function (event) {
            event = JSON.parse(event)
            const divForReview = document.createElement("div")
            const h2 = document.createElement("h2")
            h2.textContent = event.title
            const h3 = document.createElement("h3")
            h3.textContent = event.author
            const h1 = document.createElement("h1")
            h1.textContent = event.review
            divForReview.appendChild(h2)
            divForReview.appendChild(h3)
            divForReview.appendChild(h1)

            divBody.appendChild(divForReview)
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

     function getReviews() {
        const apiUrl = "http://127.0.0.1:5000/get_reviews"
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

    getReviews()
    .then(data => Reviews(data))

}