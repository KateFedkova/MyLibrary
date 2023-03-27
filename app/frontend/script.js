window.onload = (event) => {

    const form = document.getElementById("signup-form");
    const url = "http://127.0.0.1:5000/signup";

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        sendRequestToServer(form, url)

        .then(data => console.log(data))
        location.replace("/index.html")
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

    }