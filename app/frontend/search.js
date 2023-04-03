window.onload = (event) => {

    token = localStorage.getItem("token")
    console.log(token)


    searchByTitleLabel = document.getElementById("search-by-title-label")
    searchByTitle = document.getElementById("search-by-title")

    searchForm = document.getElementById("search-form")
    option = document.getElementById("select-items")
    console.log(option.value)

    searchByAuthorLabel = document.getElementById("search-by-author-label")
    searchByAuthor = document.getElementById("search-by-author")

    searchByAuthor.style.display = "none"
    searchByAuthorLabel.style.display = "none"

    allFoundBooks = document.getElementById("all-found-books")

    if (option.value === "author") {
        searchByAuthor.style.display = "block"
        searchByAuthorLabel.style.display = "block"
        searchByTitle.style.display = "none"
        searchByTitleLabel.style.display = "none"
    }


    searchForm.addEventListener("submit", function (event) {

       event.preventDefault()
       const formData = new FormData(searchForm);
       const data = {};

       for (const[key, value] of formData.entries()) {
            data[key] = value
       }

        searchResults(data)
        .then(data => displayBooks(data))

    })

    function searchResults(data) {
    const url =  "http://127.0.0.1:5000/search"
    return new Promise((resolve, reject) => {
            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                },
                body:JSON.stringify(data)
            })
            .then(data => data.json())
            .then(data => resolve(data))
            .catch((error) => {
                console.log(error);
                reject(error);
            })
       })
    }


    function displayBooks(book) {
        const divForBookInfo = document.getElementById("all-found-books")
        console.log(book)
        console.log(typeof(book))

        const title = document.createElement("h2")
        title.textContent = book.title

        const description = document.createElement("h3")
        description.textContent = book.description

        const subject_places = document.createElement("h3")
        subject_places.textContent = book.subject_places

        const subjects = document.createElement("h3")
        subjects.textContent = book.subjects

        const subject_times = document.createElement("h3")
        subject_times.textContent = book.subject_times

        divForBookInfo.appendChild(title)
        divForBookInfo.appendChild(description)
        divForBookInfo.appendChild(subject_places)
        divForBookInfo.appendChild(subjects)
        divForBookInfo.appendChild(subject_times)

    }
}
