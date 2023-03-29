window.onload = (event) => {
    token = localStorage.getItem("token")
    console.log(token)
    console.log("here1")
    console.log("12]04ijf")

    const form = document.getElementById("login-form");
    const url = "http://127.0.0.1:5000/login";
    console.log("here1")
    console.log("12]04ijf")

    form.addEventListener("submit", (event) => {
    console.log("here")
        event.preventDefault();
        sendRequestToServer(form, url)

        .then(data => console.log(data))
        location.replace("/main.html")
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
            localStorage.setItem("token", data["token"])
            .catch((error) => {
                console.log(error);
                reject(error);
            })
       })

    }

    }