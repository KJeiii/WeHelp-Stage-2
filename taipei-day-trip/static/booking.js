async function createItinerary () {
    let itineraryInfo = {
        "user_id": 6,
        "attraction_id": 22,
        "date": "2023-10-10",
        "time": "afternoon",
        "price": 2500
    };

    try{
        let response = await fetch("/api/booking",{
            method: "POST",
            headers: {
                "authorization": `Bearer ${window.localStorage.getItem("token")}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(itineraryInfo)
            });
    }
    catch(error) {
        console.log(error);
    };        
};

function loadPage() {
    SignStatus().then((result) => {
        if (result["ok"] === true) {
            let welceomMsg = document.querySelector(".welcomeMsg");
            welceomMsg.textContent = `您好，${result["data"]["name"]}，待預訂的行程如下：`;

            fetch("api/booking", {
                method: "GET",
                headers: {
                    "authorization": `Bearer ${window.localStorage.getItem("token")}`
                }
            })
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                //parse itinerary information from response body
                itineraryInfo = data["data"];

                console.log(itineraryInfo);
                if (itineraryInfo !== null) {
                // query all html elements need to be modified
                let//
                image = document.querySelector("figure"),
                itineraryTitle = document.querySelector(".itinerary-title"),
                itineraryValues = document.querySelectorAll(".itinerary-value"),
                date = itineraryValues[0],
                time = itineraryValues[1],
                fee = itineraryValues[2],
                address = itineraryValues[3],
                contactName = document.querySelector("input[name=contact-name]"),
                contactEmail = document.querySelector("input[name=contact-email]"),
                totalPrice = document.querySelector(".checkbill-inner p");
    
                // modify html elements
                image.style.backgroundImage = `url(${itineraryInfo["attraction"]["image"]})`;
                itineraryTitle.textContent = `台北一日遊：${itineraryInfo["attraction"]["name"]}`;
                date.textContent = itineraryInfo["date"];
                if (itineraryInfo["time"] === "beforenoon") {
                    time.textContent = "早上9點到下午4點"
                }
                else{
                    time.textContent = "下午4點到下午9點";
                };
                fee.textContent = `新台幣${itineraryInfo["price"]}元`;
                address.textContent = itineraryInfo["attraction"]["address"];
                contactName.value = result["data"]["name"];
                contactEmail.value = result["data"]["email"];
                totalPrice.textContent = `總價：新台幣${itineraryInfo["price"]}元`;
                }
                else{
                    let// 
                    itineraryDiv = document.querySelector(".itinerary"),
                    bottomSection = document.querySelector(".bottomSection"),
                    noItinerary = document.createElement("p"),
                    itineraryInner = document.querySelector(".itineraryInner");
                    itineraryDiv.style.display = "none";
                    bottomSection.style.display = "none";
                    noItinerary.textContent = "目前沒有任何待預訂的行程";
                    noItinerary.setAttribute("class", "no-itinerary");
                    itineraryInner.appendChild(noItinerary);
                };
            })
            .catch(error => {
                console.log(error);
            });
        }
        else {
            window.location.replace("/");
        }
    })
};

loadPage();

async function deleteItinerary() {
    SignStatus().then((result) => {
        if (result["ok"] === true){
         fetch("api/booking", {
            method: "DELETE",
            headers: {
                "authorization": `Bearer ${window.localStorage.getItem("token")}`
            }
         })
         .then(res => {
            window.location.replace(window.location.href);
            return res.json()})
         .then(data => {
            console.log(data);
         })
         .catch(error => {console.log(error)})
        };
    })
    .catch(error => {
        console.log(error);
    });
};