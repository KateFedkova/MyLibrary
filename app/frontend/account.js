window.onload = (event) => {

    token = localStorage.getItem("token")
    console.log(token)

    const header = document.getElementById("header")
    const button = document.getElementById("update-account")
    const updateButton = document.getElementById("update-button")
    const updateUsername = document.getElementById("update-username")

    const updateForm = document.getElementById("update-form")
    updateForm.style.display = "none"


    button.addEventListener("click", function (event) {
        updateForm.style.display="block"
        button.style.display="none"

    })

    updateButton.addEventListener("click", function (event) {
         event.preventDefault();
         const formData = new FormData(updateForm);
         const data = {};

        for (const[key, value] of formData.entries()) {
             data[key] = value
        }

         updateForm.style.display="none"
         button.style.display="block"
         sendChangedData(data)
    })


    function getUserInfo() {
    const url = "http://127.0.0.1:5000/get_username"

    return new Promise((resolve, reject) => {
            fetch(url, {
            method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                }
            })
              .then(response => response.json())
              .then(data => resolve(data))
              .catch(error => {console.error(error)
               reject(error);})
       })
}

     getUserInfo()
    .then(function(result) {
        result = JSON.parse(result)
        header.textContent = `Hello ${result["username"]}`
        updateUsername.value = result["username"]
    })


    function sendChangedData (data) {
        const url =  "http://127.0.0.1:5000/change_info"

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify(data)
        })
       .then(response => response.json())
       .catch(error => console.log(error))
       }

}