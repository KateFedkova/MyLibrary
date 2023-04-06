window.onload = (event) => {

    token = localStorage.getItem("token")
    console.log(token)

    const logout = document.getElementById("logout")

    form = document.getElementById("add-book-form");
    const url = "http://127.0.0.1:5000/add_book";

    const reviewUrl = "http://127.0.0.1:5000/add_review"
    const reviewForm = document.getElementById("add-review")

    logout.addEventListener("click", function (event) {
        localStorage.removeItem("token")
        location.replace("/index.html")
    })

     reviewForm.addEventListener("submit", (event) => {
        event.preventDefault();
        sendRequestToServer(reviewForm, reviewUrl)

        .then(data => {console.log(data)
         location.reload()})
        .catch(error => console.error(error))
        });

     form.addEventListener("submit", (event) => {
        event.preventDefault();
        sendRequestToServer(form, url)

        .then(data => {console.log(data)
        location.reload()})
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
            divForReview.classList.add("one-review")
            const h2 = document.createElement("h4")
            h2.textContent = `Title: ${event.title}`
            const h3 = document.createElement("span")
            h3.textContent = `Author: ${event.author}`
            const h1 = document.createElement("span")
            h1.textContent = `Review: ${event.review}`

            const h6 = document.createElement("span")
            h6.textContent = event.date_added
            h6.classList.add("date")

            const br = document.createElement("br")
            const br1 = document.createElement("br")
            const br2 = document.createElement("br")
            const br3 = document.createElement("br")

            divForReview.appendChild(h2)
            divForReview.appendChild(h3)
            divForReview.appendChild(br2)
            divForReview.appendChild(h1)
            divForReview.appendChild(br3)
            divForReview.appendChild(h6)

            divBody.appendChild(divForReview)
            divBody.appendChild(br)
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