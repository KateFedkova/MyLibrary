window.onload = (event) => {

    token = localStorage.getItem("token")

    const divForBookInfo = document.getElementById("all-found-books")
    searchByTitleLabel = document.getElementById("search-by-title-label")
    searchByTitle = document.getElementById("search-by-title")
    searchButton = document.getElementById("search-button")
    warning = document.getElementById("warning")

    searchForm = document.getElementById("search-form")
    option = document.getElementById("select-items")
     searchByAuthorLabel = document.getElementById("search-by-author-label")
    searchByAuthor = document.getElementById("search-by-author")

    selectGenres = document.getElementById("select-genres")
    category = document.getElementById("category")

    searchByAuthor.style.display = "none"
    searchByAuthorLabel.style.display = "none"
    selectGenres.style.display = "none"
    warning.style.display = "none"
    category.style.display = "none"

    option.addEventListener("change", function (event) {
        value = option.value
        if (option.value === "title") {
            searchByAuthor.style.display = "none"
            searchByAuthorLabel.style.display = "none"
            selectGenres.style.display = "none"
            searchByTitle.style.display = "block"
            searchByTitleLabel.style.display = "block"
             category.style.display = "none"
        }

        if (option.value === "author") {
            searchByAuthor.style.display = "block"
            searchByAuthorLabel.style.display = "block"
            searchByTitle.style.display = "none"
            searchByTitleLabel.style.display = "none"
            selectGenres.style.display = "none"
             category.style.display = "none"
        }

        if (option.value === "categories") {
            searchByAuthor.style.display = "none"
            searchByAuthorLabel.style.display = "none"
            searchByTitle.style.display = "none"
            searchByTitleLabel.style.display = "none"
            selectGenres.style.display = "block"
            category.style.display = "block"
        }
    })


    allFoundBooks = document.getElementById("all-found-books")


    searchButton.addEventListener("click", function (event) {

       event.preventDefault()
       divForBookInfo.innerHTML = ""
       warning.style.display = "block"
       const formData = new FormData(searchForm);
       const data = {};

       for (const[key, value] of formData.entries()) {
            data[key] = value
       }
       option.value === "categories"
       if (option.value === "categories") {data["category"] = selectGenres.value}

        searchResults(data)
        .then(function (result) {
                if (option.value === "title")
                    {displayBooks(result)}
                else if (option.value === "author")
                    {
                    displayAuthors(result)
                    }
                else {displayAuthors(result)}
                })

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
        title.textContent = `Title: ${book.title}`
        const br1 = document.createElement("br")
        const br2 = document.createElement("br")
        const br3 = document.createElement("br")

        const description = document.createElement("span")
        description.textContent = `Description: ${book.description}`
        description.classList.add("cards")

        const subject_places = document.createElement("span")
        subject_places.textContent = `Places: ${book.subject_places}`
        subject_places.classList.add("cards")

        const subjects = document.createElement("span")
        subjects.textContent = `Subjects: ${book.subjects}`
        subjects.classList.add("cards")

        const subject_times = document.createElement("span")
        subject_times.textContent = `Times: ${book.subject_times}`
        subject_times.classList.add("cards")

        divForBookInfo.appendChild(title)
        divForBookInfo.appendChild(description)
        divForBookInfo.appendChild(br1)
        divForBookInfo.appendChild(subject_places)
        divForBookInfo.appendChild(br2)
        divForBookInfo.appendChild(subjects)
        divForBookInfo.appendChild(br3)
        divForBookInfo.appendChild(subject_times)

    }


    function displayAuthors(book) {
        const divForBookInfo = document.getElementById("all-found-books")

        book.forEach(function (event) {

            const bookDiv = document.createElement("div")
            const title = document.createElement("h2")
            title.textContent = event.title
            const br1 = document.createElement("br")
            const br2 = document.createElement("br")
            const br3 = document.createElement("br")
            const br = document.createElement("br")

            const description = document.createElement("span")
            description.textContent = `1. Description: ${event.description}`


            const subject_places = document.createElement("span")
            subject_places.textContent = `2. Places: ${event.subject_places}`

            const subjects = document.createElement("span")
            subjects.textContent =  `3. Subjects: ${event.subjects}`

            const subject_times = document.createElement("span")
            subject_times.textContent = `4. Times: ${event.subject_times}`

            bookDiv.appendChild(title)
            bookDiv.appendChild(description)
            bookDiv.appendChild(br)
            bookDiv.appendChild(subject_places)
            bookDiv.appendChild(br1)
            bookDiv.appendChild(subjects)
            bookDiv.appendChild(br2)
            bookDiv.appendChild(subject_times)
            bookDiv.appendChild(br3)
            divForBookInfo.appendChild(bookDiv)
        })
    }
}
